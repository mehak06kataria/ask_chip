from ask_chip.applications.confluence_operations import ConfluenceOperations

from ask_chip.applications.drive_operations import DriveOperations

from ask_chip.applications.slack_operations import SlackOperations

from ask_chip.search.search_results_reordering import SearchResultsUpdater
from ask_chip.utils import preprocess_query


class SearchHandler:
    def __init__(self, query, query_type, query_subtype, search_in):
        self.query = query
        self.query_type = query_type
        self.query_subtype = query_subtype
        self.search_in = search_in

    def get_result(self, is_error=False, conf_search={}, drive_search={}, slack_search={}):
        if is_error:
            self.query =  preprocess_query(self.query)
        try:
            _search = slack_search.get('search', True)
            pub_ch = slack_search.get('public_channels', True)
            pri_ch = slack_search.get('private_channels', False)
            dms = slack_search.get('dms', False)
            groups = slack_search.get('groups', False)
            channel_ids = slack_search.get('channel_ids', None)
            group_ids = slack_search.get('group_ids', None)

            slack_results = SlackOperations().search_text(query=self.query, public_channels=pub_ch, private_channels=pri_ch,
                                        dms=dms, groups=groups, channel_ids=channel_ids, group_ids=group_ids, _search=_search)

            _search = drive_search.get('search', True)
            only_header = drive_search.get('only_header', False)
            _type = drive_search.get('_type', None)
            drive_results = DriveOperations().search_text(self.query, only_header, _type, _search)

            _search = conf_search.get('search', True)
            only_header = conf_search.get('only_header', False)
            _type = conf_search.get('_type', None)
            confluence_results = ConfluenceOperations().search_text(self.query, only_header, _type, _search)

            arranged_results = SearchResultsUpdater(self.query).get_ordered_contexts(slack_results, drive_results, confluence_results)
            return arranged_results
        except:
            pass
        return []
