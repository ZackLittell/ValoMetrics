CREATE TABLE teams (
    team_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100)
);

CREATE TABLE players (
    player_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    team_id INT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

CREATE TABLE matches (
    match_id INT PRIMARY KEY AUTO_INCREMENT,
    team1_id INT,
    team2_id INT,
    map_name VARCHAR(50),
    winner_team_id INT,
    date DATE
);

CREATE TABLE player_stats (
    stat_id INT PRIMARY KEY AUTO_INCREMENT,
    player_id INT,
    match_id INT,
    kills INT,
    deaths INT,
    assists INT,
    acs FLOAT,
    KAST DECIMAL(5,2),
    agent VARCHAR(50),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (match_id) REFERENCES matches(match_id)
);

INSERT INTO teams (name) VALUES ('LOUD');

INSERT INTO players (name, team_id)
VALUES ('Aspas', 1);

INSERT INTO matches (team1_id, team2_id, map_name, winner_team_id, date)
VALUES (1, 1, 'Ascent', 1, '2024-01-01');

INSERT INTO player_stats (player_id, match_id, kills, deaths, assists, acs, kast, agent)
VALUES (1, 1, 20, 15, 5, 250, 75, 'Jett');
