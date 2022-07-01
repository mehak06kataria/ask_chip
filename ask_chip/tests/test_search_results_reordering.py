from __future__ import absolute_import




from ask_chip.constants.sample_results import SAMPLE_CONFLUENCE_SEARCH_OUTPUT, SAMPLE_DRIVE_SEARCH_OUTPUT, SAMPLE_SLACK_SEARCH_OUTPUT

from ask_chip.search.search_results_reordering import SearchResultsUpdater




from tests.clean_db import RPOptimizedTestCase







class TestSearchReordering(RPOptimizedTestCase):

    def setUp(self):

        super(TestSearchReordering, self).setUp()




    def check_not_missing(self, results, search_inputs):

        result_links = set((result['link'] for result in results))

        for search_input in search_inputs:

            if search_input['link'] not in result_links:

                return False

        return True




    def test_search_results_reordering(self):

        search_results = SearchResultsUpdater('games session')

        arranged_results = search_results.get_ordered_contexts(SAMPLE_SLACK_SEARCH_OUTPUT, SAMPLE_DRIVE_SEARCH_OUTPUT, SAMPLE_CONFLUENCE_SEARCH_OUTPUT)

        self.assertEqual(len(arranged_results), len(SAMPLE_SLACK_SEARCH_OUTPUT)+len(SAMPLE_DRIVE_SEARCH_OUTPUT)+len(SAMPLE_CONFLUENCE_SEARCH_OUTPUT))

        self.assertEqual(True, self.check_not_missing(arranged_results, SAMPLE_SLACK_SEARCH_OUTPUT))

        self.assertEqual(True, self.check_not_missing(arranged_results, SAMPLE_DRIVE_SEARCH_OUTPUT))

        self.assertEqual(True, self.check_not_missing(arranged_results, SAMPLE_CONFLUENCE_SEARCH_OUTPUT))
