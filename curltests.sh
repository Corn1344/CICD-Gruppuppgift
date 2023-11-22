#!/bin/bash

ip_addr=$(docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" flask_application):5000

middle_text () {
	COLUMNS=$(tput cols 2> /dev/null || echo 80)
	dots=$((($COLUMNS - ${#1} - 2) / 2))
	for ((i=1; i<$dots; ++i)); do
		echo -n "="
	done
	echo -n " $1 "
	for ((i=1; i<$dots; ++i)); do
		echo -n "="
	done
	echo ""
}

middle_text "Running API tests to ip: $ip_addr"

fail () {
	middle_text "TEST FAILED"
	exit 1
}

success () {
	middle_text "ALL TESTS PASSED in $(($end_time - $start_time)) seconds"
	exit 0
}

try_conn () {
	res=$(curl -s -o /dev/null --retry-delay 1 --retry 10 --retry-all-errors -w "%{http_code}" -I http://$ip_addr)
	if [[ $res == "404" ]]; then
		echo "Running tests..."
	else
		middle_text "Connection timed out"
		exit 1
	fi
}

assert () {
	if [[ $1 == *"$2"* ]]; then
		echo "....OK!"
	else
		echo "FAILED!"
		fail
	fi
}

show_function_name () {
	echo -n "$1"
	dots=$(($(tput cols 2> /dev/null || echo 80) - ${#1} - 7))
	for _ in $(seq 1 $dots); do
		echo -n "."
		sleep 0.05
	done
}

test_watched_url_post () {
	show_function_name "$FUNCNAME"
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
	show_function_name "$FUNCNAME"
	URL=http://$ip_addr/watched-urls
	res=$(curl -s -X GET $URL)
	assert "$res" "urlIds"
}

test_watched_url_id_get () {
	show_function_name "$FUNCNAME"
	URL=http://$ip_addr/watched-urls/$URLID
	res=$(curl -s -X GET $URL)
	assert "$res" "activateAt"
}

test_watched_url_id_delete () {
	show_function_name "$FUNCNAME"
	URL=http://$ip_addr/watched-urls/$URLID
	res=$(curl -s -X DELETE $URL)
	assert "$res" "message"
}

test_watched_url_id_delete_should_err () {
	show_function_name "$FUNCNAME"
	URL=http://$ip_addr/watched-urls/$URLID
	res=$(curl -s -X DELETE $URL)
	assert "$res" "error"
}

start_time=$SECONDS
try_conn
test_watched_url_post
test_watched_url_get
test_watched_url_id_get
test_watched_url_id_delete
test_watched_url_id_delete_should_err
end_time=$SECONDS

success
