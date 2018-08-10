from neomodel import (
    FloatProperty,
    IntegerProperty,
    RelationshipTo,
    StructuredNode,
    StringProperty,
    DateTimeProperty
)


class Country(StructuredNode):
    """Boilerplate for a team node
    
    Attributes:
        name (str): name of the country
    """

    # PROPERTIES
    name = StringProperty(required=True)


class State(StructuredNode):
    """Boilerplate for a state node
    
    Attributes:
        name (str): name of the state
        country (Country): country of the state
    """

    # PROPERTIES
    name = StringProperty(required=True)

    # RELATIONSHIPS
    country = RelationshipTo(Country, "IS_IN")


class City(StructuredNode):
    """Boilerplate for a city node
    
    Attributes:
        name (str): name of the city
        state (State): state of the city
    """
    
    # PROPERTIES
    name = StringProperty(required=True)
    
    # RELATIONSHIPS
    state = RelationshipTo(State, "IS_IN")


class Conference(StructuredNode):
    """Boilerplate for a conference node
    
    Attributes:
        name (str): name of a conference
    """

    # PROPERTIES
    name = StringProperty(required=True)   
    

class Division(StructuredNode):
    """Boilerplate for a division node
    
    Attributes:
        name (str): name of a division
    """

    # PROPERTIES
    name = StringProperty(required=True)
    
    # RELATIONSHIPS
    conference = RelationshipTo(Conference, "BELONGS_TO")


class Arena(StructuredNode):
    """Boilerplate for an arena node
    
    name (str): name of the arena
    capacity (int): capacity of the arena
    latitude (float): latitude of arena
    longitude (float): longitude of arena
    """
    
    # PROPERTIES
    name = StringProperty(required=True, unique_index=True)
    capacity = IntegerProperty(required=True)
    latitude = FloatProperty(required=True)
    longitude = FloatProperty(required=True)
    
    # RELATIONSHIPS
    city = RelationshipTo(City, "IS_IN")


class Date(StructuredNode):
    """Boilerplate for an date node
    
    datetime (datetime.datetime): datetime of the game
    """
    
    # PROPERTIES
    datetime = DateTimeProperty(required=True)


class Season(StructuredNode):
    """Boilerplate for a season node
    
    Attributes:
        name (str): name of a division
    """

    # PROPERTIES
    name = StringProperty(required=True)
    
    # RELATIONSHIPS
    season = RelationshipTo(Date, "STARTS")
    #season = RelationshipTo(Date, "ends")


class Game(StructuredNode):
    """Boilerplate for a game node
    
    Attributes:
        type (str): type of game (Regular Season or Playoffs
        OT (int): OT 1 or 0 
    """

    # PROPERTIES
    game_name = StringProperty(required=True)
    game_type = StringProperty(required=True)
    ot = IntegerProperty(required=True)
    
    # RELATIONSHIPS
    arena = RelationshipTo(Arena, "LOCATED_IN")
    date = RelationshipTo(Date, "PLAYED_ON")
    season = RelationshipTo(Season, "TOOK_PLACE_IN")


class Score(StructuredNode):
    """Boilerplate for a score node
    
    Attributes:
        score (str): cumulated score
    """

    # PROPERTIES
    score = IntegerProperty(required=True)
    
    # RELATIONSHIPS
    in_game = RelationshipTo(Game, "IN_GAME")


class Team(StructuredNode):
    """Boilerplate for a team node    
    Attributes:
        name (str): name of the team
        acr (str): three-letter acronym of the team name
    """
    
    #PROPERTIES
    name = StringProperty(required=True)
    
    # RELATIONSHIPS
    division = RelationshipTo(Division, "PLAYS_IN")
    arena = RelationshipTo(Arena, "HAVE_HOME_COURT_AT")
    scored = RelationshipTo(Score, "SCORED")