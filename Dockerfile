FROM ubuntu:bionic

ENV APP_NAME=corpora-api
ENV DEPLOYMENT_STAGE=dev

WORKDIR /project
ADD backend/corpora /project
ADD backend/flask/app.py /project/app.py
ADD backend/flask/index.html /project/index.html
ADD backend/flask/requirements.txt /project/requirements.txt

RUN \
apt-get update && \
apt-get install -y build-essential libxml2-dev python3-dev python3-pip zlib1g-dev python3-requests python3-aiohttp llvm && \
python3 -m pip install -r requirements.txt

CMD ["python3", "app.py"]
