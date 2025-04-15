#!/bin/bash
set -e

# Suppression du réseau existant s'il existe
if docker network ls --filter name=^common-network$ --format "{{.Name}}" | grep -w "common-network" > /dev/null; then
  echo "Suppression du réseau 'common-network' existant..."
  docker network rm common-network
fi
echo "Création du réseau 'common-network'..."
docker network create --driver bridge common-network
