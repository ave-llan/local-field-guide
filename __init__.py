from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

## import CRUD Operations ##
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, UserProfile, Place, Species, SpeciesOccurrence
from database_setup import engine

# Imports for oAuth
from flask import session as login_session
from flask import make_response
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests


# on virtualenv this should be set to '/var/www/fieldguideApp/FlaskApp/'
# if files will be in the same directory, use an empty string
PATH_TO_FILE = ""

# Imports for populating species information
import flickr, wikipedia

CLIENT_ID = json.loads(
    open(PATH_TO_FILE + 'client_secrets.json', 'r').read())['web']['client_id']


# Create session and connect to DB
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



# home page
@app.route('/')
def homePage():
    print 'logged in as:'
    print login_session.get('username')
    places = session.query(Place).all()

    # build dictionary with photo urls for last six species added for each place 
    # to be used as preview thumbnails
    numThumbnails = 9
    speciesAtPlace = {}
    for place in places:
        speciesAtPlace[place.id] = session.query(
            SpeciesOccurrence).filter_by(
            place_id = place.id).order_by(
            desc(SpeciesOccurrence.species_id)).all()[:numThumbnails]
        for i in range(len(speciesAtPlace[place.id])):
            species = speciesAtPlace[place.id][i].species
            # this requests a smaller (150x150) version of the photo from Flickr
            photoUrl = flickr.addSizeSuffix(species.photo, 'q')
            speciesAtPlace[place.id][i] = {
                    'common_name': species.common_name,
                    'photo': photoUrl}
    return render_template('index.html', places = places,
                        speciesAtPlace = speciesAtPlace, login_session = login_session)


# Page for individual field guides
@app.route('/place/<int:place_id>/')
def placeFieldGuide(place_id):
    place = session.query(Place).filter_by(id=place_id).one()
    occurrences = session.query(SpeciesOccurrence).\
                    filter_by(place_id = place_id).\
                    all()
    authorInitials = "".join([i[0] for i in place.userprofile.name.split()])
    return render_template('place.html', place = place, 
                        occurrences = occurrences,
                        authorInitials = authorInitials,
                        login_session = login_session)


@app.route('/place/create/', methods=['GET', 'POST'])
def createPlace():
    if 'username' not in login_session:
        flash("Please login to create a new field guide.")
        return redirect('/login')
    if request.method == 'POST':
        newPlace = Place(name = request.form['name'],
                    longitude = request.form['longitude'],
                    latitude = request.form['latitude'],
                    user_id = getUserID(login_session['email']))
        session.add(newPlace)
        session.commit()
        flash("'" + request.form['name'] + "' Field Guide created")
        return redirect(url_for('homePage'))
    else:
        return render_template('newplace.html', login_session = login_session)


# Page to add a species to the database
# TODO make this automatic based on species name
@app.route('/addspecies', methods=['GET', 'POST'])
def addSpecies():
    if 'username' not in login_session:
        flash("Please login to add a new species to the database.")
        return redirect('/login')
    if request.method == 'POST':

        # look up photo on flickr (and select the first item from returned list)
        photo = flickr.search(request.form['scientificName'])[0]

        # look up description from wikipedia
        description = wikipedia.search(request.form['scientificName'])
        wiki_url = wikipedia.articleUrl(request.form['scientificName'])

        newSpecies = Species(common_name = request.form['commonName'],
                    scientific_name = request.form['scientificName'],
                    photo = flickr.photoUrl(photo),
                    photo_page = flickr.photoPageUrl(photo),
                    wiki_url = wiki_url,
                    description = description)
        session.add(newSpecies)
        session.commit()
        flash(request.form['commonName'] + " added to species database")
        return redirect(url_for('homePage'))
    else:
        return render_template('addspecies.html', login_session = login_session)


# Adds a species to a specific Field Guide
@app.route('/place/<int:place_id>/addspeciestoplace/', methods=['GET', 'POST'])
def addSpeciesToPlace(place_id):
    if 'username' not in login_session:
        flash("Please login to add a species to this Field Guide.")
        return redirect('/login')
    # check that this is the owner, if not, redirect
    place = session.query(Place).filter_by(id=place_id).one() 
    if getUserID(login_session['email']) != place.user_id:
        flash("You are not authorized to edit this field guide!")
        return redirect(url_for('placeFieldGuide', place_id=place_id))
    if request.method == 'POST':
        sp = session.query(Species).filter_by(common_name=request.form['species']).one()

        # first check to see if species is already added to this place
        occurrence = session.query(SpeciesOccurrence).filter_by(
            place_id = place_id, species_id = sp.id).scalar()
        if occurrence is not None:
            flash(sp.common_name + " is already in this field guide.")
            return redirect(url_for('placeFieldGuide', place_id=place_id))

        newSpeciesOccurrence = SpeciesOccurrence(place_id = place_id,
                    species_id = sp.id,
                    tip = request.form['tip'])
        session.add(newSpeciesOccurrence)
        session.commit()
        place = session.query(Place).filter_by(id=place_id).one()
        flash(request.form['species'] + " added to " + place.name)
        return redirect(url_for('placeFieldGuide', place_id=place_id))
    else:
        place = session.query(Place).filter_by(id=place_id).one()
        species = session.query(Species).all()
        return render_template('addspeciestoplace.html', place=place, species=species,
                        login_session = login_session)


# Edit the tip about a species in a specific Field Guide
@app.route('/place/<int:place_id>/<int:species_id>/editoccurrence', methods=['GET', 'POST'])
def editSpeciesOccurrence(place_id, species_id):
    if 'username' not in login_session:
        flash("Please login to edit the tips in this Field Guide.")
        return redirect('/login')
    # check that this is the owner, if not, redirect
    place = session.query(Place).filter_by(id=place_id).one() 
    if getUserID(login_session['email']) != place.user_id:
        flash("You are not authorized to edit this field guide!")
        return redirect(url_for('placeFieldGuide', place_id=place_id))
    if request.method == 'POST':
        occurrence = session.query(SpeciesOccurrence).filter_by(place_id=place_id, species_id=species_id).one()
        if request.form['tip']:
            occurrence.tip = request.form['tip']
        session.add(occurrence)
        session.commit()
        flash("Species tip edited")
        return redirect(url_for('placeFieldGuide', place_id=place_id))

    else:
        occurrence = session.query(SpeciesOccurrence).filter_by(place_id=place_id, species_id=species_id).one()
        return render_template('editspeciesoccurrence.html', occurrence=occurrence,
                        login_session = login_session)


# Remove a species from a Field Guide
@app.route('/place/<int:place_id>/<int:species_id>/removeoccurrence', methods=['GET', 'POST'])
def removeOccurrence(place_id, species_id):
    if 'username' not in login_session:
        flash("Please login to remove a species from this Field Guide.")
        return redirect('/login')
    # check that this is the owner, if not, redirect
    place = session.query(Place).filter_by(id=place_id).one() 
    if getUserID(login_session['email']) != place.user_id:
        flash("You are not authorized to edit this field guide!")
        return redirect(url_for('placeFieldGuide', place_id=place_id))
    if request.method == 'POST':
        # validate state to protect against cross-site request forgeries
        if login_session['state'] != request.form['state']:
            flash("State could not be validated, please try again.")
            return redirect(url_for('placeFieldGuide', place_id=place_id))
        occurrence = session.query(SpeciesOccurrence).filter_by(place_id=place_id, species_id=species_id).one()
        session.delete(occurrence)
        session.commit()
        flash("Species occurrence removed")
        return redirect(url_for('placeFieldGuide', place_id=place_id))

    else:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
        login_session['state'] = state
        occurrence = session.query(SpeciesOccurrence).filter_by(place_id=place_id, species_id=species_id).one()
        return render_template('deleteoccurrence.html', occurrence=occurrence, STATE=state,
                        login_session = login_session)

# Delete a Field Gudie
@app.route('/place/<int:place_id>/delete', methods=['GET', 'POST'])
def deleteFieldGuide(place_id):
    if 'username' not in login_session:
        flash("Please login to remove your Field Guide.")
        return redirect('/login')
    # check that this is the owner, if not, redirect
    place = session.query(Place).filter_by(id=place_id).one() 
    if getUserID(login_session['email']) != place.user_id:
        flash("You are not authorized to delete this field guide!")
        return redirect(url_for('placeFieldGuide', place_id=place_id))
    if request.method == 'POST':
        # validate state to protect against cross-site request forgeries
        if login_session['state'] != request.form['state']:
            flash("State could not be validated, please try again.")
            return redirect(url_for('placeFieldGuide', place_id=place_id))
        place_name = place.name
        session.query(SpeciesOccurrence).\
                    filter_by(place_id = place_id).\
                    delete(synchronize_session='fetch')
        session.delete(place)
        session.commit()
        flash('{} field guide deleted.'.format(place_name))
        return redirect(url_for('homePage'))
    else:
        state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
        login_session['state'] = state
        return render_template('deletefieldguide.html', place=place, STATE = state,
                    login_session = login_session)


# API JSON Endpoint
@app.route('/place/<int:place_id>/json')
def placeFieldGuideJSON(place_id):
    place = session.query(Place).filter_by(id=place_id).one()
    occurrences = session.query(SpeciesOccurrence).\
                    filter_by(place_id = place_id).\
                    all()
    return jsonify(
        name=place.name,
        author=place.userprofile.name,
        longitude=place.longitude,
        latitude=place.latitude,
        species=[species.serialize for species in occurrences])



###########################
### login/logout routes ###
###########################

@app.route('/login')
def showLogin():
    # create a 32 charachter state key
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# Try to log a user in using Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # first, check for valid state before proceeding
    if not stateIsValid(request.args.get('state')):
        return loginErrorResponse('Invalid State parameter', 401)

    # next, get the authorization code and try to upgrade it into a credentials object
    authorization_code = request.data
    try:
        # upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(PATH_TO_FILE + 'client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(authorization_code)
    except FlowExchangeError:
        return loginErrorResponse('Failed to upgrade the authorization code.', 401)


    ### Check for possible errors ###
        
    # check that the access token is valid
    access_token = credentials.access_token
    verification_url = 'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token='
    h = httplib2.Http()
    result = json.loads(h.request(verification_url + access_token, 'GET')[1])
    # if there is an error in the access token info, abort.
    if result.get('error') is not None:
        return loginErrorResponse(result.get('error'), 500)

    # verify the access token is for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return loginErrorResponse("Token's user ID does not match given user ID.", 401)

    # verify that the access token is for this app.
    if result['issued_to'] != CLIENT_ID:
        return loginErrorResponse("Token's client ID does not match app's id.", 401)

    # check to see if user is already logged in
    stored_credentials = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        flash_message = 'Hello again, {}.  You were already logged in!'.format(
                login_session['given_name'])
        return loginErrorResponse('Current user is already connected.', 200, flash_message)


    ### Get User Info from Google and store in login_session ###

    # get user info
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    # store in login_session
    login_session['provider'] = 'google'
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    login_session['given_name'] = data['given_name']
    login_session['family_name'] = data['family_name']


    ### check if user exists, if not make a new User ###

    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("Welcome, {}! You are now logged in.".format(login_session['given_name']))
    print "google login successful!"
    return 'Login successful! Redirecting...'


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    # verify state before proceeding
    if not stateIsValid(request.args.get('state')):
        return loginErrorResponse('Invalid State parameter', 401)

    access_token = request.data
    fb_client_secrets = json.loads(open(PATH_TO_FILE + 'fb_client_secrets.json', 'r').read())
    app_id = fb_client_secrets['web']['app_id']
    app_secret = fb_client_secrets['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.2/me?%s' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    print "url sent for API access:%s"% url
    print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    login_session['given_name'] = data['first_name']
    login_session['family_name'] = data['last_name']

    # The token must be stored in the login_session in order to properly logout
    # strip out the information before the equals sign in the token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.2/me/picture?%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if user_id is None:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    flash("Welcome, {}! You are now logged in.".format(login_session['given_name']))
    print "facebook login successful!"
    return 'Login successful! Redirecting...'


# Revokes a current Google user's token and resets their login_session.
@app.route('/gdisconnect')
def gdisconnect():
    # only disconnect a connected user
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    revokeTokenUrl = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(revokeTokenUrl, 'GET')[0]

    if result['status'] == '200':
        response = make_response(
            json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        print 'successfully logged out of google'
        return response

    if result['status'] != '200':
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Revokes a current Facebook user's token and resets their login_session.
@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    print facebook_id
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    print access_token
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)
    print url
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    print result
    return "you have been logged out"


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()
        clearLoginSession(login_session)
        flash("You have successfully been logged out.")
    else:
        flash("You were not logged in")
    return redirect(url_for('homePage'))


#############################
### User Helper Functions ###
#############################

def createUser(login_session):
    newUser = UserProfile(name=login_session['username'], email=login_session['email'], 
            picture=login_session['picture'], given_name=login_session['given_name'],
            family_name=login_session['family_name'])
    session.add(newUser)
    session.commit()
    user = session.query(UserProfile).filter_by(email=login_session['email']).one()
    return user.id

def getUserID(email):
    try:
        user = session.query(UserProfile).filter_by(email=email).one()
        return user.id
    except:
        return None


#####################################
### login/logout helper functions ###
#####################################

def clearLoginSession(login_session):
    for key in login_session.keys():
        del login_session[key]


def stateIsValid(state):
    """ Returns True if state matches login_session state, else False
    """
    if state != login_session['state']:
        return False
    return True


def loginErrorResponse(message, status_code, 
    flash_message='Login was unsuccessful, please try again.'):
    """Creates a response with the given message and status code, plus a flash message
    """
    print 'Login failed:'
    print str(status_code) + ': ' + message
    flash(flash_message)
    response = make_response(json.dumps(message), status_code)
    response.headers['Content-Type'] = 'application/json'
    return response


if __name__ == '__main__':
    # grab the flask key from the secrets file
    # grab the api-key from the secrets file
    flask_secret = json.loads(open(PATH_TO_FILE + 'secrets.json', 'r').read())['flask']
    app.secret_key = flask_secret
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
