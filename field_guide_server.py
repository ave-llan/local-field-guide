from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
app = Flask(__name__)

## import CRUD Operations ##
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Place, Species, SpeciesOccurrence

# Create session and connect to DB
engine = create_engine('sqlite:///fieldguide.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# home page
@app.route('/')
def homePage():
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
    if request.method == 'POST':
        newPlace = Place(name = request.form['name'],
                    longitude = request.form['longitude'],
                    latitude = request.form['latitude'])
        session.add(newPlace)
        session.commit()
        # redirect user back to the main page
        # TODO add flash here
        return redirect(url_for('homePage'))
    else:
        return render_template('newplace.html')


@app.route('/addspecies', methods=['GET', 'POST'])
def addSpecies():
    if request.method == 'POST':
        newSpecies = Species(common_name = request.form['commonName'],
                    scientific_name = request.form['scientificName'],
                    category = request.form['category'],
                    picture_url = request.form['picture_url'])
        session.add(newSpecies)
        session.commit()
        # redirect user back to the main page
        # TODO add flash here
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
        # redirect user back to the main page
        # TODO add flash here
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
        # redirect to the page for the place of this species occurrence
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
        return redirect(url_for('placeFieldGuide', place_id=place_id))

    else:
        occurrence = session.query(SpeciesOccurrence).filter_by(place_id=place_id, species_id=species_id).one()
        return render_template('deleteoccurrence.html', occurrence=occurrence)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)