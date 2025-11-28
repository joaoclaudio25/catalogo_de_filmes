// Chave da API OMDb
const API_KEY = "7baf41a";
const BACKEND_URL = "http://127.0.0.1:5000/movies";

// ---------------------------
// BUSCAR FILME NA OMDB
// ---------------------------
async function searchMovie() { 
    const movieName = document.getElementById("movieName").value.trim();
    const resultDiv = document.getElementById("result");
    const actionsDiv = document.getElementById("actions");

    if (!movieName) {
        resultDiv.innerHTML = "<p>Digite um nome de filme.</p>";
        actionsDiv.innerHTML = "";
        return;
    }

    const url = `https://www.omdbapi.com/?apikey=${API_KEY}&t=${movieName}`;

    try {
        const response = await fetch(url);
        const data = await response.json();

        if (data.Response === "False") {
            resultDiv.innerHTML = "<p>Filme não encontrado.</p>";
            actionsDiv.innerHTML = "";
            return;
        }

        resultDiv.innerHTML = `
            <h2>${data.Title}</h2>
            <p><strong>Avaliação:</strong> ${data.imdbRating}</p>
            <p><strong>Ano:</strong> ${data.Year}</p>
            <img src="${data.Poster}" alt="Poster" width="200">
        `;

        actionsDiv.innerHTML = `
            <button id="saveBtn" class="addBtn">Salvar no Catálogo</button>
        `;

        document.getElementById("saveBtn").onclick = () => saveMovie(data);

    } catch (error) {
        resultDiv.innerHTML = "<p>Erro ao consultar API.</p>";
        console.error(error);
    }
}

// ---------------------------
// SALVAR FILME NO CATÁLOGO
// ---------------------------
async function saveMovie(movieData) {

    const payload = {
        title: movieData.Title,
        year: movieData.Year,
        rating: movieData.imdbRating,
        poster: movieData.Poster
    };

    try {
        const response = await fetch(BACKEND_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (response.status === 201) {
            alert("Filme salvo com sucesso!");
            loadCatalog();  // recarrega tabela
            return;
        }

        if (response.status === 409) {
            alert("❌ Filme já cadastrado no catálogo!");
            return;
        }

        alert("Erro ao cadastrar filme.");

    } catch (error) {
        alert("Falha ao conectar ao servidor.");
        console.error(error);
    }
}

// ---------------------------
// CARREGAR CATÁLOGO
// ---------------------------
async function loadCatalog() {
    const url = "http://127.0.0.1:5000/movies";

    try {
        const response = await fetch(url);
        const data = await response.json();

        const tbody = document.getElementById("catalogBody");
        tbody.innerHTML = "";

        data.forEach(movie => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${movie.id}</td>
                <td>${movie.title}</td>
                <td>${movie.year}</td>
                <td>${movie.rating}</td>

                <!-- Checkbox Assistido -->
                <td>
                    <input 
                        type="checkbox" 
                        ${movie.watched ? "checked" : ""}
                        onchange="updateWatched(${movie.id}, this.checked)"
                    >
                </td>

                <!-- Campo Minha Nota -->
                <td>
                    <input 
                        type="number" 
                        step="0.1" 
                        min="0" 
                        max="10"
                        value="${movie.my_rating ?? ""}"
                        ${movie.watched ? "" : "disabled"}
                        onchange="updateMyRating(${movie.id}, this.value)"
                    >
                </td>

                <td><img src="${movie.poster}" alt="Poster"></td>

                <td>
                    <button onclick="deleteMovie(${movie.id})">Excluir</button>
                </td>
            `;

            tbody.appendChild(row);
        });

    } catch (error) {
        console.error("Erro ao carregar catálogo:", error);
    }
}

// ---------------------------
// EXCLUIR FILME DO CATÁLOGO
// ---------------------------
async function deleteMovie(id) {
    if (!confirm("Deseja realmente excluir este filme?")) return;

    try {
        const response = await fetch(`http://127.0.0.1:5000/movies/${id}`, {
            method: "DELETE"
        });

        if (response.ok) {
            alert("Filme excluído!");
            loadCatalog();
        } else {
            alert("Erro ao excluir.");
        }
    } catch (error) {
        console.error("Erro ao excluir filme:", error);
    }
}

// ---------------------------
// Função para atualizar o status de assistido
// ---------------------------
async function updateWatched(id, watched) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/movies/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ watched })
        });

        await loadCatalog();

    } catch (error) {
        console.error("Erro ao atualizar assistido:", error);
    }
}

//Função para atualizar minha nota
async function updateMyRating(id, rating) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/movies/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ my_rating: rating })
        });

        await loadCatalog();

    } catch (error) {
        console.error("Erro ao atualizar minha nota:", error);
    }
}



// ---------------------------
// CARREGAR A TABELA AO ABRIR A PÁGINA
// ---------------------------
window.onload = loadCatalog;
