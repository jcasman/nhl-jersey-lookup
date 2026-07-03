import requests
from rich.text import Text

WEB_BASE_URL = "https://api-web.nhle.com/v1"
CURRENT_SEASON = "20252026"


def _get(path):
    url = f"{WEB_BASE_URL}/{path}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def fetch_last_game(player_id):
    candidates = []

    for game_type in (3, 2):
        try:
            payload = _get(f"player/{player_id}/game-log/{CURRENT_SEASON}/{game_type}")
            candidates.extend(payload.get("gameLog", []))
        except requests.RequestException:
            continue

    if not candidates:
        try:
            payload = _get(f"player/{player_id}/game-log/now")
            candidates = payload.get("gameLog", [])
        except requests.RequestException:
            return None

    if not candidates:
        return None

    return max(candidates, key=lambda game: game["gameDate"])


def fetch_game_story(game_id):
    return _get(f"wsc/game-story/{game_id}")


def find_player_scoring_events(player_id, game_story):
    events = []

    for period in game_story.get("summary", {}).get("scoring", []):
        period_number = period.get("periodDescriptor", {}).get("number")
        period_type = period.get("periodDescriptor", {}).get("periodType", "REG")

        for goal in period.get("goals", []):
            time_in_period = goal.get("timeInPeriod", "")
            highlight_url = goal.get("highlightClipSharingUrl")

            if goal.get("playerId") == player_id:
                events.append(
                    {
                        "type": "goal",
                        "period": period_number,
                        "period_type": period_type,
                        "time": time_in_period,
                        "highlight_url": highlight_url,
                    }
                )
                continue

            for assist in goal.get("assists", []):
                if assist.get("playerId") == player_id:
                    scorer = goal.get("name", {}).get("default", "unknown")
                    events.append(
                        {
                            "type": "assist",
                            "period": period_number,
                            "period_type": period_type,
                            "time": time_in_period,
                            "scorer": scorer,
                            "highlight_url": highlight_url,
                        }
                    )

    return events


def format_period_label(period_number, period_type):
    if period_type == "OT":
        return "OT"
    if period_type == "SO":
        return "SO"
    return f"P{period_number}"


def format_last_game_line(game, position_code):
    opponent = game.get("opponentAbbrev", "???")
    date = game.get("gameDate", "")
    home_away = "vs" if game.get("homeRoadFlag") == "H" else "@"

    if position_code == "G" or "decision" in game:
        decision = game.get("decision", "")
        save_pctg = game.get("savePctg")
        save_pctg_text = f", {save_pctg:.3f} SV%" if save_pctg is not None else ""
        decision_text = f", {decision}" if decision else ""
        return (
            f"{date} {home_away} {opponent}: "
            f"{game.get('shotsAgainst', 0)} SA, {game.get('goalsAgainst', 0)} GA"
            f"{save_pctg_text}{decision_text}"
        )

    goals = game.get("goals", 0)
    assists = game.get("assists", 0)
    points = game.get("points", 0)
    plus_minus = game.get("plusMinus", 0)
    plus_minus_sign = "+" if plus_minus >= 0 else ""
    shots = game.get("shots", 0)

    return (
        f"{date} {home_away} {opponent}: "
        f"{goals}G-{assists}A-{points}PT ({plus_minus_sign}{plus_minus}), "
        f"{shots} SOG"
    )


def format_highlights(events):
    if not events:
        return "—"

    lines = []
    for event in events:
        period_label = format_period_label(event["period"], event["period_type"])
        time_label = event["time"]

        if event["type"] == "goal":
            label = f"Goal ({period_label} {time_label})"
        else:
            label = f"Assist on {event['scorer']} ({period_label} {time_label})"

        highlight_url = event.get("highlight_url")
        if highlight_url:
            lines.append(Text.from_markup(f"[link={highlight_url}]{label}[/link]"))
        else:
            lines.append(label)

    if len(lines) == 1:
        return lines[0]

    return Text("\n").join(lines)


def fetch_last_game_summary(player_id, position_code):
    game = fetch_last_game(player_id)
    if game is None:
        return "No recent games", "—"

    last_game_line = format_last_game_line(game, position_code)

    try:
        game_story = fetch_game_story(game["gameId"])
        events = find_player_scoring_events(player_id, game_story)
        highlights_line = format_highlights(events)
    except requests.RequestException:
        highlights_line = "—"

    return last_game_line, highlights_line
