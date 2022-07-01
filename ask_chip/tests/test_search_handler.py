from __future__ import absolute_import

from ask_chip.search.search_handler import SearchHandler

from ask_chip.applications.confluence_operations import ConfluenceOperations

from ask_chip.applications.drive_operations import DriveOperations

from ask_chip.applications.slack_operations import SlackOperations

from ask_chip.constants.sample_results import SAMPLE_CONFLUENCE_SEARCH_OUTPUT, SAMPLE_DRIVE_SEARCH_OUTPUT, SAMPLE_SLACK_SEARCH_OUTPUT
from ask_chip.search.search_results_reordering import SearchResultsUpdater

from tests.clean_db import RPOptimizedTestCase


class TestSearchHandler(RPOptimizedTestCase):
    def setUp(self):
        super(TestSearchHandler, self).setUp()

    def test_search_handler(self):
        # query = 'Our team ETA support sessioned dashboard suddenly became inaccessible (happened ~ a week ago). Is any other team facing the same issue?'
        query = 'recruit marshall'
        query_type = 'query_type'
        query_subtype = 'query_subtype'

        is_error = False
        conf_config = {
            'search' : True,
            'only_header' : False,
            '_type' : ['page', 'blogpost']  # blogpost, page, comment, attachment only supported
        }
        drive_config = {
            'search' : True,
            'only_header' : False,
            '_type' : 'doc'  # doc, sheet
        }
        slack_config = {
            'search' : True,
            'public_channels' : True,
            'private_channels' : False,
            'dms' : False,
            'groups' : False,
            'channel_ids' : None,
            'group_ids' : None
        }

        arranged_results = SearchHandler(query,query_type,query_subtype,None).get_result(is_error, conf_config, drive_config, slack_config)
        for result in arranged_results:
            print(result['link'])
        self.assertTrue(len(arranged_results) > 0)
