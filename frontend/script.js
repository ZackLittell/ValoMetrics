function searchPlayer() {
    const playerName = document.getElementById("playerSearch").value;

    const resultsDiv = document.getElementById("results");

    resultsDiv.innerHTML = "";

    if (playerName.trim() === "") {
        resultsDiv.innerHTML = "<p>Please enter a player name.</p>";
        return;
    }

    fetch(`http://127.0.0.1:5000/player/${playerName}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Player not found");
            }
            return response.json();
        })
        .then(data => {
            resultsDiv.innerHTML = `
                <h2>${data.player_name}</h2>
                <p><strong>Kills:</strong> ${data.kills}</p>
                <p><strong>Deaths:</strong> ${data.deaths}</p>
                <p><strong>Assists:</strong> ${data.assists}</p>
                <p><strong>K/D Ratio:</strong> ${data.kd_ratio}</p>
                <p><strong>ACS:</strong> ${data.acs}</p>
                <p><strong>KAST:</strong> ${data.kast}%</p>
                <p><strong>Agent Usage:</strong> ${data.agent_usage}</p>
            `;
        })
        .catch(error => {
            resultsDiv.innerHTML = `<p>${error.message}</p>`;
        });
}