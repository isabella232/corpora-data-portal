import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import json
import requests


def merge_unique(a, b):
    """
    Merge entries from 'b' into 'a' if not in 'a'
    :param a:
    :param b:
    :return:
    """
    unique_keys = set(b.keys())
    unique_keys.difference_update(set(a.keys()))
    for unique_key in unique_keys:
        a[unique_key] = b[unique_key]


def convert():
    with open("./chalicelib/config/corpora-api.yml") as fp:
        corpora_api = data = yaml.load(fp, Loader=Loader)

    # Convert chalice swagger to openapi 3.0
    with open("./dist/chalice.tf.json") as fp:
        chalice_tf = json.load(fp)
    chalice_swagger = json.loads(chalice_tf["data"]["template_file"]["chalice_api_swagger"]["template"])
    chalice_swagger = requests.post(
        "https://converter.swagger.io/api/convert",
        headers={"accept": "application/json", "Content-Type": "application/json"},
        data=json.dumps(chalice_swagger),
    ).json()

    # Add x-amazon-apigateway-binary-media-types
    corpora_api["x-amazon-apigateway-binary-media-types"] = chalice_swagger["x-amazon-apigateway-binary-media-types"]

    # Update Paths
    for path, path_def in corpora_api["paths"].items():
        swag_path_def = chalice_swagger["paths"][path]
        for cmd, cmd_def in path_def.items():
            merge_unique(cmd_def, swag_path_def[cmd])
        merge_unique(path_def, swag_path_def)
    merge_unique(corpora_api["paths"], chalice_swagger["paths"])
    merge_unique(corpora_api["components"]["schemas"], chalice_swagger["components"]["schemas"])

    chalice_tf["data"]["template_file"]["chalice_api_swagger"]["template"] = json.dumps(corpora_api)
    with open("./dist/chalice.tf.json", "w") as fp:
        json.dump(chalice_tf, fp)


if __name__ == "__main__":
    convert()
