// Chave da API OMDb (em produção é melhor usar no backend, mas aqui está exposta no front)
const API_KEY = "7baf41a"; // sua API key OMDb
// URL base do backend para salvar filmes
const BACKEND_URL = "http://127.0.0.1:5000/movies"; // endpoint do Flask

// Função chamada ao clicar no botão "Buscar"
async function searchMovie() {
    // Lê o valor digitado no input e remove espaços extras
    const movieName = document.getElementById("movieName").value.trim();
    // Referência à div que exibirá o resultado do filme
    const resultDiv = document.getElementById("result");
    // Referência à div que exibirá os botões de ação (ex: salvar)
    const actionsDiv = document.getElementById("actions");

    // Se o usuário não digitou nada, mostra uma mensagem e interrompe
    if (!movieName) {
        resultDiv.innerHTML = "<p>Digite um nome de filme.</p>";
        actionsDiv.innerHTML = "";
        return;
    }

    // Monta a URL da OMDb com a chave e o título do filme
    const url = `https://www.omdbapi.com/?apikey=${API_KEY}&t=${movieName}`;

    try {
        // Faz a requisição para a API OMDb
        const response = await fetch(url);
        // Converte a resposta para JSON
        const data = await response.json();

        // Se a API indicar que não encontrou, exibe mensagem
        if (data.Response === "False") {
            resultDiv.innerHTML = "<p>Filme não encontrado.</p>";
            actionsDiv.innerHTML = "";
            return;
        }

        // Exibe informações básicas do filme
        resultDiv.innerHTML = `
            <h2>${data.Title}</h2>
            <p><strong>Avaliação:</strong> ${data.imdbRating}</p>
            <p><strong>Ano:</strong> ${data.Year}</p>
            <img src="${data.Poster}" alt="Poster" width="200">
        `;

        // Cria botão de salvar no catálogo
        actionsDiv.innerHTML = `
            <button id="saveBtn" class="addBtn">Salvar no Catálogo</button>
        `;

        // Associa o clique do botão à função saveMovie, passando os dados do filme
        document.getElementById("saveBtn").onclick = () => saveMovie(data);

    } catch (error) {
        // Em caso de erro na requisição (rede, CORS, etc.)
        resultDiv.innerHTML = "<p>Erro ao consultar API.</p>";
        console.error(error);
    }
}

// Função para salvar o filme no backend
async function saveMovie(movieData) {

    // Monta o payload com os campos que o backend espera
    const payload = {
        title: movieData.Title,
        year: movieData.Year,
        rating: movieData.imdbRating,
        poster: movieData.Poster
    };

    try {
        // Faz uma requisição POST para o backend
        const response = await fetch(BACKEND_URL, {
            method: "POST",
            headers: {
                // Define corretamente o tipo de conteúdo como JSON
                "Content-Type": "application/json"
            },
            // Converte o objeto payload para string JSON
            body: JSON.stringify(payload)
        });

        // Verifica se o backend respondeu com sucesso (status 2xx)
        if (response.ok) {
            alert("Filme salvo com sucesso!");
        } else {
            alert("Erro ao salvar filme.");
        }
    } catch (error) {
        // Erro de rede ou CORS ao falar com o backend
        alert("Erro ao conectar ao servidor.");
        console.error(error);
    }
}
