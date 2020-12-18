from tests.unit.fixtures.test_db import TestDatabaseManager

class DataPortalTestCase(unittest.TestCase):

    def setUp(self):
        TestDatabaseManager.initialize_db()

    def tearDown(self):
        pass
