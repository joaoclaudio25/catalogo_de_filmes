// =============================
// CONFIGURAÇÕES
// =============================
const API_KEY = "7baf41a";
const BACKEND_URL = "http://127.0.0.1:5000/movies/";   // <-- IMPORTANTE: barra no final

// =============================
// BUSCA FILME NA OMDB
// =============================
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
            <p><strong>Avaliação IMDb:</strong> ${data.imdbRating}</p>
            <p><strong>Ano:</strong> ${data.Year}</p>
            <img src="${data.Poster}" width="200">
        `;

        actionsDiv.innerHTML = `
            <button id="saveBtn" class="addBtn">Salvar no Catálogo</button>
        `;

        document.getElementById("saveBtn").onclick = () => saveMovie(data);

    } catch (error) {
        console.error("Erro ao consultar API OMDb:", error);
        resultDiv.innerHTML = "<p>Erro ao consultar API.</p>";
    }
}

// =============================
// SALVAR FILME NO CATÁLOGO
// =============================
async function saveMovie(movieData) {
    const payload = {
        title: movieData.Title,
        year: movieData.Year,
        rating: movieData.imdbRating,
        poster: movieData.Poster,
        watched: false,
        my_rating: null
    };

    try {
        const response = await fetch(BACKEND_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (response.status === 201) {
            alert("Filme salvo com sucesso!");
            loadCatalog();
            return;
        }

        if (response.status === 409) {
            alert("❌ Filme já cadastrado no catálogo!");
            return;
        }

        alert("Erro ao salvar filme no catálogo.");

    } catch (error) {
        alert("Erro de conexão com o servidor.");
        console.error(error);
    }
}

// =============================
// CARREGAR CATÁLOGO DO BANCO
// =============================
async function loadCatalog() {
    const tbody = document.getElementById("catalogBody");

    try {
        const response = await fetch(BACKEND_URL);
        const data = await response.json();

        tbody.innerHTML = "";

        data.forEach(movie => {
            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${movie.id}</td>
                <td>${movie.title}</td>
                <td>${movie.year}</td>
                <td>${movie.rating}</td>

                <td>
                    <input type="checkbox" 
                        ${movie.watched ? "checked" : ""}
                        onchange="updateWatched(${movie.id}, this.checked)">
                </td>

                <td>
                    <input type="number"
                        min="0" max="10" step="0.1"
                        value="${movie.my_rating ?? ""}"
                        ${movie.watched ? "" : "disabled"}
                        onchange="updateMyRating(${movie.id}, this.value)">
                </td>

                <td><img src="${movie.poster}" width="60"></td>

                <td>
                    <button onclick="deleteMovie(${movie.id})" class="btn-delete">
                        Excluir
                    </button>
                </td>
            `;

            tbody.appendChild(row);
        });

    } catch (error) {
        console.error("Erro ao carregar catálogo:", error);
        tbody.innerHTML = "<tr><td colspan='8'>Erro ao carregar catálogo.</td></tr>";
    }
}

// =============================
// ATUALIZAR CAMPO: ASSISTIDO?
// =============================
async function updateWatched(id, watched) {
    try {
        await fetch(BACKEND_URL + id, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ watched })
        });

        loadCatalog();

    } catch (error) {
        console.error("Erro ao atualizar campo assistido:", error);
    }
}

// =============================
// ATUALIZAR MINHA AVALIAÇÃO
// =============================
async function updateMyRating(id, rating) {
    try {
        await fetch(BACKEND_URL + id, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ my_rating: rating })
        });

        loadCatalog();

    } catch (error) {
        console.error("Erro ao atualizar minha avaliação:", error);
    }
}

// =============================
// EXCLUIR FILME
// =============================
async function deleteMovie(id) {
    if (!confirm("Deseja realmente excluir este filme?")) return;

    try {
        await fetch(BACKEND_URL + id, {
            method: "DELETE"
        });

        loadCatalog();

    } catch (error) {
        console.error("Erro ao excluir filme:", error);
    }
}

// =============================
// CARREGAR CATÁLOGO AO ABRIR A PÁGINA
// =============================
window.onload = loadCatalog;

