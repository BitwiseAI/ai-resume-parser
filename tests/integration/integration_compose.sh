#!/usr/bin/env bash
set -euo pipefail
export OPENAI_API_KEY=${OPENAI_API_KEY:?OPENAI_API_KEY is required}

# bring up the stack
docker compose up -d --build
# wait for API to be ready
tries=0
until curl -sf http://localhost:8001/health >/dev/null || [ $tries -ge 30 ]; do
  tries=$((tries+1)); sleep 2;
done

# run API tests against compose
API_URL=http://localhost:8001 pytest -q -k "integration"

# teardown
docker compose down -v
