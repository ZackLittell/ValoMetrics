from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Password5",
        database="valometrics"
    )

SAMPLE_PLAYERS = {
    "Aspas": {
        "player_name": "Aspas",
        "kills": 4401,
        "deaths": 3061,
        "assists": 738,
        "kd_ratio": 1.44,
        "acs": 248.4,
        "kast": 75,
        "agent_usage": "Jett",
    }
}

@app.route("/player/<name>")
def get_player(name: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT p.name AS player_name, ps.kills, ps.deaths, ps.assists,
            ps.acs, ps.kast, ps.agent
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

if __name__ == "__main__":
    app.run(debug=True)
