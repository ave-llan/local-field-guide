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


# add Chimnney Swift
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


# add Northern Cardinal
cardinal = Species(common_name="Northern Cardinal",
    scientific_name="Cardinalis cardinalis", 
    description="""
    Red crested bird with a large repertoire of clear, whistled songs.   
    """,
    category="bird", 
    picture_url="http://bit.ly/1ImrO7d")

session.add(cardinal)
session.commit()

cardinalAtWalter = SpeciesAtLocation(place_id=walterPierce.id, species_id=cardinal.id,
    prevalence = 'common',
    tip = """
    Seen and heard year round.  Likes to perch near the top of trees.
    """)

session.add(cardinalAtWalter)
session.commit()


# add deer
deer = Species(common_name="White-Tailed Deer",
    scientific_name="Odocoileus virginianus", 
    description="""
    Tan deer with white on belly, throat, around eyes, and underside of tail. Male has antlers.
    """,
    category="mammal", 
    picture_url="http://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/White-tailed_deer.jpg/2560px-White-tailed_deer.jpg")

session.add(deer)
session.commit()

deerAtWalter = SpeciesAtLocation(place_id=walterPierce.id, species_id=deer.id,
    prevalence = 'common',
    tip = """
    Freqently seen grazing or resting in the valley behind the basketball court.  Occasionally 
    enters the park itself near the circle. 
    """)

session.add(deerAtWalter)
session.commit()


# add red fox
redFox = Species(common_name="American Red Fox",
    scientific_name="Vulpes vulpes fulvus", 
    description="""
    The size of a medium dog with pointed ears and red fur across the face, back, sides, and tail.
    """,
    category="mammal", 
    picture_url="http://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Fox_study_6.jpg/440px-Fox_study_6.jpg")

session.add(redFox)
session.commit()

foxAtWalter = SpeciesAtLocation(place_id=walterPierce.id, species_id=redFox.id,
    prevalence = 'rare',
    tip = """
    Rarely seen in the valley behind the basketball court.  Look for motion under the vegitation. 
    """)

session.add(foxAtWalter)
session.commit()



