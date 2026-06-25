#!/usr/bin/env bash
set -euo pipefail

echo "Seeding Neo4j..."

docker compose exec -T neo4j cypher-shell \
  -u "$NEO4J_USER" \
  -p "$NEO4J_PASSWORD" < seed.cypher

echo "Neo4j seed complete."