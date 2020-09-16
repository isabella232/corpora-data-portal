import json
import logging
import os
import re
import sys
from collections import defaultdict
from functools import wraps

import chalice
import connexion
from chalice import Chalice, CORSConfig
from connexion import FlaskApi, ProblemException, problem

pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "chalicelib"))  # noqa
sys.path.insert(0, pkg_root)  # noqa

from corpora.common.authorizer import assert_authorized_token
from corpora.common.utils.json import CustomJSONEncoder
from corpora.common.utils.aws_secret import AwsSecret
from corpora.common.corpora_config import CorporaAuthConfig, CorporaConfig

cors_config = CORSConfig(allow_origin="*", max_age=600, allow_credentials=True)


if "PSYCOGREEN" in os.environ:
    from gevent.monkey import patch_all
    patch_all()
    from psycogreen.gevent import patch_psycopg
    patch_psycopg()

    CorporaConfig.using_gevent = True

def requires_auth():
    """
    A decorator for assert_authorized
    :return: 401 or the original function response.
    """

    def decorate(func):
        @wraps(func)
        def call(*args, **kwargs):
            token = app.current_request.cookies.get(CorporaAuthConfig.cookie_name)
            assert_authorized_token(token)
            return func(*args, **kwargs)

        return call

    return decorate


def create_flask_app():
    app = connexion.FlaskApp(f"{os.environ['APP_NAME']}-{os.environ['DEPLOYMENT_STAGE']}")
    swagger_spec_path = os.path.join(pkg_root, "config", f"{os.environ['APP_NAME']}.yml")
    app.add_api(swagger_spec_path, validate_responses=True)
    return app.app


def get_chalice_app(flask_app):
    app = Chalice(app_name=flask_app.name)
    flask_app.debug = True
    app.debug = flask_app.debug
    app.log.setLevel(logging.DEBUG)

    # set the flask secret key, needed for session cookies
    flask_secret_key = "OpenSesame"
    deployment = os.environ["DEPLOYMENT_STAGE"]
    if deployment != "test":
        secret_name = f"corpora/backend/{os.environ['DEPLOYMENT_STAGE']}/auth0-secret"
        auth_secret = json.loads(AwsSecret(secret_name).value)
        if auth_secret:
            flask_secret_key = auth_secret.get("flask_secret_key", flask_secret_key)
    # FIXME, enforce that the flask_secret_key is found once all secrets are setup for all environments
    flask_app.config.update(SECRET_KEY=flask_secret_key)

    def clean_entry_for_logging(entry):
        log = entry.to_dict()
        log.pop("body", None)
        return log

    def dispatch(*args, **kwargs):
        app.log.info(f"Request: {clean_entry_for_logging(app.current_request)}")

        uri_params = app.current_request.uri_params or {}
        resource_path = app.current_request.context["resourcePath"].format(**uri_params)
        req_body = app.current_request.raw_body if app.current_request._body is not None else None

        # Must convert the chalice.MultiDict into a list of tuples. Chalice returns chalice.Multidict which is
        # incompatible with the werkzeug.MultiDict expected by Flask.
        query_string = list(app.current_request.query_params.items()) if app.current_request.query_params else None

        with flask_app.test_request_context(
            path=resource_path,
            base_url="https://{}".format(app.current_request.headers["host"]),
            query_string=query_string,
            method=app.current_request.method,
            headers=list(app.current_request.headers.items()),
            data=req_body,
            environ_base=app.current_request.stage_vars,
        ):
            flask_res = flask_app.full_dispatch_request()

        response_headers = dict(flask_res.headers)
        response_headers.update({"X-AWS-REQUEST-ID": app.lambda_context.aws_request_id})

        chalice_response = chalice.Response(
            status_code=flask_res._status_code,
            headers=response_headers,
            body="".join([c.decode() if isinstance(c, bytes) else c for c in flask_res.response]),
        )

        app.log.info(f"Response: {clean_entry_for_logging(chalice_response)}")

        return chalice_response

    routes = defaultdict(list)
    for rule in flask_app.url_map.iter_rules():
        routes[re.sub(r"<(.+?)(:.+?)?>", r"{\1}", rule.rule).rstrip("/")] += rule.methods
    for route, methods in routes.items():
        app.route(route, methods=list(set(methods) - {"OPTIONS"}), cors=cors_config)(dispatch)

    with open(os.path.join(pkg_root, "index.html")) as swagger_ui_file_object:
        swagger_ui_html = swagger_ui_file_object.read()

    @app.route("/", methods=["GET", "HEAD"])
    def serve_swagger_ui():
        return chalice.Response(
            status_code=200,
            headers={"Content-Type": "text/html", "X-AWS-REQUEST-ID": app.lambda_context.aws_request_id},
            body=swagger_ui_html,
        )

    flask_app.json_encoder = CustomJSONEncoder

    @flask_app.errorhandler(ProblemException)
    def handle_corpora_error(exception):
        response = problem(
            exception.status,
            exception.title,
            exception.detail,
            exception.type,
            exception.instance,
            exception.headers,
            exception.ext,
        )
        response.headers["X-AWS-REQUEST-ID"] = app.lambda_context.aws_request_id
        return FlaskApi.get_response(response)

    return app


app = get_chalice_app(create_flask_app())
