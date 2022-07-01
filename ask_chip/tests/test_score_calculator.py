from __future__ import absolute_import

from datetime import date, datetime
from decimal import Decimal

from ask_chip.search.score_calculator import ScoreWordContext
from common.tests.test_utils import make_test_apps

from tests.clean_db import RPOptimizedTestCase


class TestScoreCalculator(RPOptimizedTestCase):
    def setUp(self):
        super(TestScoreCalculator, self).setUp()
        self.context1 = 'This is the first game context, when we played chess'
        self.context2 = 'This is the second game context, where we had sessions discussing the ' \
                        'football game played between Arsenal and Man United'

    def test_score_calculator(self):
        query = 'games play'
        score_calculator = ScoreWordContext(query, self.context1)
        mathing_length, score = score_calculator.get_matching_score()
        self.assertTrue(score>Decimal('0.0'))
        score_calculator = ScoreWordContext(query, self.context2)
        mathing_length, score = score_calculator.get_matching_score()
        self.assertEqual(14, mathing_length)
