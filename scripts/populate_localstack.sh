#!/bin/bash

aws --endpoint-url=http://localhost:4566 secretsmanager create-secret --name corpora/backend/dev/auth0-secret || true
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret --name corpora/backend/dev/database_local || true
aws --endpoint-url=http://localhost:4566 secretsmanager create-secret --name corpora/backend/test/database_local || true

aws --endpoint-url=http://localhost:4566 secretsmanager update-secret --secret-id corpora/backend/dev/auth0-secret --secret-string '{"client_id":"xxx","client_secret":"yyy","audience":"https://localhost:5000","grant_type":"client_credentials"}' || true
aws --endpoint-url=http://localhost:4566 secretsmanager update-secret --secret-id corpora/backend/dev/database_local --secret-string '{"database_uri": "postgresql://corpora:test_pw@database:5432"}' || true
aws --endpoint-url=http://localhost:4566 secretsmanager update-secret --secret-id corpora/backend/test/database_local --secret-string '{"database_uri": "postgresql://corpora:test_pw@localhost:5432"}' || true

export CORPORA_LOCAL_DEV=true
export BOTO_ENDPOINT_URL=http://localhost:4566
export AWS_ACCESS_KEY_ID=nonce
export AWS_SECRET_ACCESS_KEY=nonce
python3 $(dirname ${BASH_SOURCE[0]})/populate_db.py
