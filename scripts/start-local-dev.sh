#!/bin/bash
docker-compose up -d
echo -n "waiting for localstack to be ready: "
until $(curl --output /dev/null --silent --head http://localhost:4566); do
    echo -n '.'
    sleep 2
done
echo " done"
$(dirname ${BASH_SOURCE[0]})/populate_localstack.sh
