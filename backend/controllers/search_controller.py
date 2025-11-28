from flask import Blueprint, request, jsonify, current_app
import requests

search_bp = Blueprint("search", __name__)

@search_bp.get("/")
def search_movie():
    title = request.args.get("title")

    if not title:
        return jsonify({"error": "title required"}), 400

    api_key = current_app.config["OMDB_API_KEY"]
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"

    resp = requests.get(url).json()

    if resp.get("Response") == "False":
        return jsonify({"error": "not found"}), 404

    return jsonify({
        "title": resp.get("Title"),
        "year": resp.get("Year"),
        "rating": resp.get("imdbRating"),
        "poster": resp.get("Poster")
    })
