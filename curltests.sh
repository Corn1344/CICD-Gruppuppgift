#!/bin/bash
ip_addr=$(docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" flask_application):5000
echo "Running API tests to ip: $ip_addr. . ."
echo ""

postreq=$(curl -X POST http://$ip_addr/watched-urls -H "Content-Type: application/json" -d '{"activateAt": "2023-11-06T01:36:28+00:00", "force": true, "periodSec": 30, "url": "https://www.youtube.com"}')
if [[ $postreq == *'message'* ]]; then
	echo "POST request succeded"
else
	echo "POST request failed"
	exit 1
fi

getreq=$(curl -X GET http://$ip_addr/watched-urls)
if [[ $getreq == *'urlIds'* ]]; then
	echo "GET request succeded"
else
	echo "GET request failed"
	exit 1
fi

getreqid=$(curl -X GET http://$ip_addr/watched-urls/0)
if [[ $getreqid == *'activateAt'* ]]; then
	echo "GET request with ID succeded"
else
	echo "GET request with ID failed"
	exit 1
fi
exit 0
