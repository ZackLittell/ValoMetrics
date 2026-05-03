import requests
from bs4 import BeautifulSoup

def scrape_data():
    events = [
        {
            "event_name": "VCT 2024 Americas Kickoff",
            "url": "https://www.vlr.gg/event/stats/1923/champions-tour-2024-americas-kickoff"
        },
        {
            "event_name": "VCT 2024 Americas Stage 1",
            "url": "https://www.vlr.gg/event/stats/2004/champions-tour-2024-americas-stage-1"
        },
        {
            "event_name": "VCT 2024 Americas Stage 2",
            "url": "https://www.vlr.gg/event/stats/2095/champions-tour-2024-americas-stage-2"
        },
        {
            "event_name": "VCT 2025 Americas Kickoff",
            "url": "https://www.vlr.gg/event/stats/2274/vct-2025-americas-kickoff"
        },
        {
            "event_name": "VCT 2025 Americas Stage 1",
            "url": "https://www.vlr.gg/event/stats/2347/vct-2025-americas-stage-1"
        },
        {
            "event_name": "VCT 2025 Americas Stage 2",
            "url": "https://www.vlr.gg/event/stats/2501/vct-2025-americas-stage-2"
        },
        {
            "event_name": "VCT 2026 Americas Kickoff",
            "url": "https://www.vlr.gg/event/stats/2682/vct-2026-americas-kickoff"
        },
    ]

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    players = []

    for event in events:
        response = requests.get(event["url"], headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        all_names = soup.find_all("td", class_="mod-player mod-a")
        acs = soup.find_all("td", class_="mod-color-sq mod-acs")
        stats = soup.find_all("td")
        all_agents = soup.find_all("td", class_="mod-agents")

        if len(all_names) == 0:
            print(f"No player data found for {event['event_name']}")
            continue

        num_stat = int(len(stats) / len(all_names))

        for i in range(len(all_names)):
            all_names_stripped = all_names[i].text.strip()
            split_text = all_names_stripped.split("\n")

            player_name = split_text[0]
            team_name = split_text[1]

            row = i * num_stat

            agent_pngs = all_agents[i].find_all("img")

            agents = []
            for png in agent_pngs:
                src = png.get("src", "")
                agent_name = src.split("/")[-1].replace(".png", "")
                agents.append(agent_name)

            rounds = int(stats[row + 2].text.strip())
            kills = int(stats[row + 16].text.strip())
            deaths = int(stats[row + 17].text.strip())
            assists = int(stats[row + 18].text.strip())
            kast = int(stats[row + 6].text.strip().strip("%"))

            player = {
                "name": player_name,
                "team": team_name,
                "event": event["event_name"],
                "acs": float(acs[i].text.strip()),
                "rounds": rounds,
                "kills": kills,
                "deaths": deaths,
                "assists": assists,
                "KAST": kast,
                "agents": agents
            }

            players.append(player)

    return players

if __name__ == "__main__":
    players = scrape_data()
    print(players)

