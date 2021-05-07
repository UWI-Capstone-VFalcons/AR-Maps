#!/bin/sh


IMAGE_ID=$(docker inspect registry.heroku.com/uwi-ar-maps/web --format={{.Id}})
PAYLOAD='{"updates": [{"type": "web", "docker_image": "'"$IMAGE_ID"'"}]}'

curl -n -X PATCH https://api.heroku.com/apps/uwi-ar-maps/formation \
  -d "${PAYLOAD}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
  -H "Authorization: Bearer 1ecff113-be1b-424d-a3f3-1ff7d351aac4"