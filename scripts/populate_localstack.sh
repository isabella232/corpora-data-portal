#!/bin/bash
export AWS_REGION=us-west-2
export AWS_ACCESS_KEY_ID=nonce
export AWS_SECRET_ACCESS_KEY=nonce

aws --endpoint-url=http://localhost:4566 s3api create-bucket --bucket corpora-data-dev || true
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret --name corpora/backend/dev/auth0-secret || true
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret --name corpora/backend/dev/database_local || true
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret --name corpora/backend/test/database_local || true

echo test-h5ad-file > fake-h5ad-file.h5ad
aws --endpoint-url=http://localhost:4566 s3 cp fake-h5ad-file.h5ad s3://corpora-data-dev/
rm fake-h5ad-file.h5ad

aws --endpoint-url=http://localhost:4566 secretsmanager update-secret --secret-id corpora/backend/dev/auth0-secret --secret-string '{"client_id":"dev-client-id","client_secret":"dev-client-secret","audience":"dev-client-id","grant_type":"client_credentials","api_base_url":"https://localhost:8443","cookie_name":"cxguser","callback_base_url":"https://localhost:5000","redirect_to_frontend":"http://localhost:8000"}' || true
aws --endpoint-url=http://localhost:4566 secretsmanager update-secret --secret-id corpora/backend/dev/database_local --secret-string '{"database_uri": "postgresql://corpora:test_pw@database:5432"}' || true
aws --endpoint-url=http://localhost:4566 secretsmanager update-secret --secret-id corpora/backend/test/database_local --secret-string '{"database_uri": "postgresql://corpora:test_pw@localhost:5432"}' || true

export CORPORA_LOCAL_DEV=true
export BOTO_ENDPOINT_URL=http://localhost:4566
python3 $(dirname ${BASH_SOURCE[0]})/populate_db.py
