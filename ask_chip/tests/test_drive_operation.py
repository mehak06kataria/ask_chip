from __future__ import absolute_import

from ask_chip.applications.drive_operations import DriveOperations

from tests.clean_db import RPOptimizedTestCase


class TestDriveOperations(RPOptimizedTestCase):
    def setUp(self):
        super(TestDriveOperations, self).setUp()
        self.drive_operations = DriveOperations()

    def test_drive_search(self):
        results = self.drive_operations.search_text(query='Hack Day')
        self.assertTrue(len(results) > 0)
