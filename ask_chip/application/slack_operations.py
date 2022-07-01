import requests
import json
import os

from ask_chip.constants.slack_constants import RIPPLING_WHITELIST_CHANNELS


class SlackOperations:
    def __init__(self):
        self.read_access_token = os.environ.get('SLACK_READ_OAUTH_TOKEN')
        self.write_access_token = os.environ.get('SLACK_WRITE_OAUTH_TOKEN')

    @staticmethod
    def is_channel(response):
        return response["channel"]["is_channel"]

    @staticmethod
    def is_group(response):
        return response["channel"]["is_group"]

    @staticmethod
    def is_public_channel(response):
        return SlackOperations.is_channel(response) and (response["channel"]["is_private"]==False)

    @staticmethod
    def is_private_channel(response):
        return SlackOperations.is_channel(response) and response["channel"]["is_private"]

    @staticmethod
    def is_dm(response):
        return "user" in response["channel"].keys()

    def search_text(self, query, team_id=None, count=None, channels=True, public_channels=True, private_channels=False, dms=False,
                    groups=False, channel_ids=None, group_ids=None, page=None, pretty='1', _search=True):

        results = []
        if not _search:
            return results
        if query is None or query == '':
            return results
        api_url = 'https://slack.com/api/search.messages'
        api_url += ('?query=' + query)
        if team_id:
            api_url += ('&team_id=' + team_id)
        if count:
            api_url += ('&count=' + count)
        if page:
            api_url += ('&page=' + page)
        if pretty:
            api_url += ('&pretty=' + pretty)
        try:
            api_call_headers = {'Authorization': 'Bearer ' + self.read_access_token}
            api_call_response = requests.get(url=api_url, headers=api_call_headers, verify=False)
        except:
            return results
        response_text = api_call_response.text

        if api_call_response.status_code != 200:
            return results

        data = json.loads(response_text)

        total_matching_messages = int(data['messages']['total'])
        if total_matching_messages == 0:
            return results

        def get_dec_link(match):
            mssg_description = match['text']
            redirect_link = match['permalink']
            return {'content': mssg_description, 'link': redirect_link}

        matching_texts = []
        for match in data['messages']['matches']:
            if channels is True and SlackOperations.is_channel(match):
                if channel_ids is not None and len(channel_ids) > 0:
                    if match['channel']['id'] in channel_ids:
                        matching_texts.append(get_dec_link(match))
                        continue
                else:
                    if public_channels is True and SlackOperations.is_public_channel(match):
                        matching_texts.append(get_dec_link(match))
                    elif private_channels is True and not SlackOperations.is_private_channel(match):
                        matching_texts.append(get_dec_link(match))

            if groups is True and SlackOperations.is_group(match):
                if group_ids is not None and len(group_ids) > 0:
                    if match['channel']['id'] in group_ids:
                        matching_texts.append(get_dec_link(match))
                        continue
                else:
                    matching_texts.append(get_dec_link(match))

            if dms is True and SlackOperations.is_dm(match):
                matching_texts.append(get_dec_link(match))


            # # #FOR DEMO - WHITELISTING SOME CHANNELS RESULTS ONLY TO AVOID PERSONAL INFO LEAK
            # # if not SlackOperations.is_channel(match) or match["channel"]["id"] not in RIPPLING_WHITELIST_CHANNELS:
            # #     continue
            # # FOR DEMO - SHOWING ONLY PUBLIC CHANNEL RESULT TO AVOID PERSONAL INFO LEAK
            # if not SlackOperations.is_public_channel(match):
            #     continue
        if len(matching_texts) > 10:
            matching_texts = matching_texts[:10]
        return matching_texts

    def post_message_to_channel(self, channel_id, message, pretty='1'):
        if message is None or message == "":
            return False
        if channel_id is None or channel_id == "":
            return False
        try:
            api_url = "https://slack.com/api/chat.postMessage"
            api_url += ('?channel=' + channel_id)
            api_url += ('&text=' + message)
            if pretty:
                api_url += ('&pretty=' + pretty)
            api_call_headers = {'Authorization': 'Bearer ' + self.write_access_token}
            api_call_response = requests.post(api_url, headers=api_call_headers, verify=False)
        except:
            return False
        if api_call_response.status_code != 200:
            return False
        return True
