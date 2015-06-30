from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

## import CRUD Operations ##
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Place, Species, SpeciesOccurrence

# Imports for oAuth
from flask import session as login_session
from flask import make_response
import random, string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


# Create session and connect to DB
engine = create_engine('sqlite:///fieldguide.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    # create a 32 charachter state key
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # check for valid state before proceeding
    if request.args.get('state') != login_session['state']:
        response = make_response(
            json.dumps('Invalid State parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        # upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # check that the access token is valid
    access_token = credentials.access_token
    verification_url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
            % access_token)
    # create json get request with url
    h = httplib2.Http()
    result = json.loads(h.request(verification_url, 'GET')[1])
    # if there is an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # verify the access token is for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID does not match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's id."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    # check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    

    # store the access toekn in the session for later use
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "google login successful!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session.
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
        # Reset the user's session
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

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




# home page
@app.route('/')
def homePage():
    print 'logged in as:'
    print login_session.get('username')
    places = session.query(Place).all()
    # last 10 species added to database
    latestSpecies = session.query(Species).order_by(desc(Species.id)).all()[:10]
    return render_template('index.html', places = places, latestSpecies = latestSpecies)


@app.route('/place/<int:place_id>/')
def placeFieldGuide(place_id):
    place = session.query(Place).filter_by(id=place_id).one()
    occurrences = session.query(SpeciesOccurrence).\
                    filter_by(place_id = place_id).\
                    all()
    return render_template('place.html', place=place, occurrences=occurrences)


@app.route('/place/create/', methods=['GET', 'POST'])
def createPlace():
    if 'username' not in login_session:
        flash("Please login to create a new field guide.")
        return redirect('/login')
    if request.method == 'POST':
        newPlace = Place(name = request.form['name'],
                    longitude = request.form['longitude'],
                    latitude = request.form['latitude'])
        session.add(newPlace)
        session.commit()
        flash("New Place Added")
        return redirect(url_for('homePage'))
    else:
        return render_template('newplace.html')


@app.route('/addspecies', methods=['GET', 'POST'])
def addSpecies():
    if request.method == 'POST':
        newSpecies = Species(common_name = request.form['commonName'],
                    scientific_name = request.form['scientificName'],
                    category = request.form['category'])
        session.add(newSpecies)
        session.commit()
        flash("New Species Added")
        return redirect(url_for('homePage'))
    else:
        return render_template('addspecies.html')


@app.route('/place/<int:place_id>/addspeciestoplace/', methods=['GET', 'POST'])
def addSpeciesToPlace(place_id):
    if request.method == 'POST':
        sp = session.query(Species).filter_by(common_name=request.form['species']).one()
        newSpeciesOccurrence = SpeciesOccurrence(place_id = place_id,
                    species_id = sp.id,
                    tip = request.form['tip'])
        print 'adding', newSpeciesOccurrence
        session.add(newSpeciesOccurrence)
        session.commit()
        flash("New Species Occurrence Added")
        return redirect(url_for('placeFieldGuide', place_id=place_id))
    else:
        place = session.query(Place).filter_by(id=place_id).one()
        species = session.query(Species).all()
        return render_template('addspeciestoplace.html', place=place, species=species)


@app.route('/place/<int:place_id>/<int:species_id>/editoccurrence', methods=['GET', 'POST'])
def editSpeciesOccurrence(place_id, species_id):
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
        return render_template('editspeciesoccurrence.html', occurrence=occurrence)


@app.route('/place/<int:place_id>/<int:species_id>/removeoccurrence', methods=['GET', 'POST'])
def removeOccurrence(place_id, species_id):
    if request.method == 'POST':
        occurrence = session.query(SpeciesOccurrence).filter_by(place_id=place_id, species_id=species_id).one()
        session.delete(occurrence)
        session.commit()
        flash("Species occurrence removed")
        return redirect(url_for('placeFieldGuide', place_id=place_id))

    else:
        occurrence = session.query(SpeciesOccurrence).filter_by(place_id=place_id, species_id=species_id).one()
        return render_template('deleteoccurrence.html', occurrence=occurrence)


# API Endpoint
@app.route('/place/<int:place_id>/JSON')
def placeFieldGuideJSON(place_id):
    place = session.query(Place).filter_by(id=place_id).one()
    occurrences = session.query(SpeciesOccurrence).\
                    filter_by(place_id = place_id).\
                    all()
    return jsonify(fieldGuide=[species.serialize for species in occurrences])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)