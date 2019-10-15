#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=${DOMAIN} \
USERNAME=${USERNAME} \
EMAIL=${EMAIL} \
HASHED_PASSWORD=${HASHED_PASSWORD} \
TRAEFIK_TAG=${TRAEFIK_TAG} \
STACK_NAME=${STACK_NAME} \
TAG=${TAG-latest} \
docker-compose \
-f docker-compose.shared.admin.yml \
-f docker-compose.deploy.admin.yml \
-f docker-compose.deploy.command.yml \
-f docker-compose.deploy.images.yml \
-f docker-compose.deploy.labels.yml \
-f docker-compose.deploy.networks.yml \
-f docker-compose.deploy.ports.yml \
-f docker-compose.deploy.volumes-placement.yml \
config > docker-stack.yml

docker stack deploy -c docker-stack.yml --with-registry-auth ${STACK_NAME}
