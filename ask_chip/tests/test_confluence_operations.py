from __future__ import absolute_import

from decimal import Decimal

from ask_chip.applications.confluence_operations import ConfluenceOperations

from tests.clean_db import RPOptimizedTestCase


class TestConfluenceOperations(RPOptimizedTestCase):
    def setUp(self):
        super(TestConfluenceOperations, self).setUp()

    def test_confluence_search(self):
        confluence_operations = ConfluenceOperations()
        results = confluence_operations.search_text('ETA', only_header=False, _type=['blogpost', 'page'])
        self.assertTrue(len(results) > 5)
