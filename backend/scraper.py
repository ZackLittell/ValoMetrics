import requests
from bs4 import BeautifulSoup

def scrape_data():
    url = "https://www.vlr.gg/event/stats/2682/vct-2026-americas-kickoff"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    all_names = soup.find_all("td", class_="mod-player mod-a")
    acs = soup.find_all("td", class_="mod-color-sq mod-acs")
    stats = soup.find_all("td")

    players = []

    num_stat = int(len(stats) / len(all_names))

    for i in range(len(all_names)):
        all_names_stripped = all_names[i].text.strip()
        split_text = all_names_stripped.split("\n")

        player_name = split_text[0]
        team_name = split_text[1]

        row = i * num_stat

        rounds = int(stats[row + 2].text.strip())
        kills = int(stats[row + 16].text.strip())
        deaths = int(stats[row + 17].text.strip())
        assists = int(stats[row + 18].text.strip())
        kast = int(stats[row + 6].text.strip().strip("%"))

        player = {
            "name": player_name,
            "team": team_name,
            "acs": float(acs[i].text.strip()),
            "rounds": rounds,
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "KAST": kast
        }

        players.append(player)

    return players

if __name__ == "__main__":
    players = scrape_data()
    print(players)

