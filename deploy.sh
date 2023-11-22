#!/bin/bash

docker build -t flask_app backend/.
if [ "$(docker ps -a -q -f name=flask_application)" ]; then
    docker stop flask_application
    docker rm flask_application
fi
docker run -d --network flaskan_docker-network --name flask_application flask_app -p 5000:5000
IP_ADDR=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' flask_application)
echo "Flask app running on: http://$IP_ADDR:5000"