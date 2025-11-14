📚 MVP Catálogo de Filmes

Projeto MVP desenvolvido com Python + Flask, SQLite, e Front-end em HTML/CSS/JS, integrando com a OMDb API para busca de filmes e persistindo dados no banco.

🚀 Funcionalidades

Buscar filmes pela API OMDb
Ver título, avaliação (IMDB), ano e pôster
Salvar filmes encontrados no catálogo local
Gerenciar filmes salvos (CRUD) - a ser desenvolvido
Persistir dados em SQLite
Interagir com um front-end simples em HTML + CSS + JS através de API própria com endpoints REST (/movies)

O projeto está organizado no padrão MVC simplificado, dividido entre backend (Flask) e frontend estático.

🗂️ Estrutura do Projeto
MVP/
│
├── backend/
│   ├── app.py              # Aplicação Flask + rotas + integração OMDb
│   ├── requirements.txt    # Dependências do Python
│   ├── README.md           # Docs específicas do backend
│   │
│   ├── instance/
│   │   └── movies.db       # Banco SQLite (persistência local)
│   │
│   ├── log/
│   │   └── gunicorn.detailed.log
│   │
│   └── models/
│       ├── base.py         # Configuração do SQLAlchemy
│       ├── movie.py        # Modelo Movie + métodos CRUD
│       └── __init__.py
│
└── frontend/
    ├── index.html          # Interface do usuário
    ├── style.css           # Estilos visuais
    ├── scripts.js          # Requisições e lógica do front
    │
    └── img/
        └── Filmstrip.jpg   # Imagem decorativa

⚙️ Tecnologias Utilizadas
Backend
Python 3.x
Flask
Flask-CORS
SQLAlchemy
SQLite
OMDb API
HTML
CSS
JavaScript (fetch API)

Como Executar o Backend

1. Criar ambiente virtual (opcional, mas recomendado)
python -m venv venv
source venv/bin/activate   # Linux / MacOS
venv\Scripts\activate      # Windows

2. Instalar dependências

Executar dentro da pasta backend: pip install -r requirements.txt

3. Executar o servidor Flask: python app.py


Por padrão o servidor inicia em: http://127.0.0.1:5000

Como Executar o Frontend

O front-end é estático, basta abrir: frontend/index.html

Você pode rodar direto no navegador ou com um servidor simples:

cd frontend
python -m http.server 8000

A aplicação estará acessível em: http://localhost:8000

API — Endpoints Disponíveis
🔍 Buscar filme pela OMDb
GET /search?title=Batman


Retorno:

{
  "title": "Batman",
  "rating": "7.5",
  "year": "1989",
  "poster": "https://..."
}

Filmes no Catálogo (SQLite)
➕ Criar filme
POST /movies

📄 Listar filmes
GET /movies

🔎 Obter por ID
GET /movies/<id>

✏ Atualizar filme
PUT /movies/<id>

❌ Remover filme
DELETE /movies/<id>

Melhorias Futuras (Roadmap)

 Implementar autenticação (usuários)
 Adicionar página de listagem de filmes salvos
 Melhorar layout com Bootstrap
 Criar filtros (ano, gênero, nota)
 Adicionar opcional: onde assistir (Utelly API)
 Criar testes unitários