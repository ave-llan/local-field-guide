from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

 
Base = declarative_base()


class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)


class Species(Base):
    __tablename__ = 'species'
    
    id = Column(Integer, primary_key=True)
    common_name = Column(String(80), nullable=False)
    scientific_name = Column(String(80), nullable=False)
    # mammal, bird, insect, reptile, fish, butterfly, mushroom, flower, tree
    category = Column(String(80), nullable=False)
    picture_url = Column(String(250))


class SpeciesOccurrence(Base):
    __tablename__ = 'speciesOccurrence'

    place_id = Column(Integer, ForeignKey('place.id'), primary_key=True)
    species_id = Column(Integer, ForeignKey('species.id'), primary_key=True)
    # add a tip about how to find this species at this place
    tip = Column(String(250))

    place = relationship("Place", backref=backref('species'))
    species = relationship("Species")

    # serialize for JSON API
    @property
    def serialize(self):

        return {
            'common_name': self.species.common_name,
            'scientific_name': self.species.scientific_name,
            'tip': self.tip,
            'species_id': self.species_id,
        }




engine = create_engine('sqlite:///fieldguide.db')


Base.metadata.create_all(engine)