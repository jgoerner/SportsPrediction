from neomodel import (
    StructuredNode,
    StringProperty,
)

class Team(StructuredNode):
    """Boilerplate for a team node
    
    Attributes:
        name (str): Name of the team
        acr (str): three-letter acronym of the team name
    """
    acr = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=True)