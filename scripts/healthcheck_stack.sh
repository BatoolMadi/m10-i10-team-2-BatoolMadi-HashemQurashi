#!/usr/bin/env bash
set -euo pipefail

echo "Checking service health..."
docker compose ps

if docker compose ps --format json | grep -v '"Health":"healthy"' | grep -q '"State":"running"'; then
    echo "Some services are not yet healthy."
    exit 1
else
    echo "All services are healthy."
fi