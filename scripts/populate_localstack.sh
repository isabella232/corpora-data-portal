#!/bin/bash
export AWS_REGION=us-west-2
export AWS_ACCESS_KEY_ID=nonce
export AWS_SECRET_ACCESS_KEY=nonce

echo "Creating secretsmanager secrets"
aws --endpoint-url=http://localhost:4566 s3api create-bucket --bucket corpora-data-dev &> /dev/null || true
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret --name corpora/backend/dev/auth0-secret &> /dev/null || true
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret --name corpora/backend/dev/database_local &> /dev/null || true
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret --name corpora/backend/test/database_local &> /dev/null || true


echo "Updating secrets"
aws --endpoint-url=http://localhost:4566 secretsmanager update-secret --secret-id corpora/backend/dev/auth0-secret --secret-string '{
    "client_id": "dev-client-id",
    "client_secret": "dev-client-secret",
    "audience": "dev-client-id",
    "grant_type": "client_credentials",
    "api_authorize_url": "https://localhost:8443/connect/authorize",
    "api_base_url": "https://localhost:8443",
    "api_token_url": "http://oidc/connect/token",
    "cookie_name": "cxguser",
    "callback_base_url": "http://localhost:5000",
    "redirect_to_frontend": "http://localhost:8000"
}' || true
aws --endpoint-url=http://localhost:4566 secretsmanager update-secret --secret-id corpora/backend/dev/database_local --secret-string '{"database_uri": "postgresql://corpora:test_pw@database:5432"}' || true
aws --endpoint-url=http://localhost:4566 secretsmanager update-secret --secret-id corpora/backend/test/database_local --secret-string '{"database_uri": "postgresql://corpora:test_pw@database:5432"}' || true

# Make a 1mb data file
echo "Writing test file to s3"
dd if=/dev/zero of=fake-h5ad-file.h5ad bs=1024 count=1024 &> /dev/null
aws --endpoint-url=http://localhost:4566 s3 cp fake-h5ad-file.h5ad s3://corpora-data-dev/
rm fake-h5ad-file.h5ad

echo "Populating test db"
export CORPORA_LOCAL_DEV=true
export BOTO_ENDPOINT_URL=http://localhost:4566
python3 $(dirname ${BASH_SOURCE[0]})/populate_db.py
