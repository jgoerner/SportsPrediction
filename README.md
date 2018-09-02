# SportsPrediction
Predicting Sport Event outcomes.

## How to ramp up the stack
1. put a `neo4j.env` and `aws.env` into `config/` with appropriate access keys & variables (see sample)
2. `docker-compose build --no-cache`
3. `docker-compse up -d`

## How to access Web-UIs
- Jupyter: `http://localhost:7777`
- Neo4j: `http://localhost:7474`

## How to build the graph
- open a new terminal inside the Jupyter container
- navigate to `/home/jovyan/work`
- run `make -B data`
- open a new terminal outside of the Docker container at the root of the repository
- run `make backup`
