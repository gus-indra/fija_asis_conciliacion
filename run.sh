#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

ENV_FILE="./env/dev.env"

if [[ ! -f "$ENV_FILE" ]]; then
    echo "ERROR: No existe $ENV_FILE" >&2
    exit 1
fi

compose() {
    docker compose --env-file "$ENV_FILE" "$@"
}

echo "==> Validando configuración..."
compose config --quiet

echo "==> Construyendo imágenes..."
compose build

echo "==> Deteniendo contenedores sin eliminar volúmenes..."
compose down --remove-orphans

echo "==> Inicializando o migrando Airflow..."
compose up \
    --exit-code-from airflow-init \
    airflow-init

echo "==> Iniciando servicios..."
compose up -d

echo "==> Estado de los contenedores..."
compose ps -a