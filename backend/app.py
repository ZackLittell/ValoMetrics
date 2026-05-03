from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from scraper import scrape_data

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Password5",
        database="valometrics"
    )

## NO LONGER USED
# SAMPLE_PLAYERS = {
#     "Aspas": {
#         "player_name": "Aspas",
#         "kills": 4401,
#         "deaths": 3061,
#         "assists": 738,
#         "kd_ratio": 1.44,
#         "acs": 248.4,
#         "kast": 75,
#         "agent_usage": "Jett",
#     }
# }

@app.route("/player/<name>")
def get_player(name: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT p.name AS player_name, ps.rounds, ps.kills, ps.deaths, ps.assists, ps.acs, ps.kast, ps.agent
    FROM players p
    JOIN player_stats ps ON p.player_id = ps.player_id
    WHERE p.name = %s
    LIMIT 1;
    """

    cursor.execute(query, (name,))
    player = cursor.fetchone()

    cursor.close()
    conn.close()

    if player is None:
        return jsonify({"error": "Player not found"}), 404
    return jsonify(player)

@app.route("/import-data")
def import_data():
    players = scrape_data()

    conn = get_db_connection()
    cursor = conn.cursor()

    for player in players:
        ## TEAMS
        cursor.execute("SELECT team_id FROM teams WHERE name = %s", (player["team"],))
        team_result = cursor.fetchone()

        if team_result:
            team_id = team_result[0]
        else:
            cursor.execute("INSERT INTO teams (name) VALUES (%s)", (player["team"],))
            conn.commit()
            team_id = cursor.lastrowid

        ## PLAYERS
        cursor.execute("SELECT player_id FROM players WHERE name = %s", (player["name"],))
        player_result = cursor.fetchone()

        if player_result:
            player_id = player_result[0]
        else:
            cursor.execute(
                "INSERT INTO players (name, team_id) VALUES (%s, %s)",
                (player["name"], team_id)
            )
            conn.commit()
            player_id = cursor.lastrowid

        ## EVENTS
        cursor.execute("SELECT event_id FROM events WHERE name = %s", (player["event"],))
        event_result = cursor.fetchone()

        if event_result:
            event_id = event_result[0]
        else:
            cursor.execute(
                "INSERT INTO events (name) VALUES (%s)",
                (player["event"],)
            )
            conn.commit()
            event_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO player_stats (player_id, event_id, rounds, kills, deaths, assists, acs, kast, agent)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            player_id,
            event_id,
            player["rounds"],
            player["kills"],
            player["deaths"],
            player["assists"],
            player["acs"],
            player["KAST"],         
            ",".join(player.get("agents", []))    
        ))
        conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Scraped data imported successfully"})

@app.route("/compare-teams/<team1>/<team2>")
def compare_teams(team1: str, team2: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
        t.name AS team_name,
        SUM(ps.kills) AS team_kills,
        SUM(ps.deaths) AS team_deaths,
        SUM(ps.assists) AS team_assists,
        ROUND(AVG(ps.acs), 2) AS average_acs,
        ROUND(AVG(ps.kast), 2) AS average_kast,
        ROUND(SUM(ps.rounds) / 5) AS team_rounds
    FROM teams t
    JOIN players p ON t.team_id = p.team_id
    JOIN player_stats ps ON p.player_id = ps.player_id
    WHERE t.name = %s
    GROUP BY t.name
    """

    cursor.execute(query, (team1,))
    team1_data = cursor.fetchone()

    cursor.execute(query, (team2,))
    team2_data = cursor.fetchone()

    cursor.close()
    conn.close()

    if team1_data is None or team2_data is None:
        return jsonify({"error": "One or both teams not found"}), 404
    
    return jsonify({
        "team1": team1_data,
        "team2": team2_data
    })

@app.route("/team-event-stats/<team1>/<team2>")
def team_event_stats(team1: str, team2: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT
        e.event_id,
        e.name AS event_name,
        t.name AS team_name,
        SUM(ps.kills) AS kills,
        SUM(ps.deaths) AS deaths,
        SUM(ps.assists) AS assists,
        ROUND(AVG(ps.acs), 2) AS average_acs,
        ROUND(AVG(ps.kast), 2) AS average_kast,
        ROUND(SUM(ps.rounds) / 5, 0) AS rounds,
        ROUND(SUM(ps.kills) / NULLIF(SUM(ps.deaths), 0), 2) AS kd_ratio
    FROM teams t
    JOIN players p ON t.team_id = p.team_id
    JOIN player_stats ps ON p.player_id = ps.player_id
    JOIN events e ON ps.event_id = e.event_id
    WHERE t.name IN (%s, %s)
    GROUP BY e.event_id, e.name, t.name
    ORDER BY e.event_id, t.name;
    """

    cursor.execute(query, (team1, team2))
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return jsonify({"error": "No event stats found for those teams"}), 404

    return jsonify({"event_stats": rows})

if __name__ == "__main__":
    app.run(debug=True)
