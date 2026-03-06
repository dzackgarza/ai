# SPDX-License-Identifier: AGPL-3.0-or-later
"""
 zbMATH Open (Science)
"""

from json import loads
from urllib.parse import urlencode

# about
about = {
    "website": 'https://zbmath.org',
    "wikidata_id": 'Q2510606',
    "official_api_documentation": 'https://api.zbmath.org/v1/',
    "use_official_api": True,
    "require_api_key": False,
    "results": 'JSON',
}

# engine dependent config
categories = ['science']
paging = True

# search-url
search_url = 'https://api.zbmath.org/v1/document/_search?{query}'  # noqa

# engine dependent config
page_size = 10


# do search-request
def request(query, params):
    params['url'] = search_url.format(query=urlencode({
        'search_string': query,
        'results_per_page': page_size,
        'page': params['pageno'] - 1,
    }))

    return params


# get response from search-request
def response(resp):
    results = []

    search_res = loads(resp.text)

    # check if results are received
    if 'result' not in search_res:
        return results

    documents = search_res['result']

    for doc in documents:
        title = doc['title']['title']
        if doc['title'].get('subtitle'):
            title += ': ' + doc['title']['subtitle']

        authors = [a['name'] for a in doc['contributors']['authors'][:3]]
        author_str = ', '.join(authors)
        if len(doc['contributors']['authors']) > 3:
            author_str += ' et al.'

        year = doc['year']
        source = doc['source']['source']

        content = '{} ({})'.format(author_str, year)
        if source:
            content += '. ' + source

        results.append({
            'url': doc['zbmath_url'],
            'title': title,
            'content': content,
        })

    return results
