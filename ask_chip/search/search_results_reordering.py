from decimal import Decimal

from ask_chip.search.score_calculator import ScoreWordContext
from ask_chip.utils import get_summarized_text


class SearchResultsUpdater:
    def __init__(self, query_sentence):
        self.query_words = query_sentence
        self.ordered_contexts = []
        # self.context = self.getContextList(all_context_links)

    def get_ordered_contexts(self, slack_contexts, drive_contexts, confluence_contexts):
        '''INPUT :
        3 x list of {
          'content' : ,
          'link' : ,
        }
        OUTPUT :
        list of {
          'content' : ,
          'link' : ,
          'type' : ,
        }'''
        ordered_contexts = []
        slack_index = 0
        drive_index = 0
        confluence_index = 0
        remaining_runs = len(slack_contexts) + len(drive_contexts) + len(confluence_contexts)

        while (slack_index < len(slack_contexts) or drive_index < len(drive_contexts) or confluence_index < len(
                confluence_contexts)):
            # print(slack_index, drive_index, confluence_index)
            slack_top = {'content': None, 'link': None}
            drive_top = {'content': None, 'link': None}
            confluence_top = {'content': None, 'link': None}

            if slack_index < len(slack_contexts):
                slack_top = slack_contexts[slack_index]
            if drive_index < len(drive_contexts):
                drive_top = drive_contexts[drive_index]
            if confluence_index < len(confluence_contexts):
                confluence_top = confluence_contexts[confluence_index]
            best_result = self.get_best_result(slack_top['content'], drive_top['content'], confluence_top['content'])
            if best_result is None:
                break
            if best_result['type'] == 'slack':
                slack_index += 1
                summary = get_summarized_text(slack_top)
                ordered_contexts.append({
                    'content': summary,
                    'link': slack_top['link'],
                    'type': best_result['type']
                })
            elif best_result['type'] == 'drive':
                drive_index += 1
                summary = get_summarized_text(drive_top)
                ordered_contexts.append({
                    'content': summary,
                    'link': drive_top['link'],
                    'type': best_result['type']
                })
            elif best_result['type'] == 'confluence':
                confluence_index += 1
                summary = get_summarized_text(confluence_top)
                ordered_contexts.append({
                    'content': summary,
                    'link': confluence_top['link'],
                    'type': best_result['type']
                })
            else:
                break
            remaining_runs -= 1
            if remaining_runs == 0:
                return ordered_contexts # To avoid infinite loop - For safety

        self.ordered_contexts = ordered_contexts
        return ordered_contexts

    def get_best_result(self, slack_text, drive_text, confluence_text):
        '''INPUT
        3 x str
        OUTPUT
        {
          'type' : ,
          'match' : ,
          'score' : ,
        }'''
        matching_slack, similarity_slack_score = ScoreWordContext(self.query_words, slack_text).get_matching_score()
        matching_drive, similarity_drive_score = ScoreWordContext(self.query_words, drive_text).get_matching_score()
        matching_confluence, similarity_confluence_score = ScoreWordContext(self.query_words,
                                                                                 confluence_text).get_matching_score()

        matching_lis = []
        if slack_text is not None:
            matching_lis.append({
                'type': 'slack',
                'match': matching_slack,
                'score': similarity_slack_score
            })
        if drive_text is not None:
            matching_lis.append({
                'type': 'drive',
                'match': matching_drive,
                'score': similarity_drive_score
            })

        if confluence_text is not None:
            matching_lis.append({
                'type': 'confluence',
                'match': matching_confluence,
                'score': similarity_confluence_score
            })
        matching_lis = sorted(matching_lis, key=lambda k: (-1 * k['match'], -1 * k['score']))
        return matching_lis[0] if len(matching_lis)>0 else None
