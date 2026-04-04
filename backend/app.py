from flask import Flask, jsonify

app = Flask(__name__)

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
    player = SAMPLE_PLAYERS.get(name)
    if player is None:
        return jsonify({"error": "Player not found"}), 404
    return jsonify(player)

if __name__ == "__main__":
    app.run(debug=True)
