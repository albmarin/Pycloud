#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=${DOMAIN} \
TRAEFIK_TAG=${TRAEFIK_TAG} \
STACK_NAME=${STACK_NAME} \
TAG=${TAG-latest} \
docker-compose \
-f docker-compose.shared.admin.yml \
-f docker-compose.deploy.command.yml \
-f docker-compose.deploy.images.yml \
-f docker-compose.deploy.labels.yml \
-f docker-compose.deploy.networks.yml \
-f docker-compose.deploy.ports.yml \
-f docker-compose.deploy.env.yml \
-f docker-compose.deploy.volumes-placement.yml \
-f docker-compose.deploy.volumes.yml \
config > docker-stack.yml

docker stack deploy -c docker-stack.yml --with-registry-auth ${STACK_NAME}