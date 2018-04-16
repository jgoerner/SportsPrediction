from sqlalchemy import create_engine

def get_connection(user="postgres", pw="postgres"):
    """Create a connection to the postgres container
    
    Parameter
    ---------
    user: string,
        postgres username
    pw: string,
        postgres password
        
    
    Return
    ------
    con: engine,
        database engine to be usd in
        e.g. pandas read_sql
    """
    con = create_engine("postgres://{user}:{pw}@postgres_container:5432".format(user=user, pw=pw))
    return con
