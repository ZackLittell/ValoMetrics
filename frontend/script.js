function searchPlayer() {
    const playerName = document.getElementById("playerSearch").value.trim();

    const resultsDiv = document.getElementById("results");

    resultsDiv.innerHTML = "";

    if (playerName.trim() === "") {
        resultsDiv.innerHTML = "<p>Please enter a player name.</p>";
        return;
    }

    resultsDiv.innerHTML = "<p>Loading...</p>";

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
                <p><strong>Rounds:</strong> ${data.rounds}</p>
                <p><strong>Kills:</strong> ${data.kills}</p>
                <p><strong>Deaths:</strong> ${data.deaths}</p>
                <p><strong>Assists:</strong> ${data.assists}</p>
                <p><strong>K/D Ratio:</strong> ${(data.kills / data.deaths).toFixed(2)}</p>
                <p><strong>ACS:</strong> ${data.acs}</p>
                <p><strong>KAST:</strong> ${data.kast}%</p>
                <p><strong>Agent Usage:</strong> ${data.agent_usage}</p>
            `;
        })
        .catch(error => {
            resultsDiv.innerHTML = `<p>${error.message}</p>`;
        });
}

function compareTeams() {
    const teamOne = document.getElementById("teamOne").value.trim();
    const teamTwo = document.getElementById("teamTwo").value.trim();
    const teamResults = document.getElementById("teamResults");

    teamResults.innerHTML = "";

    if (teamOne === "" || teamTwo === "") {
        teamResults.innerHTML = "<p>Please enter two team names.</p>";
        return;
    }

    if (teamOne.toLowerCase() === teamTwo.toLowerCase()) {
        teamResults.innerHTML = "<p>Please enter two different teams.</p>";
        return;
    }

    teamResults.innerHTML = "<p>Loading team comparison...</p>";

    fetch(`http://127.0.0.1:5000/compare-teams/${teamOne}/${teamTwo}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("One or both teams not found");
            }
            return response.json();
        })
        .then(data => {
            teamResults.innerHTML = `
                <h3>${data.team1.team_name} vs ${data.team2.team_name}</h3>

                <p><strong>Team Kills:</strong> ${data.team1.team_kills} vs ${data.team2.team_kills}</p>
                <p><strong>Team Deaths:</strong> ${data.team1.team_deaths} vs ${data.team2.team_deaths}</p>
                <p><strong>Team K/D:</strong> ${(data.team1.team_kills / data.team1.team_deaths).toFixed(2)} vs ${(data.team2.team_kills / data.team2.team_deaths).toFixed(2)}</p>
                <p><strong>Team Assists:</strong> ${data.team1.team_assists} vs ${data.team2.team_assists}</p>
                <p><strong>Average ACS:</strong> ${data.team1.average_acs} vs ${data.team2.average_acs}</p>
                <p><strong>Average KAST:</strong> ${data.team1.average_kast}% vs ${data.team2.average_kast}%</p>
                <p><strong>Team Rounds:</strong> ${data.team1.team_rounds} vs ${data.team2.team_rounds}</p>
                <p><strong>Team KPR:</strong> ${(data.team1.team_kills / data.team1.team_rounds).toFixed(2)} vs ${(data.team2.team_kills / data.team2.team_rounds).toFixed(2)}</p>
            `;
        })
        .catch(error => {
            teamResults.innerHTML = `<p style="color:red;">${error.message}</p>`;
        });
}