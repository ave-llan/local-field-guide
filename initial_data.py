from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Place, Species, SpeciesOccurrence, engine
import json
from os import listdir


Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



# takes a json file, creates a place and adds species
def fieldGuideFromJSON(filename, owner):
    # read file
    with open(filename) as guide_file:
        guide_data = json.loads(guide_file.read())

    # Create field guide
    fieldguide = Place(
        name=guide_data['name'],
        latitude=guide_data['latitude'],
        longitude=guide_data['longitude'],
        user_id=owner.id)
    session.add(fieldguide)
    session.commit()

    for s in guide_data['species']:
        # try to get species from database (it might not be there yet)
        sp = session.query(Species).filter_by(
            scientific_name=s['scientific_name']).scalar()
        # if species not in database, first add it
        if sp is None:
            sp = Species(
                common_name=s['common_name'],
                scientific_name=s['scientific_name'])
            session.add(sp)
            session.commit()
        # add species to this field guide
        occurrance = SpeciesOccurrence(
            place_id=fieldguide.id,
            species_id=sp.id,
            tip=s['tip'])
        session.add(occurrance)
        session.commit()


# Create inital user to whom all initial field guides will be assigned
juan = User(
    name="Juan Avellanas",
    email="jrleszczynski@gmail.com",
    picture="http://c2.staticflickr.com/4/3909/15252090882_19df37d630_n.jpg",
    given_name="Juan",
    family_name="Avellanas")
session.add(juan)
session.commit()

# add all files in initial-field-guides directory to database
for fgJSON in listdir('initial-field-guides'):
    filepath = 'initial-field-guides/' + fgJSON
    fieldGuideFromJSON(filepath, juan)


