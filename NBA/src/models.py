from neomodel import (
    BooleanProperty,
    DateTimeProperty,
    FloatProperty,
    IntegerProperty,
    RelationshipTo,
    StructuredNode,
    StringProperty
)



class Player(StructuredNode):
    """Boilerplate for a player node
    
    Attributes:
        msfID (int): My-Sports-Feed ID of the player
        firstName (str): first name of the player
        lastName (str): last name of the player
        primaryPosition (str): primary position 
        height (float): height of the player in cm
        weight (float): weight of the player in kg
        birthDate (datetime): day of birth
        rookie (bool): flag indicating if the player is a rookie
        shoots (str): primary throwing hand
        officialImageSrc (str): URL of the official NBA "mugshot"
        draftedYear (int): year the player was drafted
        draftedRound (int): round the player was drafted
        draftedRoundPick (int): position the player was drafted inside the draft round
        draftedOverallPick (int): position the player was drafted overall
        nbaID = (int): stats.nba ID of the player
    """

    # PROPERTIES
    msfID = IntegerProperty(required=True, unique_index=True)
    firstName = StringProperty(required=True)
    lastName = StringProperty(required=True)
    primaryPosition = StringProperty(required=True)
    height = FloatProperty(required=True)
    weight = FloatProperty(required=True)
    birthDate = DateTimeProperty(required=True)
    rookie = BooleanProperty(require=True)
    shoots = StringProperty()
    officialImageSrc = StringProperty(required=True)
    draftedYear = IntegerProperty(required=True)
    draftedRound = IntegerProperty(required=True)
    draftedRoundPick = IntegerProperty(required=True)
    draftedOverallPick = IntegerProperty(required=True)
    nbaID = IntegerProperty() 
    
    # RELATIONSHIPS
    # TODO: birthCity
    # TODO: birthCountry
    
    
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
    venue_id = IntegerProperty(required=True, unique_index=True)
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
    game_id = IntegerProperty(required=True, unique_index=True)
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
        team_id (int): msf team ID
        abbreviation (str): three-letter acronym of the team name
    """
    
    #PROPERTIES
    name = StringProperty(required=True)
    team_id = IntegerProperty(required=True, unique_index=True)
    abbreviation = StringProperty(required=True, unique_index=True)
    
    # RELATIONSHIPS
    division = RelationshipTo(Division, "PLAYS_IN")
    arena = RelationshipTo(Arena, "HAVE_HOME_COURT_AT")
    scored = RelationshipTo(Score, "SCORED")