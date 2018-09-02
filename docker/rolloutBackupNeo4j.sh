#!/usr/bin/env bash
echo "Injecting Backup into docker volume \"sportsprediction_neo4j_data\""
docker run \
  -it --rm \
  -v sportsprediction_neo4j_data:/volume \
  -v `pwd`/NBA/data/backup:/backup \
  alpine \
  sh -c "rm -rf /volume/* /volume/..?*; tar -C /volume/ -xjf /backup/backup_neo.tar.bz2"	

echo "Restarting Neo4J"
docker-compose restart neo4j

echo "Done"
