# Chalice dockerfile
FROM ubuntu:focal

ENV APP_NAME=corpora-api
ENV DEPLOYMENT_STAGE=dev
ENV EXPORT_ENV_VARS_TO_LAMBDA="APP_NAME DEPLOYMENT_STAGE"
ENV LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

ADD chalice/api_server /chalice
WORKDIR /chalice

RUN apt-get update && \
    apt-get install -y gettext moreutils build-essential libxml2-dev python3-dev python3-pip zlib1g-dev python3-requests python3-aiohttp llvm

# Clean up artifacts.
RUN rm -rf __pycache__ vendor chalicelib/config chalicelib/corpora .chalice/venv .chalice/deployments .chalice/deployed

RUN mv .chalice/config.json.dev .chalice/config.json
# RUN envsubst < config/iam-policy-templates/corpora-api-lambda.json > .chalice/policy-$(DEPLOYMENT_STAGE).json


RUN mkdir -p chalicelib config vendor
ADD corpora chalicelib/corpora
ADD config/corpora-api.yml chalicelib/config/corpora-api.yml

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "run_local_server.py"]
