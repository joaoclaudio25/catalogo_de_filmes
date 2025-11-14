# Importa o objeto 'db' definido em models/base.py (exposto em models/__init__.py)
from . import db

# Define o modelo Movie que será mapeado para uma tabela no banco de dados
class Movie(db.Model):
    # Coluna ID, chave primária, numérica, auto-incremento
    id = db.Column(db.Integer, primary_key=True)
    # Título do filme
    title = db.Column(db.String(150))
    # Nota (rating) do IMDB ou outra fonte
    rating = db.Column(db.String(10))
    # Ano de lançamento
    year = db.Column(db.String(10))
    # URL do pôster do filme
    poster = db.Column(db.String(300))

    # Converte o objeto Movie em um dicionário (útil para jsonify)
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "rating": self.rating,
            "year": self.year,
            "poster": self.poster
        }

    # Cria e salva um novo filme no banco
    @staticmethod
    def create(data):
        # Cria uma instância de Movie com base nos dados recebidos
        movie = Movie(
            title=data.get("title"),
            rating=data.get("rating"),
            year=data.get("year"),
            poster=data.get("poster")
        )
        # Adiciona ao contexto de sessão
        db.session.add(movie)
        # Confirma a transação (salva no banco)
        db.session.commit()
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
        # Busca o filme no banco
        movie = Movie.query.get(movie_id)
        # Se não encontrar, retorna None
        if not movie:
            return None

        # Atualiza campo a campo, mantendo o valor antigo caso o novo não venha
        movie.title = data.get("title", movie.title)
        movie.rating = data.get("rating", movie.rating)
        movie.year = data.get("year", movie.year)
        movie.poster = data.get("poster", movie.poster)

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

