📚 Catálogo de Filmes – MVP (Flask + SOLID + OMDb + SQLite + Frontend JS)

Este é um MVP de catálogo de filmes que permite:

Buscar filmes na OMDb API
Exibir título, ano, nota IMDb e poster
Salvar o filme em um catálogo local (SQLite)
Marcar filmes como assistidos
Atribuir minha avaliação (nota do usuário)
Exibir o catálogo em uma tabela interativa
Editar status e nota direto na tabela
Seguir o padrão SOLID com serviços, controllers e models separados

🚀 Tecnologias Utilizadas

Backend
Python 3.x
Flask
Flask-CORS
SQLAlchemy (ORM)
SQLite
Requests
Padrão SOLID

Frontend

HTML5
CSS3
JavaScript (Fetch API)
DOM API

Integrações

OMDb API para busca de filmes
https://www.omdbapi.com/

🗂️ Estrutura do Projeto
backend/
│── app.py
│── config.py
│── database.py
│── requirements.txt
│
├── controllers/
│   ├── __init__.py
│   ├── movie_controller.py
│   ├── search_controller.py
│
├── models/
│   ├── __init__.py
│   ├── movie.py
│
├── services/
│   ├── __init__.py
│   ├── movie_service.py
│
└── movies.db  (gerado automaticamente)

frontend/
│── index.html
│── style.css
│── scripts.js
│── img/
│     └── Filmstrip.jpg

⚙️ Como executar o projeto
1️⃣ Instalar dependências do backend

No diretório backend/: pip install -r requirements.txt

2️⃣ Configurar OMDb API Key

No arquivo frontend/scripts.js, ajuste: const API_KEY = "SUA_API_KEY";

3️⃣ Iniciar o servidor Flask: python app.py

O backend ficará disponível em: http://127.0.0.1:5000

4️⃣ Abrir o frontend

Abra o arquivo: frontend/index.html

Melhorias Futuras (Roadmap)

 Criar ENUM com Streamings para levantar onde foi assisito
 Implementar autenticação (usuários)
 Melhorar layout com Bootstrap
 Criar filtros (ano, gênero, nota)
 Criar testes unitários
 Usar uma API de IA para traduzir o nome dos filmes em Português e apresentar ao usuário ambos os nomes
 Futuramento trazer a sinopse dos filmes traduzida
 Função recomenda
 Função recomenda para quem

Visão do Produto Final: o objetivo é ter uma aplicação web e mobile (Android e IOS) onde cada usuário
pode montar o seu catálogo de filmes para compartilhar com amigos e parentes, além de montar  uma base
que vai permitir desenvolvermos uma API para disponibilizar onde assistir os filmes. A visão do produto final é facilitar a troca de informações sobre filmes que gostamos e aproximar pessoas com gostos semelhantes para que possamos receber recomendações de filmes com probabilidade de gostarmos e não perder nosso tempo assistindo filmes que não nos agradam.