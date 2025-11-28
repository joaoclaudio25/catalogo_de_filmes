from . import db # Importa o objeto 'db' definido em models/base.py (exposto em models/__init__.py)
from sqlalchemy import UniqueConstraint # Importa o módulo de restrições únicas do SQLAlchemy
class Movie(db.Model):
    
    tablename = 'movies'  # Nome da tabela no banco
    id = db.Column(db.Integer, primary_key=True) # Coluna ID, chave primária, numérica, auto-incremento
    title = db.Column(db.String(150), nullable=False)  # Título do filme não pode ser nulo
    rating = db.Column(db.String(10))  # Nota (rating) do IMDB ou outra fonte
    year = db.Column(db.String(10)) # Ano de lançamento
    poster = db.Column(db.String(300)) # URL do pôster do filme
    watched = db.Column(db.Boolean, default=False)  # Indica se o filme foi assistido ou não
    my_rating = db.Column(db.Float, nullable=True) # Minha avaliação pessoal do filme
    # Restrição de unicidade para evitar filmes duplicados (mesmo título e ano)
    __table_args__ = (
        UniqueConstraint("title", "year", name="uix_title_year"),
    )
    # Converte o objeto Movie em um dicionário (útil para jsonify)
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "rating": self.rating,
            "year": self.year,
            "poster": self.poster,
            "watched": self.watched,
            "my_rating": self.my_rating
            
        }

    # Cria e salva um novo filme no banco
    @staticmethod
    def create(data):
        # Cria uma instância de Movie com base nos dados recebidos
        movie = Movie(
            title=data.get("title"),
            rating=data.get("rating"),
            year=data.get("year"),
            poster=data.get("poster"),
            watched=data.get("watched", False), # Padrão é False pois se entende que ao criar, ainda não foi assistido
            my_rating=data.get("my_rating")
        )
        
        db.session.add(movie) # Adiciona ao contexto de sessão
        db.session.commit()  # Confirma a transação (salva no banco)
        return movie

    # Retorna todos os filmes cadastrados
    @staticmethod
    def get_all():
        return Movie.query.all()

    # Busca um filme pelo ID
    @staticmethod
    def get_by_id(movie_id):
        return Movie.query.get(movie_id)

    # Atualiza os dados de um filme pelo ID
    @staticmethod
    def update(movie_id, data):
        
        movie = Movie.query.get(movie_id) # Busca o filme no banco
        # Se não encontrar, retorna None
        if not movie:
            return None

        # Atualiza campo a campo, mantendo o valor antigo caso o novo não venha
        movie.title = data.get("title", movie.title)
        movie.rating = data.get("rating", movie.rating)
        movie.year = data.get("year", movie.year)
        movie.poster = data.get("poster", movie.poster)
        movie.watched = data.get("watched", movie.watched)
        movie.my_rating = data.get("my_rating", movie.my_rating)

        # Salva as alterações
        db.session.commit()
        return movie

    # Remove um filme do banco pelo ID
    @staticmethod
    def delete(movie_id):
        movie = Movie.query.get(movie_id)
        # Se não encontrar o filme, não há o que deletar
        if not movie:
            return False
        # Remove da sessão
        db.session.delete(movie)
        # Confirma a remoção
        db.session.commit()
        return True

