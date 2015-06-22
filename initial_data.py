from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Place, Species, SpeciesOccurrence, engine

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

swiftsAtWalter = SpeciesOccurrence(place_id=walterPierce.id, species_id=chimneySwift.id,
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

cardinalAtWalter = SpeciesOccurrence(place_id=walterPierce.id, species_id=cardinal.id,
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

deerAtWalter = SpeciesOccurrence(place_id=walterPierce.id, species_id=deer.id,
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

foxAtWalter = SpeciesOccurrence(place_id=walterPierce.id, species_id=redFox.id,
    tip = """
    Rarely seen in the valley behind the basketball court.  Look for motion under the vegetation. 
    """)

session.add(foxAtWalter)
session.commit()


# add rat snake
ratSnake = Species(common_name="Black Rat Snake",
    scientific_name="Elaphe obsoleta", 
    description="""
    Black non-venomous snake which climbs trees and can grow up to six feet in length.
    """,
    category="reptile", 
    picture_url="http://upload.wikimedia.org/wikipedia/commons/d/d4/Black_Rat_Snake.jpg")

session.add(ratSnake)
session.commit()

ratSnakeAtWalter = SpeciesOccurrence(place_id=walterPierce.id, species_id=ratSnake.id,
    tip = """
    In the summer of 2013, several rat snakes fell from the trees in the children's playground.
    """)

session.add(ratSnakeAtWalter)
session.commit()


# add tulip tree
tulipTree = Species(common_name="Tuliptree",
    scientific_name="Liriodendron tulipifera", 
    description="""
    One of the largest hardwood trees in North America, with unique leaf shape and green tulip-shaped flowers.
    """,
    category="tree", 
    picture_url="http://upload.wikimedia.org/wikipedia/commons/3/37/Liriodendron_tulipifera_%28arbre%29_-_Laeken.JPG")

session.add(tulipTree)
session.commit()

tulipAtWalter = SpeciesOccurrence(place_id=walterPierce.id, species_id=tulipTree.id,
    tip = """
    Medium tree near the drinking fountain, up above the basketball court. 
    """)

session.add(tulipAtWalter)
session.commit()


# add Red-bellied woodpecker
rbWoodpecker = Species(common_name="Red-bellied woodpecker",
    scientific_name="Melanerpes carolinus", 
    description="""
    Medium woodpecker with strikingly barred backs and red caps. 
    """,
    category="bird", 
    picture_url="http://upload.wikimedia.org/wikipedia/commons/1/12/Red-bellied_Woodpecker-27527.jpg")

session.add(rbWoodpecker)
session.commit()

rbWoodpeckerAtWalter = SpeciesOccurrence(place_id=walterPierce.id, species_id=rbWoodpecker.id,
    tip = """
    Easiest to find by listening for the distinctive 'churrr' call along with drumming. 
    Often seen in the woods behind the dog park and in the trees on the other side of the valley.
    """)

session.add(rbWoodpeckerAtWalter)
session.commit()


#####################################
# Create Dumbarton Oaks instance
dumbartonOaks = Place(name="Dumbarton Oaks Park", 
    longitude="-77.064373", latitude="38.916790")

session.add(dumbartonOaks)
session.commit()

# add cardinal to dumbarton
cardinalAtDumbarton = SpeciesOccurrence(place_id=dumbartonOaks.id, species_id=cardinal.id,
    tip = """
    Seen and heard year round throughout the park.
    """)

session.add(cardinalAtDumbarton)
session.commit()


# add Eastern Towhee
towhee = Species(common_name="Eastern Towhee",
    scientific_name="Pipilo erythrophthalmus", 
    description="""
    An oversized sparrow with bold black and warm reddish-browns.  
    Often rummaging in undergrowth. Sings classic "drink-your-tea!" song.
    """,
    category="bird", 
    picture_url="http://upload.wikimedia.org/wikipedia/commons/2/21/Pipilo_erythrophthalmus_-Quabbin_Reservoir%2C_Massachusetts%2C_USA_-male-8.jpg")

session.add(towhee)
session.commit()

towheeAtDumbarton = SpeciesOccurrence(place_id=dumbartonOaks.id, species_id=towhee.id,
    tip = """
    Often heard rummaging in the bushes up the hill that leads to the fenced Dumbarton Oaks Gardens.
    """)

session.add(towheeAtDumbarton)
session.commit()


# add deer to dumbarton
deerAtDumbarton = SpeciesOccurrence(place_id=dumbartonOaks.id, species_id=deer.id,
    tip = """
    Often seen on the northwest side of the park in the woods around Observatory Circle and Whitehaven Street. 
    """)

session.add(deerAtDumbarton)
session.commit()

