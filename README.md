# Corpora Data Portal

![Push Tests](https://github.com/chanzuckerberg/corpora-data-portal/workflows/Push%20Tests/badge.svg)
[![codecov](https://codecov.io/gh/chanzuckerberg/corpora-data-portal/branch/main/graph/badge.svg)](https://codecov.io/gh/chanzuckerberg/corpora-data-portal)
[![Maintainability](https://api.codeclimate.com/dp/v1/badges/9416c313de4d0457a5cc/maintainability)](https://codeclimate.com/github/chanzuckerberg/corpora-data-portal/maintainability)

The Corpora Data Portal (CDP) enables the publication, discovery and exploration of interoperable
single-cell datasets. Data contributors can upload, review and publish datasets for private or
public use. Via the portal, data consumers are able to discover, download and connect data to visualization tools
such as [cellxgene](https://chanzuckerberg.github.io/cellxgene/posts/cellxgene_cziscience_com) to perform further
analysis. The goal of the CDP is to catalyze distributed collaboration of single-cell research by providing a large,
well-labeled repository of interoperable datasets.

## Developers

### Development quickstart
See [DEV_ENV.md](DEV_ENV.md) for the local development guide.

### Pre-requisites

1. [Install and configure awscli](docs/awscli.md)
1. [Configure ssh access](https://github.com/chanzuckerberg/single-cell-infra#ssh)

### Environment variables

| Name                | Description                                                                                                                                                                               | Values                                |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| `DEPLOYMENT_STAGE`  | Specifies an app deployment stage for tasks such as deployments and functional tests.                                                                                                     | `dev`, `staging`, `prod`              |
| `AWS_PROFILE`       | Specifies the profile used to interact with AWS resources via awscli.                                                                                                                     | `single-cell-dev`, `single-cell-prod` |
| `CORPORA_LOCAL_DEV` | If this variable is set to any value, the Corpora app will look for the database on **localhost:5432** and will use the aws secret _corpora/backend/\${DEPLOYMENT_STAGE}/database_local_. | Any                                   |

### Commands

| Command                 | Description                                                                          | Notes                                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| `make fmt`              | Auto-format codebase using [black](https://pypi.org/project/black/).                 | This should be run before merging in any changes.                                                    |
| `make lint`             | Perform lint checks on codebase using [flake8](https://flake8.pycqa.org/en/latest/). | This should be run before merging in any changes.                                                    |
| `make unit-test`        | Run all unit tests.                                                                  |                                                                                                      |
| `make functional-tests` | Run all functional tests.                                                            | These tests run against a deployed environment which is selected by the value of `DEPLOYMENT_STAGE`. |

### Deployment

1. Set `DEPLOYMENT_STAGE` and `AWS_PROFILE` according to the environment to be deployed.
1. [Deploy Backend](backend/chalice/api_server/README.md#Deploy)
1. [Deploy Cloudfront-invalidator](backend/chalice/cloudfront_invalidator/README.md#Deploy)
1. [Deploy Frontend](frontend/README.md#Deployment)

### Running unittests

1. Set `AWS_PROFILE`
1. Run the tests `$ make unit-test`

### Running functional tests

1. Set `DEPLOYMENT_STAGE` and `AWS_PROFILE` according to the environment to be deployed.
1. In another terminal run `make functional-test`

### Running local functional tests

1. Set `DEPLOYMENT_STAGE` and `AWS_PROFILE` according to the environment to be deployed.
1. Run `make local-database` to setup and populate a locally hosted database.
1. Run `make local-backend` to setup the api on a locally.
1. In another terminal run `make functional-test`
