#Importações necessárias
from flask import Flask, request, jsonify
from flask_cors import CORS
from models import db, Movie
import requests
# Importa exceção de integridade para tratar erros de unicidade
from sqlalchemy.exc import IntegrityError

# Cria a aplicação Flask
app = Flask(__name__)
# Libera o acesso CORS (permite que o front-end acesse a API)
CORS(app)

# Configuração SQLite
# Caminho do arquivo SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
# Desativa alertas desnecessários do SQLAlchemy
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Inicializa o banco com a aplicação
db.init_app(app)
# Cria as tabelas se não existirem
with app.app_context():
    db.create_all()

# Chave da API OMDb (usada para buscar detalhes de filmes)
OMDB_API_KEY = "${OMDB_APIKEY}"   # Usando uma varável de ambiente, para não expor a chave diretamente no código
#Preciso entender com o professor como ele vai testar a aplicação com a chave da API

# Endpoint de busca no OMDb (somente busca)
@app.get("/search")
def search_movie():
    # Pega o título enviado via query string ?
    movie_title = request.args.get("title")

    # Monta a URL da requisição para a OMDb API
    url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={movie_title}"

    # Faz a requisição HTTP para a API
    response = requests.get(url)
    data = response.json()

    # Tratando erro 404
    if data.get("Response") == "False":
        return jsonify({"error": "Movie not found"}), 404

    # Retorna apenas os dados que interessam ao front-end
    # Título, Avaliação IMDb, Ano e Poster
    # Pode ser extendido futuramente
    return jsonify({
        "title": data.get("Title"),
        "rating": data.get("imdbRating"),
        "year": data.get("Year"),
        "poster": data.get("Poster")
    })

# ------------------------------------------------------------
# ROTAS CRUD DO CATÁLOGO (salvo no banco SQLite local)
# ------------------------------------------------------------

# CREATE — adicionar filme ao catálogo
@app.post("/movies")
def add_movie():
    # Recebe o JSON enviado pelo front-end
    data = request.json
    
    try:
        # Chama o método Movie.create (definido no models.py)
        movie = Movie.create(data)
        # Retorna o filme criado com status 201 (created)
        return jsonify(movie.to_dict()), 201
    except IntegrityError:  # Captura erro de violação de unicidade
        db.session.rollback()  # Reverte a transação
        return jsonify({"error": "Filme já consta no catálogo"}), 400

# READ — listar todos os filmes salvos no banco
# Preciso ajustar o front para consumir esse endpoint e listar os filmes salvos
@app.get("/movies")
def list_movies():
    movies = Movie.get_all()
    return jsonify([m.to_dict() for m in movies])

# READ — buscar um filme pelo ID
@app.get("/movies/<int:movie_id>")
def get_movie(movie_id):
    movie = Movie.get_by_id(movie_id)
    if not movie:
        return jsonify({"error": "Movie not found"}), 404
    return jsonify(movie.to_dict())

# UPDATE — atualizar um filme existente
# Usar para ajustar futura flag de filmes assistidos e avaliação pessoal
@app.put("/movies/<int:id>")
def update_movie(id):
    movie = Movie.update(id, request.json)
    if movie:
        return jsonify(movie.to_dict())
    return jsonify({"error": "Movie not found"}), 404

# DELETE — excluir filme do catálogo
@app.delete("/movies/<int:id>")
def delete_movie(id):
    if Movie.delete(id):
        return jsonify({"message": "Deleted"})
    return jsonify({"error": "Movie not found"}), 404

# ------------------------------------------------------------
# EXECUÇÃO DO SERVIDOR
# ------------------------------------------------------------

if __name__ == "__main__":
    # debug=True recarrega o servidor automaticamente ao salvar mudanças
    app.run(debug=True)


