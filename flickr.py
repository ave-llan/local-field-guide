"""
Looks up photos on Flickr related to a given query string. 
Formats Flickr's results into working links to the photo itself
and the url of the Flickr photo page. 
"""

import requests, json

# grab the api-key from the secrets file
flickr_api_key = json.loads(
    open('/var/www/fieldguideApp/FlaskApp/secrets.json', 'r').read())['flickr']

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


def addSizeSuffix(photoUrl, size_suffix):
    """ Changes the photo url to use a Flickr size size_suffix

    size_suffix args:
        s   small square 75x75
        q   large square 150x150
        t   thumbnail, 100 on longest side
        m   small, 240 on longest side
        n   small, 320 on longest side
        -   medium, 500 on longest side
        z   medium 640, 640 on longest side
        c   medium 800, 800 on longest side
        b   large, 1024 on longest side
        h   large 1600, 1600 on longest side
        k   large 2048, 2048 on longest side
        o   original image, either a jpg, gif or png, depending on source format
    """
    # change photo ending from .jpg to _{size_suffix}.jpg
    return photoUrl[:-4] + '_' + size_suffix + '.jpg'


