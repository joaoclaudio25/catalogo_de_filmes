from flask import Flask
from flask_cors import CORS
from config import Config
from database import db

from controllers.movie_controller import movie_bp
from controllers.search_controller import search_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    # registrar blueprints
    app.register_blueprint(movie_bp, url_prefix="/movies")
    app.register_blueprint(search_bp, url_prefix="/search")

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)



