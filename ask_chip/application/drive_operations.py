import requests
import json
import os

from ask_chip.constants.drive_constants import DRIVE_DOC_MIMETYPE, DRIVE_SHEET_MIMETYPE, FOLDER_MIME_TYPE


class DriveOperations:
    def __init__(self):
        self.access_token = os.environ.get('DRIVE_OAUTH_TOKEN')

    def get_document_description(self, title, file_id):
        description = title
        description += ' '
        api_url = 'https://docs.googleapis.com/v1/documents/{}'.format(file_id)

        api_call_headers = {'Authorization': 'Bearer ' + self.access_token}
        api_call_response = requests.get(url=api_url, headers=api_call_headers, verify=False)

        response_text = api_call_response.text

        if api_call_response.status_code != 200:
            return description
        data = json.loads(response_text)

        contents = data['body']['content']

        locked = True
        for content in contents:
            if 'paragraph' in content:
                para_content = content['paragraph']
                for _element in para_content['elements']:
                    locked = False
                    if 'textRun' in _element:
                        description += _element['textRun']['content']
                        description += ' '

        return description, locked

    def get_sheet_description(self, title, file_id):
        description = title
        description += ' '
        api_url = 'https://sheets.googleapis.com/v4/spreadsheets/{}/values:batchGet?ranges=A1:Z100'.format(file_id)

        api_call_headers = {'Authorization': 'Bearer ' + self.access_token}
        api_call_response = requests.get(url=api_url, headers=api_call_headers, verify=False)

        response_text = api_call_response.text

        if api_call_response.status_code != 200:
            return description
        data = json.loads(response_text)

        value_ranges = data['valueRanges']
        locked = True
        for value_range in value_ranges:
            all_values = value_range["values"]
            locked = False
            for each_value in all_values:
                description += " ".join([text for text in each_value])
        return description, locked

    def search_text(self, query, only_header=False, search_type=None, _search=True):
        results = []
        if not _search:
            return results
        if query is None or query == '':
            return results
        api_url = 'https://www.googleapis.com/drive/v3/files'

        '''
        If we want to integrate token wise search as well, refer below: 
        -> CONS : Gives a lot of irrelevant results, though of lower score
        # tokens = query.split()
        # fulltext_search_query = ' OR '.join('fullText contains \'' + str(token) + '\'' for token in tokens)
        # name_search_query = ' OR '.join('name contains \'' + str(token) + '\'' for token in tokens)
        # name_search_query = 'name contains {} OR ' + name_search_query
        # header_query = 'mimeType != {} and {}'.format(FOLDER_MIME_TYPE, fulltext_search_query)
        '''
        fulltext_search_query = 'q=fullText contains \'{}\''.format(query)
        name_search_query = 'q=name contains \'{}\''.format(query)
        search_query = 'mimeType != \'{}\'&{}'.format(FOLDER_MIME_TYPE, fulltext_search_query)
        if only_header:
            search_query = 'mimeType != \'{}\'&{}'.format(FOLDER_MIME_TYPE, name_search_query)
        api_url += '?{}'.format(search_query)

        api_call_headers = {'Authorization': 'Bearer ' + self.access_token}
        api_call_response = requests.get(url=api_url, headers=api_call_headers, verify=False)

        response_text = api_call_response.text

        if api_call_response.status_code != 200:
            return results

        data = json.loads(response_text)

        search_results = data['files']
        total_matching_messages = len(search_results)
        if total_matching_messages == 0:
            return results
        # elif total_matching_messages > 10:
        #     search_results = search_results[:10]

        matching_texts = []
        for result in search_results:
            if result["mimeType"] not in [DRIVE_SHEET_MIMETYPE, DRIVE_DOC_MIMETYPE]:
                continue
            _type = 'doc' if result["mimeType"] == DRIVE_DOC_MIMETYPE else 'sheet'
            file_id = result['id']
            mssg_title = result['name']
            _file_link = None
            if _type == 'doc':
                _file_link = 'https://docs.google.com/document/d/{}/'.format(file_id)
            else:
                _file_link = 'https://docs.google.com/spreadsheets/d/{}/'.format(file_id)
            mssg_description = mssg_title
            locked = True
            if not only_header:
                if _type == 'doc':
                    mssg_description, locked = self.get_document_description(mssg_title, file_id)
                else:
                    mssg_description, locked = self.get_sheet_description(mssg_title, file_id)
            if not locked:
                matching_texts.append({'content': mssg_description, 'link': _file_link})
            # print(file_id, mssg_title, mssg_description)

        return matching_texts
