from sqlalchemy import create_engine

def get_connection(user, pw):
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
    if not user:
        raise ValueError("Must specify a user when connecting to postgres")
    if not pw:
        raise ValueError("Must specify a password when connecting to postgres")
    con = create_engine("postgres://{user}:{pw}@postgres_container:5432".format(user=user, pw=pw))
    return con
