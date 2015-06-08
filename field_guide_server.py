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


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)