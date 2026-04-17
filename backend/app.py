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
        cursor.execute("SELECT team_id FROM teams WHERE name = %s", (player["team"],))
        team_result = cursor.fetchone()

        if team_result:
            team_id = team_result[0]
        else:
            cursor.execute("INSERT INTO teams (name) VALUES (%s)", (player["team"],))
            conn.commit()
            team_id = cursor.lastrowid

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

        cursor.execute("""
            INSERT INTO player_stats (player_id, rounds, kills, deaths, assists, acs, kast, agent)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            player_id,
            player["rounds"],
            player["kills"],
            player["deaths"],
            player["assists"],
            player["acs"],
            player["KAST"],         
            "AGENTS PLACEHOLDER"     
        ))
        conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Scraped data imported successfully"})

if __name__ == "__main__":
    app.run(debug=True)
