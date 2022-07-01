from __future__ import absolute_import
from common.api_base import ApiInterface
from ask_chip.search.search_handler import SearchHandler

class ChipBot(ApiInterface):
    def __init__(self, user_id):
        self.user_id = user_id

    # GET combine get_confluence_result and get_slack_result
    def search_result(self, query, query_type, query_subtype):
        """if query_state == "NEW" or query_state == "NO FIX YET":
            post_query_slack(query, query_type)
        else:"""
        search_handler = SearchHandler(query, query_type, query_subtype)
        search_result = search_handler.get_result()
        return search_result

    # if query_state == NEW or DOESN'T EXIST
    # POST req to post query in slack
    def post_query_slack(self, query, query_type):
        '''
        channel_id = ... # Appropriate chennel id from slack_constants.py as per query type
        result = SlackOperations().post_message_to_channel(channel_id, query)
        '''
        pass

    # Not necessaary function
    # if user is new then add it to DB
    def add_user_to_DB(self, user_id):
        pass
