from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, UserProfile, Place, Species, SpeciesOccurrence, engine
import json
from os import listdir

import flickr, wikipedia

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



# takes a json file name, creates a place and adds species
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

    print 'Searching Flickr and Wikipedia for...'

    for s in guide_data['species']:
        # try to get species from database (it might not be there yet)
        sp = session.query(Species).filter_by(
            scientific_name=s['scientific_name']).scalar()
        # if species not in database, first add it
        if sp is None:
            print '   {0} ({1})'.format(
                s['scientific_name'],
                s['common_name'])

            # look up photo on flickr (and select the first item from returned list)
            photo = flickr.search(s['scientific_name'])[0]

            # look up description from wikipedia
            description = wikipedia.search(s['scientific_name'])
            wiki_url = wikipedia.articleUrl(s['scientific_name'])

            sp = Species(
                common_name=s['common_name'],
                scientific_name=s['scientific_name'],
                photo = flickr.photoUrl(photo),
                photo_page = flickr.photoPageUrl(photo),
                wiki_url = wiki_url,
                description = description)
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
juan = UserProfile(
    name="John Leszczynski",
    email="jrleszczynski@gmail.com",
    picture="https://lh3.googleusercontent.com/-zNX5AZdffwk/AAAAAAAAAAI/AAAAAAAACoQ/dmsDQGk34DI/photo.jpg",
    given_name="John",
    family_name="Leszczynski")
session.add(juan)
session.commit()


# add all files in initial-field-guides directory to database
for fgJSON in listdir('initial-field-guides'):
    filepath = 'initial-field-guides/' + fgJSON
    fieldGuideFromJSON(filepath, juan)

print "success! fieldguide database has been populated"
