# SportsPrediction
Predicting Sport Event outcomes.

## How to ramp up the stack
1. put a `jupyter.env` and a `neo4j.env` into `config/` with appropriate access keys & variables
2. `docker-compose build --no-cache`
3. `docker-compse up -d`

## How to run automatized tasks
- `make data`: will fetch all CSVs from S3 and persist them inside of the postgres container
- `make features`: will derive all features specified in `src/_derive_features.py`

## How to access Web-UIs
- Jupyter: `http://localhost:7777`
- Neo4j: `http://localhost:7474`
