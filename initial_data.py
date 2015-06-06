from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Place, Species, SpeciesAtLocation, engine

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create Walter Pierce Park instance
walterPierce = Place(name="Walter Pierce Park", 
    longitude="-77.046051", latitude="38.924066")

session.add(walterPierce)
session.commit()

chimneySwift = Species(common_name="Chimney Swift",
    scientific_name="Chaetura pelagica", 
    description="""
    Look like cigars with wings, always chattering high above
    while catching insects.  Almost always flying and only lands
    to roost in chimneys.   
    """,
    category="bird", 
    picture_url="http://upload.wikimedia.org/wikipedia/commons/6/6d/Chimney_swift_overhead.jpg")

session.add(chimneySwift)
session.commit()

swiftsAtWalter = SpeciesAtLocation(place_id=walterPierce.id, species_id=chimneySwift.id,
    prevalence = 'common',
    tip = """
    In the summer, almost always flying high above the park.  Some roost in the chimneys of 
    the buildings along Adams Mill Road.
    """)

session.add(swiftsAtWalter)
session.commit()




