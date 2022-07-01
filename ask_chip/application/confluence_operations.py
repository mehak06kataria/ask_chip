import requests
import json
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import os


class ConfluenceOperations:
    def __init__(self):
        self.auth = HTTPBasicAuth(os.environ.get('CONFLUENCE_USER_ID'), os.environ.get('CONFLUENCE_USER_TOKEN'))

    def get_document_description(self, doc_id):
        description = ''
        api_url = 'https://rippling.atlassian.net/wiki/rest/api/content/{}?expand=body.storage'.format(doc_id)

        api_call_response = requests.get(url=api_url, auth=self.auth, verify=False)

        response_text = api_call_response.text

        if api_call_response.status_code != 200:
            return description

        data = json.loads(response_text)
        html_content = data["body"]["storage"]["value"]

        content = BeautifulSoup(html_content, "lxml").text
        return content

    def search_text(self, query, only_header=False, _type=None, _search=True):
        results = []
        if not _search:
            return results
        if query is None or query == '':
            return results
        api_url = 'https://rippling.atlassian.net/wiki/rest/api/content/search'
        if only_header:
            api_url += ('?cql=title~\"{}\"'.format(query))
        else:
            api_url += ('?cql=text~\"{}\"'.format(query))
        if _type:
            types=[]
            # Search and take input via if conditions to prevent cql injection and to query only supported/intended types
            if 'blogpost' in _type:
                types.append('blogpost')
            if 'page' in _type:
                types.append('page')
            if 'comment' in _type:
                types.append('comment')
            if 'attachment' in _type:
                types.append('attachment')
            type_list = ', '.join(types)
            api_url += ('AND type IN ({})'.format(type_list))
        '''
        SOME SEARCH FILTER FORMATS THAT CAN ALSO BE USED :
        space.title ~ "Development Team"    ?cql=space="eng"
        text ~ Confluence         ?cql=text~"eng"
        title ~ "Searching CQL"    ?cql=title~"eng"
        type IN (blogpost, page, comment, attachment) ?cql=...
        type = page      ?cql=...
        type IN (blogpost, page)  ?cql=...
        '''
        api_call_response = requests.get(url=api_url, auth=self.auth, verify=False)

        response_text = api_call_response.text

        if api_call_response.status_code != 200:
            return results

        data = json.loads(response_text)
        search_results = data['results']
        total_matching_messages = len(search_results)
        if total_matching_messages == 0:
            return results
        elif total_matching_messages > 10:
            search_results = search_results[:10]

        matching_texts = []
        for result in search_results:
            doc_id = result['id']
            doc_title = result['title']
            doc_link = 'https://rippling.atlassian.net/wiki{}'.format(result['_links']['webui'])
            mssg_description = doc_title
            if not only_header:
                mssg_description = self.get_document_description(doc_id)
            matching_texts.append({'content': mssg_description, 'link': doc_link})
            # print(doc_id, doc_title, doc_link)

        return matching_texts
