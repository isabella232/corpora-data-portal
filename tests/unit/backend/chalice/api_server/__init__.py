import os

from tests.unit.backend.chalice import ChaliceTestHarness

os.environ["APP_NAME"] = "corpora-api"


class BaseAPITest:
    """
    Provide access to the a Chalice app hosting the Corpora API. All test for the Corpora API should inherit this class.
    """

    @classmethod
    def setUpClass(cls):
        corpora_api_dir = os.path.join(os.environ["CORPORA_HOME"], "backend", "chalice", "api_server")
        cls.app = ChaliceTestHarness(corpora_api_dir)
        cls.maxDiff = None  # Easier to compare json responses.

    @staticmethod
    def remove_timestamps(body: dict) -> dict:
        """
        A helper function to remove timestamps from the response body.
        :param body: The decoded json response body
        :return: The decode json response body with timestamps removed.
        
        >>> base = BaseAPITest()
        >>> test_body = {"created_at": "123", "updated_at":123,"list": [{"created_at": 1234, "updated_at", 1234}], "dict1": {"created_at":123, "update_at":1234}}
        >>> result = base.remove_timestamps(test_body)
        >>> assert result == {'list1':[],"dict1":{}}
        """

        def _remove_timestamps(jrb):
            jrb.pop("created_at", None)
            jrb.pop("updated_at", None)
            for value in jrb.values():
                if isinstance(value, dict):
                    _remove_timestamps(value)
                elif isinstance(value, list):
                    for list_value in value:
                        _remove_timestamps(list_value)
            return jrb

        return _remove_timestamps(body)
