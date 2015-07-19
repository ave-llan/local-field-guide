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



### Example Usage

Let's create a new Field Guide for Shoreline Park at Mountain View and add a few species.



- Log in with Google or Facebook.



- Click 'Create a Field Guide' at the top of the main page and input the following:

Name: `Shoreline Park`

Longitude: `-122.086549`

Latitude: `37.434430`



- Add Some Species. If the species is already in another field guide, you can just select it from the drop down list.


From the species list, select `Black-crowned Night-Heron`

As a tip: `Look in the trees near the water.`



- Add a Species to the database if it is not already in another field guide.

Select 'Add a new species'

Species Common Name: `American White Pelican`
Scientific name: `Pelecanus erythrorhynchos`

Then, add the species to the field guide as in step 3. 


### API

On any field guide page, add `/json` to the url for an api endpoint which will return a json.

For example: `http://localhost:5000/place/2/json`


### Thanks to

Species Photos: [Flickr](https://www.flickr.com/)

Species Descriptions: [Wikipedia](https://www.wikipedia.org/)

Maps: [Mapbox](https://www.mapbox.com/about/maps/) and [OpenStreetMap](http://www.openstreetmap.org)

