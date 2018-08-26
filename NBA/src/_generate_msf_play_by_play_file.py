from collections import defaultdict
import os
os.chdir("/home/jovyan/work")

from src.utils import send_request



def _get_play_type(play):
    return (set(play.keys()) - set(["description", "playStatus"])).pop()


def _unmarshall_jumpball(jumpball):
    result = {}
    
    # attributes
    result["name"] = jumpball["description"]
    result["wonBy"] = jumpball["jumpBall"]["wonBy"]
    
    # relationships
    result["homePlayerID"] = jumpball["jumpBall"]["homePlayer"]["id"]
    result["awayPlayerID"] = jumpball["jumpBall"]["awayPlayer"]["id"]
    result["secondsElapsed"] = jumpball["playStatus"]["secondsElapsed"]
    result["quarter"] = jumpball["playStatus"]["quarter"]
    
    PARSED_GAMES["jumpball"].append(result)
    
    
def _unmarshall_fieldGoalAttempt(fieldGoalAttempt):
    result = {}
    
    # attributes
    result["name"] = fieldGoalAttempt["description"]
    result["points"] = fieldGoalAttempt["fieldGoalAttempt"]["points"]
    result["result"] = fieldGoalAttempt["fieldGoalAttempt"]["result"]
    result["shotType"] = fieldGoalAttempt["fieldGoalAttempt"]["shotType"]
    
    # relationships
    result["shootingPlayerID"] = fieldGoalAttempt["fieldGoalAttempt"]["shootingPlayer"]["id"]
    result["secondsElapsed"] = fieldGoalAttempt["playStatus"]["secondsElapsed"]
    result["quarter"] = fieldGoalAttempt["playStatus"]["quarter"]
    
    # fragile values
    if fieldGoalAttempt["fieldGoalAttempt"]["blockingPlayer"] == None:
        result["blockingPlayerID"] = -1
    else:
        result["blockingPlayerID"] = fieldGoalAttempt["fieldGoalAttempt"]["blockingPlayer"]["id"]
    
    if fieldGoalAttempt["fieldGoalAttempt"]["assistingPlayer"] == None:
        result["assistingPlayerID"] = -1
    else:
        result["assistingPlayerID"] = fieldGoalAttempt["fieldGoalAttempt"]["assistingPlayer"]["id"]
    
    PARSED_GAMES["fieldGoalAttempt"].append(result)


def _unmarshall_turnover(turnover):
    result = {}
    
    # attributes
    result["name"] = turnover["description"]
    result["isStolen"] = turnover["turnover"]["isStolen"]
    result["type"] = turnover["turnover"]["type"]
    
    # relationships
    result["lostByPlayerID"] = turnover["turnover"]["lostByPlayer"]["id"]
    result["secondsElapsed"] = turnover["playStatus"]["secondsElapsed"]
    result["quarter"] = turnover["playStatus"]["quarter"]
    
    # fragile values
    if turnover["turnover"]["stolenByPlayer"] == None:
        result["stolenByPlayerID"] = -1
    else:
        result["stolenByPlayerID"] = turnover["turnover"]["stolenByPlayer"]["id"]
    
    PARSED_GAMES["turnover"].append(result)


def _unmarshall_rebound(rebound):
    result = {}
    
    # attributes
    result["name"] = rebound["description"]
    result["type"] = rebound["rebound"]["type"]
    
    # relationships
    result["secondsElapsed"] = rebound["playStatus"]["secondsElapsed"]
    result["quarter"] = rebound["playStatus"]["quarter"]
    
    # fragile values
    if rebound["rebound"]["retrievingPlayer"] == None:
        result["retrievingPlayerID"] = -1
    else:
        result["retrievingPlayerID"] = rebound["rebound"]["retrievingPlayer"]["id"]
    
    PARSED_GAMES["rebound"].append(result)


def _unmarshall_substitution(substitution):
    result = {}
    
    # attributes
    result["name"] = substitution["description"]
    
    # relationships
    result["secondsElapsed"] = substitution["playStatus"]["secondsElapsed"]
    result["quarter"] = substitution["playStatus"]["quarter"]
    
    # fragile values
    if substitution["substitution"]["incomingPlayer"] == None:
        result["incomingPlayerID"] = -1
    else:
        result["incomingPlayerID"] = substitution["substitution"]["incomingPlayer"]["id"]
    
    if substitution["substitution"]["outgoingPlayer"] == None:
        result["outgoingPlayerID"] = -1
    else:
        result["outgoingPlayer"] = substitution["substitution"]["outgoingPlayer"]["id"]
    
    PARSED_GAMES["substitution"].append(result)


def _unmarshall_freeThrowAttempt(freeThrowAttempt):
    result = {}
    
    # attributes
    result["name"] = freeThrowAttempt["description"]
    result["attemptNum"] = freeThrowAttempt["freeThrowAttempt"]["attemptNum"]
    result["result"] = freeThrowAttempt["freeThrowAttempt"]["result"]
    result["totalAttempts"] = freeThrowAttempt["freeThrowAttempt"]["totalAttempts"]
    
    # relationships
    result["shootingPlayerID"] = freeThrowAttempt["freeThrowAttempt"]["shootingPlayer"]["id"]
    result["secondsElapsed"] = freeThrowAttempt["playStatus"]["secondsElapsed"]
    result["quarter"] = freeThrowAttempt["playStatus"]["quarter"]
    
    PARSED_GAMES["freeThrowAttempt"].append(result)


def _unmarshall_violation(violation):
    result = {}
    
    # attributes
    result["name"] = violation["description"]
    result["teamOrPersonal"] = violation["violation"]["teamOrPersonal"]
    
    # relationships
    result["teamAbbreviation"] = violation["violation"]["team"]["abbreviation"]
    result["teamAbbreviation"] = violation["violation"]["team"]["abbreviation"]
    result["secondsElapsed"] = violation["playStatus"]["secondsElapsed"]
    result["quarter"] = violation["playStatus"]["quarter"]
    
    # fragile values
    if violation["violation"]["player"] == None:
        result["playerID"] = -1
    else:
        result["playerID"] = violation["violation"]["player"]["id"]
    
    PARSED_GAMES["violation"].append(result)


def _unmarshall_foul(foul):
    result = {}
    
    # attributes
    result["name"] = foul["description"]
    result["teamAbbreviation"] = foul["foul"]["team"]["abbreviation"]
    
    # relationships
    result["secondsElapsed"] = foul["playStatus"]["secondsElapsed"]
    result["quarter"] = foul["playStatus"]["quarter"]
    
    # fragile values
    if foul["foul"]["penalizedPlayer"] == None:
        result["penalizedPlayerID"] = -1
    else:
        result["penalizedPlayerID"] = foul["foul"]["penalizedPlayer"]["id"]

    if foul["foul"]["drawnByPlayer"] == None:
        result["drawnByPlayerID"] = -1
    else:
        result["drawnByPlayerID"] = foul["foul"]["drawnByPlayer"]["id"]

    if  foul["foul"]["isPersonal"]:
        result["type"] = "personal"
    elif  foul["foul"]["isTechnical"]:
        result["type"] = "technical"
    elif  foul["foul"]["isFlagrant1"]:
        result["type"] = "flagrant1"
    elif  foul["foul"]["isFlagrant2"]:
        result["type"] = "flagrant2"
    else:
        result["type"] = "unnkown"

    PARSED_GAMES["foul"].append(result)


UNMARSHALL = {
    "jumpBall": _unmarshall_jumpball,
    "fieldGoalAttempt": _unmarshall_fieldGoalAttempt,
    "turnover": _unmarshall_turnover,
    "foul": _unmarshall_foul,
    "rebound": _unmarshall_rebound,
    "substitution": _unmarshall_substitution,
    "freeThrowAttempt": _unmarshall_freeThrowAttempt,
    "violation": _unmarshall_violation
}

PARSED_GAMES = defaultdict(list)

if __name__ == "__main__":
    print("running")