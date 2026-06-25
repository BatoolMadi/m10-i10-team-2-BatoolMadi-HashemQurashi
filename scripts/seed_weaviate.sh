#!/usr/bin/env bash
set -euo pipefail

echo "Seeding Weaviate..."

docker compose exec -T api python seed_weaviate.py

echo "Weaviate seed complete."