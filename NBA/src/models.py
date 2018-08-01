from neomodel import (
    FloatProperty,
    IntegerProperty,
    RelationshipTo,
    StructuredNode,
    StringProperty,
)

class Team(StructuredNode):
    """Boilerplate for a team node
    
    Attributes:
        name (str): name of the team
        acr (str): three-letter acronym of the team name
    """
    
    #PROPERTIES
    acr = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True)


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


class Arena(StructuredNode):
    """Boilerplate for an arena node
    
    name (str): name of the arena
    capacity (int): capacity of the arena
    lat (float): latitude of arena
    lon (float): longitude of arena
    """
    
    # PROPERTIES
    name = StringProperty(required=True, unique_index=True)
    capacity = IntegerProperty(required=True)
    lat = FloatProperty(required=True)
    lon = FloatProperty(required=True)
    
    # RELATIONSHIPS
    city = RelationshipTo(City, "IS_IN")
