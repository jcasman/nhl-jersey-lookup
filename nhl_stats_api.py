import requests

BASE_URL = "https://api.nhle.com/stats/rest/en"
PAGE_SIZE = 5


def _get(path, params=None):
    url = f"{BASE_URL}/{path}"
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_team_map():
    payload = _get("team", params={"cayenneExp": "leagueId=133", "limit": -1})
    return {team["id"]: team["triCode"] for team in payload["data"]}


def fetch_players_by_jersey(jersey_number):
    cayenne_exp = f"sweaterNumber={jersey_number} and currentTeamId>0"
    players = []
    start = 0

    while True:
        payload = _get(
            "players",
            params={
                "cayenneExp": cayenne_exp,
                "limit": PAGE_SIZE,
                "start": start,
            },
        )
        batch = payload.get("data", [])

        if not batch:
            break

        players.extend(batch)
        start += len(batch)

        total = payload.get("total")
        if total is not None and start >= total:
            break

    return players
