"""
Looks up photos on Flickr related to a given query string. 
Formats Flickr's results into working links to the photo itself
and the url of the Flickr photo page. 
"""

import requests, json

# grab the api-key from another file
flickr_api_key = json.loads(
    open('api-keys.json', 'r').read())['flickr']


def search(search_terms, numResults=1):
    """Returns a a list of Flickr photo objects, or None if no results 
    """

    flickrEndpoint = 'https://api.flickr.com/services/rest/'
    parameters = {
        'api_key' : flickr_api_key,
        'method'  : 'flickr.photos.search',
        'sort'    : 'relevance',
        'per_page': numResults,
        # exclude only license 0 -- which is All Rights Reserved 
        'license': '1,2,3,4,5,6,7,8,9,10', 
        'format'  : 'json',
        'nojsoncallback': 1,
        'text': search_terms
    }
    r = requests.get(flickrEndpoint, params=parameters).json()
    if len(r['photos']['photo']) == 0:
        return None
    return r['photos']['photo']


def photoUrl(flickr_photo_object):
    """Builds a url for a photo from a Flickr photo object
    """
    url = 'https://farm{farm}.staticflickr.com/{server}/{id}_{secret}.jpg'.format(
            farm = flickr_photo_object['farm'],
            server = flickr_photo_object['server'],
            id = flickr_photo_object['id'],
            secret = flickr_photo_object['secret'])
    return url


def photoPageUrl(flickr_photo_object):
    """Builds the url for this photos page on Flickr from a Flickr photo object
    """
    url = 'https://www.flickr.com/photos/{owner}/{id}'.format(
            owner = flickr_photo_object['owner'],
            id = flickr_photo_object['id'])
    return url

