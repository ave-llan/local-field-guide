from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

 
Base = declarative_base()


class UserProfile(Base):
    __tablename__ = 'userprofile'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    given_name = Column(String(250))
    family_name = Column(String(250))
    picture = Column(String(250))


class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('userprofile.id'))
    userprofile = relationship("UserProfile")


class Species(Base):
    __tablename__ = 'species'
    
    id = Column(Integer, primary_key=True)
    common_name = Column(String(80), nullable=False)
    scientific_name = Column(String(80), nullable=False)
    # url of a Flickr photo of the species
    photo = Column(String(250))
    # url of the photos page on Flickr
    photo_page = Column(String(250))
    # url for a wikipedia page about this species
    wiki_url = Column(String(250))
    # description of this species from Wikipedia
    description = Column(String(800))


class SpeciesOccurrence(Base):
    __tablename__ = 'speciesOccurrence'

    place_id = Column(Integer, ForeignKey('place.id'), primary_key=True)
    species_id = Column(Integer, ForeignKey('species.id'), primary_key=True)
    # a tip about how to find this species at this place (where to look, what to look for)
    tip = Column(String(250))

    place = relationship("Place", backref=backref('species'))
    species = relationship("Species")

    # serialize for JSON API
    @property
    def serialize(self):
        return {
            'common_name': self.species.common_name,
            'scientific_name': self.species.scientific_name,
            'tip': self.tip
        }




engine = create_engine("postgresql+psycopg2://fieldguide:barnswallow@localhost/fieldguidedb")


Base.metadata.create_all(engine)
