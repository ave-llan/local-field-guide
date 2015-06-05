import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
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
    description = Column(String(250))
    picture_url = Column(String(250))


class SpeciesAtLocation(Base):
    __tablename__ = 'speciesAtLocation'

    place_id = Column(Integer, ForeignKey('place.id'), primary_key=True)
    place = relationship(Place)

    species_id = Column(Integer, ForeignKey('species.id'), primary_key=True)
    species = relationship(Species)

    # add a tip about how to find this species at this place
    tip = Column(String(250))
    # common, occoasional, OR rare
    prevalence = Column(String(12), nullable=False)



engine = create_engine('sqlite:///fieldguide.db')


Base.metadata.create_all(engine)