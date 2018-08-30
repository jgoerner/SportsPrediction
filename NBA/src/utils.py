import base64
from functools import wraps
import json
import os
import requests
import time

from neomodel import db


def init_connection():
    """
    Initiates the connection to the Neo4J Docker
    """
    db.set_connection("bolt://{auth}@neo4j:7687".format(auth=os.environ["NEO4J_AUTH"].replace("/", ":")))


def print_information(func):
    """Decorator to print name and execution time of function
    
    Parameters
    ----------
    func: callable
        function that shall be wrapped
        
    Remarks
    -------
    For the best result make sure that the func name is split by underscores 
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # print start block
        name = " ".join(func.__name__.split("_"))
        print("#"*(len(name)+4))
        print("# {} #".format(name))
        print("#"*(len(name)+4))
        
        # get start time
        t1 = time.time()

        # execute the function
        result = func(*args, **kwargs)
        
        # get the end time
        t2 = time.time()
        
        # print result
        print("finished in {:.2f} seconds\n".format(t2-t1))
        
        # return the result
        return result
    
    return wrapper


def send_request(link):
    """Send a request to MySportFeeds
    
    Parameters
    ----------
    link: string,
        API endpoint that shall be queried
    """
    api_key = os.environ["MSF-TOKEN"]

    try:
        response = requests.get(
            url=link,
            params={
                "fordate": "2018121"
            },
            headers={
                "Authorization": "Basic " + base64.b64encode('{}:{}'.format(api_key,"MYSPORTSFEEDS").encode('utf-8')).decode('ascii')
            }
        )
        print("{}: {}".format(response.status_code, response.reason))
        return response
    except requests.exceptions.RequestException:
        print("{}: {}".format(response.status_code, response.reason))
        print('HTTP Request failed')
