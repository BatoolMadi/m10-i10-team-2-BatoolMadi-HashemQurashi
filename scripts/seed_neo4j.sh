#!/usr/bin/env bash
set -euo pipefail

source .env

echo "Seeding Neo4j..."

docker compose exec -T neo4j cypher-shell \
  -u "$NEO4J_USER" \
  -p "$NEO4J_PASSWORD" < api/seed.cypher

echo "Neo4j seed complete."