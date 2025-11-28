#Regras de negócio (criar, listar, atualizar, excluir)
from database import db
from models.movie import Movie
from sqlalchemy.exc import IntegrityError

class MovieService:

    @staticmethod
    def create(data):
        movie = Movie(
            title=data.get("title"),
            year=data.get("year"),
            rating=data.get("rating"),
            poster=data.get("poster"),
            watched=data.get("watched", False),
            my_rating=data.get("my_rating")
        )

        try:
            db.session.add(movie)
            db.session.commit()
            return movie, None
        except IntegrityError:
            db.session.rollback()
            return None, "duplicate"

    @staticmethod
    def get_all():
        return Movie.query.all()

    @staticmethod
    def get_by_id(id):
        return Movie.query.get(id)

    @staticmethod
    def update(id, data):
        movie = Movie.query.get(id)
        if not movie:
            return None

        movie.title = data.get("title", movie.title)
        movie.year = data.get("year", movie.year)
        movie.rating = data.get("rating", movie.rating)
        movie.poster = data.get("poster", movie.poster)
        movie.watched = data.get("watched", movie.watched)
        movie.my_rating = data.get("my_rating", movie.my_rating)

        db.session.commit()
        return movie

    @staticmethod
    def delete(id):
        movie = Movie.query.get(id)
        if not movie:
            return False

        db.session.delete(movie)
        db.session.commit()
        return True
