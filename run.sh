#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

set -a
source env/dev.env
set +a

docker compose config >/dev/null

docker compose down -v --remove-orphans

docker compose up airflow-init

docker compose up -d

docker compose ps