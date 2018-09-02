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


class JumpBall(StructuredNode):
    """Boilerplate for a Jumpball node
    
    Attributes:
        name (str): name of the jumpball
        won_by (str): AWAY or HOME
        elapsed_seconds (int): time after which play occured
        quarter (int): quarter in which the play occured
        away_player (Player): away player of the jumpball
        home_player (Player): home player of the jumpball
        game (Game): game in which the jumpball occured in
    """

    # PROPERTIES
    name = StringProperty(required=True)
    won_by = StringProperty(required=True)
    elapsed_seconds = IntegerProperty(required=True)
    quarter = IntegerProperty(required=True)


    # RELATIONSHIPS
    away_player = RelationshipTo(Player, "BY_AWAY_PLAYER")
    home_player = RelationshipTo(Player, "BY_HOME_PLAYER")
    game = RelationshipTo(Game, "IN_GAME")


class Violation(StructuredNode):
    """Boilerplate for a Violation node
    
    Attributes:
        name (str): name of the violation
        team_abbreviation (str): abbreviation of the player's team
        violation_type (str): personal foul or team foul
        elapsed_seconds (int): time after which play occured
        quarter (int): quarter in which the play occured
        player (Player): player who violated (if not team foul)
        game (Game): game in which the violation occured in
    """
    
    # PROPERTIES
    name = StringProperty(required=True)
    team_abbreviation = StringProperty(required=True)
    vioalation_type = StringProperty(required=True)
    elapsed_seconds = IntegerProperty(required=True)
    quarter = IntegerProperty(required=True)
    
    # RELATIONSHIPS
    player = RelationshipTo(Player, "VIOLOATED_BY")
    game = RelationshipTo(Game, "IN_GAME")


class Turnover(StructuredNode):
    """Boilerplate for a Turnover node
    
    Attributes:
        name (str): name of the turnover
        is_stolen (boolean): is the turnover a steal or not
        turnover_type (str): personal foul or team foul
        elapsed_seconds (int): time after which play occured
        quarter (int): quarter in which the play occured
        lost_by_player (Player): player who lost the ball
        stolen_by_player (Player): player who stole the ball
        game (Game): game in which the turnover occured in
    """
    
    # PROPERTIES
    name = StringProperty(required=True)
    is_stolen = BooleanProperty(required=True)
    turnover_type = StringProperty(required=True)
    elapsed_seconds = IntegerProperty(required=True)
    quarter = IntegerProperty(required=True)
    
    # RELATIONSHIPS
    lost_by_player = RelationshipTo(Player, "LOST_BY")
    stolen_by_player = RelationshipTo(Player, "STOLEN_BY")
    game = RelationshipTo(Game, "IN_GAME")


class Foul(StructuredNode):
    """Boilerplate for a Foul node
    
    Attributes:
        name (str): name of the foul
        team_abbreviation (str): abbreviation of the fouling player's team
        foul_type (str): personal foul or team foul
        elapsed_seconds (int): time after which play occured
        quarter (int): quarter in which the play occured
        drawn_by_player (Player): player who got fouled
        penalized_player (Player): player who fouled
        game (Game): game in which the foul occured in
    """
    
    # PROPERTIES
    name = StringProperty(required=True)
    team_abbreviation = StringProperty(required=True)
    foul_type = StringProperty(required=True)
    elapsed_seconds = IntegerProperty(required=True)
    quarter = IntegerProperty(required=True)
    
    # RELATIONSHIPS
    drawn_by_player = RelationshipTo(Player, "DRAWN_BY")
    penalized_player = RelationshipTo(Player, "PENALIZED")
    game = RelationshipTo(Game, "IN_GAME")


class FieldGoalAttempt(StructuredNode):
    """Boilerplate for a FieldGoalAttempt node
    
    Attributes:
        name (str): name of the field goal attempt
        points (int): points of the throw
        result (str): result of the attempt
        shot_type (str): type of the shot
        elapsed_seconds (int): time after which play occured
        quarter (int): quarter in which the play occured
        shooting_player (Player): player who did the shot
        assisting_player (Player): player who did assist
        blocking_player (Player): player who did block
        game (Game): game in which the attempt occured in
    """
    
    # PROPERTIES
    name = StringProperty(required=True)
    points = IntegerProperty(required=True)
    result = StringProperty(required=True)
    shot_type = StringProperty(required=True)
    elapsed_seconds = IntegerProperty(required=True)
    quarter = IntegerProperty(required=True)
    
    # RELATIONSHIPS
    shooting_player = RelationshipTo(Player, "SHOT_BY")
    assisting_player = RelationshipTo(Player, "ASSISTED_BY")
    blocking_player = RelationshipTo(Player, "BLOCKED_BY")
    game = RelationshipTo(Game, "IN_GAME")


class Rebound(StructuredNode):
    """Boilerplate for a rebound node
    
    Attributes:
        name (str): name of the turnover
        rebound_type (str): type of the rebound
        elapsed_seconds (int): time after which play occured
        quarter (int): quarter in which the play occured
        retrieving_player (Player): player who retrieves
        game (Game): game in which the turnover occured in
    """
    
    # PROPERTIES
    name = StringProperty(required=True)
    rebound_type = StringProperty(required=True)
    elapsed_seconds = IntegerProperty(required=True)
    quarter = IntegerProperty(required=True)
    
    # RELATIONSHIPS
    retrieving_player = RelationshipTo(Player, "RETRIEVED_BY")
    game = RelationshipTo(Game, "IN_GAME")


class Substitution(StructuredNode):
    """Boilerplate for a Substitution node
    
    Attributes:
        name (str): name of the turnover
        elapsed_seconds (int): time after which play occured
        quarter (int): quarter in which the play occured
        
        incoming_player (Player): player who enters the game
        outgoing_player (Player): player who leaves the game
        game (Game): game in which the subsitution occured in
    """
    
    # PROPERTIES
    name = StringProperty(required=True)
    elapsed_seconds = IntegerProperty(required=True)
    quarter = IntegerProperty(required=True)
    
    # RELATIONSHIPS
    incoming_player = RelationshipTo(Player, "INCOMING")
    outgoing_player = RelationshipTo(Player, "OUTGOING")
    game = RelationshipTo(Game, "IN_GAME")


class FreeThrowAttempt(StructuredNode):
    """Boilerplate for a FreeThrowAttempt node
    
    Attributes:
        name (str): name of the attempt
        number (int): number of the attempt
        total_attempts (int): number of total attempts
        result (str): scored or missed
        elapsed_seconds (int): time after which play occured
        quarter (int): quarter in which the play occured
        
        shooting_player (Player): player shot the free throw
        game (Game): game in which the turnover occured in
    """
    
    # PROPERTIES
    name = StringProperty(required=True)
    number = IntegerProperty(required=True)
    total_attempts = StringProperty(required=True)
    elapsed_seconds = IntegerProperty(required=True)
    quarter = IntegerProperty(required=True)
    
    # RELATIONSHIPS
    shooting_player = RelationshipTo(Player, "SHOT_BY")
    game = RelationshipTo(Game, "IN_GAME")