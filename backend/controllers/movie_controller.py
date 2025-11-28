from flask import Blueprint, request, jsonify
from services.movie_service import MovieService

#Somente rotas relacionadas ao catálogo de filmes
movie_bp = Blueprint("movies", __name__)

@movie_bp.post("/")
def create_movie():
    movie, error = MovieService.create(request.json)
    if error == "duplicate":
        return jsonify({"error": "duplicate"}), 409
    return jsonify(movie.to_dict()), 201

@movie_bp.get("/")
def list_movies():
    movies = MovieService.get_all()
    return jsonify([m.to_dict() for m in movies])

@movie_bp.get("/<int:id>")
def get_movie(id):
    movie = MovieService.get_by_id(id)
    if not movie:
        return jsonify({"error": "not found"}), 404
    return jsonify(movie.to_dict())

@movie_bp.put("/<int:id>")
def update_movie(id):
    movie = MovieService.update(id, request.json)
    if not movie:
        return jsonify({"error": "not found"}), 404
    return jsonify(movie.to_dict())

@movie_bp.delete("/<int:id>")
def delete_movie(id):
    deleted = MovieService.delete(id)
    if not deleted:
        return jsonify({"error": "not found"}), 404
    return jsonify({"message": "deleted"})
