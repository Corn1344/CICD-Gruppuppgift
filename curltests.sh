#!/bin/bash
ip_addr=$(docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" flask_application):5000
echo "Running API tests to ip: $ip_addr..."
echo ""

try_conn () {
	res=$(curl -s -o /dev/null --retry-delay 1 --retry 10 --retry-all-errors -w "%{http_code}" -I http://$ip_addr)
	if [[ $res == "404" ]]; then
		echo "Running tests..."
	else
		echo "Connection timed out"
		exit 1
	fi
}

assert () {
	if [[ $1 == *"$2"* ]]; then
		echo "OK!"
	else
		echo "FAILED!"
		exit 1
	fi
}

test_watched_url_post () {
	echo -n "$FUNCNAME..."
	URL=http://$ip_addr/watched-urls
	JSON='''
	{
		"activateAt": "2023-11-06T01:36:28+00:00",
		"force": true,
		"periodSec": 30,
		"url": "https://www.youtube.com"
	}
	'''
	res=$(curl -s -X POST $URL -H "Content-Type: application/json" -d "$JSON")
	assert "$res" "message"
	URLID=$(echo $res | grep -oE "[0-9]+")
}

test_watched_url_get () {
	echo -n "$FUNCNAME..."
	URL=http://$ip_addr/watched-urls
	res=$(curl -s -X GET $URL)
	assert "$res" "urlIds"
}


test_watched_url_id_get () {
	echo -n "$FUNCNAME..."
	URL=http://$ip_addr/watched-urls/$URLID
	res=$(curl -s -X GET $URL)
	assert "$res" "activateAt"
}

test_watched_url_id_delete () {
	echo -n "$FUNCNAME..."
	URL=http://$ip_addr/watched-urls/$URLID
	res=$(curl -s -X DELETE $URL)
	assert "$res" "message"
}

test_watched_url_id_delete_should_err () {
	echo -n "$FUNCNAME..."
	URL=http://$ip_addr/watched-urls/$URLID
	res=$(curl -s -X DELETE $URL)
	assert "$res" "error"
}

test_watched_url_post
test_watched_url_get
test_watched_url_id_get
test_watched_url_id_delete
test_watched_url_id_delete_should_err

exit 0
