"""Watched_urls"""
from datetime import datetime
from flask import request, jsonify
import validators
from werkzeug.exceptions import BadRequest
from pingurl import app
from pingurl.models import WatchedUrl
from pingurl import business, persistance

MIN_PERIOD = 10


@app.route("/watched-urls", methods=["POST"])
def add_watched_url():
    """Retrieves request to add watched url"""
    data = request.get_json()

    try:
        if not "activateAt" in data:
            raise BadRequest("Missing parameter 'activateAt'")

        activate_at = None

        try:
            activate_at = datetime.fromisoformat(
                data["activateAt"].replace("Z", "+00:00")
            )
        except ValueError as error:
            raise BadRequest(
                "The 'activateAt' parameter must an ISO 8601 date-time."
            ) from error

        force = data.get("force", False)

        if not isinstance(force, bool):
            raise BadRequest("The 'force' parameter must be a boolean.")

        if not "periodSec" in data:
            raise BadRequest("Missing parameter 'periodSec'")

        period_sec = data["periodSec"]

        if not isinstance(period_sec, int) or period_sec < MIN_PERIOD:
            raise BadRequest(
                f"The 'periodSec' parameter must be an integer of {MIN_PERIOD} or more."
            )

        if not "url" in data:
            raise BadRequest("Missing parameter 'url'")

        url = data["url"]

        if not isinstance(url, str) or not validators.url(url):
            raise BadRequest("The 'url' parameter must be valid URL string.")

        try:
            watched_url = WatchedUrl(activate_at, force, period_sec, url)

            url_id = business.add_watched_url(watched_url)

            return jsonify({"message": "Watched URL added", "urlId": url_id}), 201

        except business.AddWatchedUrlError as error:
            raise BadRequest(str(error)) from error

    except BadRequest as error:
        return jsonify({"error": "Bad request", "message": error.description}), 400


@app.route("/watched-urls/<int:url_id>", methods=["DELETE"])
def delete_url(url_id):
    """Retrieves request to delete watched url"""
    try:
        business.delete_watched_url(url_id)
    except persistance.WatchedUrlNotFoundError as error:
        return jsonify({"error": str(error)}), 404

    return jsonify({"message": f"Removed watched url with id {url_id}"}), 200


@app.route("/watched-urls/<int:url_id>", methods=["GET"])
def get_url_data(url_id):
    """Retrieves request to get info about watched url from url-id"""
    try:
        url_data = persistance.get_url_data(url_id)

        return jsonify(url_data), 200

    except persistance.WatchedUrlNotFoundError as error:
        return jsonify({"error": str(error)}), 404


@app.route("/watched-urls", methods=["GET"])
def get_url_ids():
    """Retrieves request to get list of watched url-ids"""
    return jsonify({"urlIds": persistance.get_url_ids()}), 200


@app.route("/stats", methods=["GET"])
def get_total():
    """Retrieves request to get stats"""
    return jsonify(persistance.get_stats()), 200
