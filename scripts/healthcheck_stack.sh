#!/usr/bin/env bash
set -euo pipefail

echo "Checking service health..."
docker compose ps

echo "Done."