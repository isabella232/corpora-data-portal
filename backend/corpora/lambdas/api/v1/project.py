from flask import make_response, jsonify

from ....common.utils.exceptions import ForbiddenHTTPException
from ....common.entities import Project


def get_projects_list(user_uuid: str = "", from_date: int = None, to_date: int = None):
    result = dict(projects=Project.list_projects_in_time_range(from_date=from_date, to_date=to_date))
    if from_date:
        result["from_date"] = from_date
    if to_date:
        result["to_date"] = to_date
    return make_response(jsonify(result), 200)


def get_project_details(project_uuid: str):
    project = Project.get_project(project_uuid)
    if project:
        result = project.reshape_for_api()
        return make_response(jsonify(result), 200)
    else:
        raise ForbiddenHTTPException()


def delete_project(path_project_uuid: str):
    raise NotImplementedError


def get_project_dataset(path_dataset_uuid: str):
    raise NotImplementedError
