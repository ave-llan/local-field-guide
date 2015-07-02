"""
Looks up summaries on Wikipedia related to a given query string. 
"""

import requests, json


def search(search_terms, numSentences=2):
    """Returns a Wikipedia object, or None if no results 
    """

    wikiEndpoint = 'https://en.wikipedia.org/w/api.php'
    parameters = {
        'format'         : 'json',
        'action'         : 'query',
        'prop'           : 'extracts',
        'exintro'        : '',
        'explaintext'    : '', 
        'redirects'      : '',
        'exsectionformat': 'plain',
        'exsentences'    : numSentences,
        'titles'         : search_terms
    }
    r = requests.get(wikiEndpoint, params=parameters).json()
    # get pageid id so we can get the page content. It is the first key.
    key = r['query']['pages'].keys()[0]
    # if key is -1, no results were found
    if int(key) == -1:
        return None
    return r['query']['pages'][key]['extract'] 


def articleUrl(search_terms):
    """Returns a link to a Wikipedia article, or None if no results
    """
    wikiEndpoint = 'https://en.wikipedia.org/w/api.php'
    parameters = {
        'format'         : 'json',
        'action'         : 'query',
        'titles'         : search_terms
    }
    r = requests.get(wikiEndpoint, params=parameters).json()
    # get pageid id so we can get the page content. It is the first key.
    key = r['query']['pages'].keys()[0]
    # if key is -1, no results were found
    if int(key) == -1:
        return None
    return 'http://en.wikipedia.org/wiki/' + r['query']['pages'][key]['title']
    
