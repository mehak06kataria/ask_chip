from __future__ import absolute_import

from datetime import date, datetime
from decimal import Decimal

from ask_chip.constants.slack_constants import CHIP_SPAM_TESTING_CHANNEL_ID
from common.tests.test_utils import make_test_apps
from ask_chip.applications.slack_operations import SlackOperations

from tests.clean_db import RPOptimizedTestCase


class TestSlackOperations(RPOptimizedTestCase):
    def setUp(self):
        super(TestSlackOperations, self).setUp()
        self.slack_operations = SlackOperations()

    def test_slack_search(self):
        results = self.slack_operations.search_text(query='funding round')
        self.assertTrue(len(results) >= 3)

    def test_slack_post(self):
        result = self.slack_operations.post_message_to_channel(CHIP_SPAM_TESTING_CHANNEL_ID,"Bumping up!")
        self.assertEqual(True, result)
