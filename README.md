# Local Field Guide
Create and view little field guides. When given a species name, the app automatically creates a species card by looking up a picture from Flickr and a description from Wikipedia. 


### Requirements

Python >2.7 and <3.0.

[SQLAlchemy](http://www.sqlalchemy.org/)

[Flask](http://flask.pocoo.org/)

[jQuery](https://jquery.com/)

[oathu2client](https://pypi.python.org/pypi/oauth2client)




### Set up

Clone the repository:

`git clone https://github.com/jrleszcz/swiss-tournament.git`


Populate the app with field guides in the `initial-field-guides` directory. This may take a minute as the program looks up descriptions from Wikipedia and photos from Flickr. 

`python initial_data.py`


Launch the server:

`python field_guide_server.py`


Visit `localhost:5000` in the browser to see the site.



### Usage

Log in with Google or Facebook to create a field guide and edit field guides that you own. 


### Thanks to

Species Photos: [Flickr](https://www.flickr.com/)

Species Descriptions: [Wikipedia](https://www.wikipedia.org/)

Maps: [Mapbox](https://www.mapbox.com/about/maps/) and [OpenStreetMap](http://www.openstreetmap.org)

