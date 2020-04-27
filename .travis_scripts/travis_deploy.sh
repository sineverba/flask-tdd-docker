#!/bin/sh

#docker login -u _ -p $HEROKU_AUTH_TOKEN registry.heroku.com;
#docker push $HEROKU_REGISTRY_IMAGE;
#IMAGE_ID=$(docker inspect ${HEROKU_REGISTRY_IMAGE} --format={{.Id}})
#PAYLOAD='{"updates": [{"type": "web", "docker_image": "'"$IMAGE_ID"'"}]}'

#curl -n -X PATCH https://api.heroku.com/apps/$HEROKU_APP_NAME/formation \
#  -d "${PAYLOAD}" \
#  -H "Content-Type: application/json" \
#  -H "Accept: application/vnd.heroku+json; version=3.docker-releases" \
#  -H "Authorization: Bearer ${HEROKU_AUTH_TOKEN}";
heroku container:push web --app $HEROKU_APP_NAME;
heroku container:release web --app $HEROKU_APP_NAME;
heroku run python manage.py db migrate --app $HEROKU_APP_NAME;
heroku run python manage.py db upgrade --app $HEROKU_APP_NAME;