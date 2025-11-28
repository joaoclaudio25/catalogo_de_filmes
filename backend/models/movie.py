from database import db
from sqlalchemy import UniqueConstraint

class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    year = db.Column(db.String(10))
    rating = db.Column(db.String(10))
    poster = db.Column(db.String(300))

    watched = db.Column(db.Boolean, default=False)
    my_rating = db.Column(db.Float, nullable=True)

    __table_args__ = (
        UniqueConstraint("title", "year", name="uix_title_year"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "rating": self.rating,
            "poster": self.poster,
            "watched": self.watched,
            "my_rating": self.my_rating
        }
