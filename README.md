# NHL Jersey Lookup

A simple CLI that finds current NHL players by jersey number and shows each player's last game stat line plus any goals, assists, and highlight links from that game.

Uses two NHL APIs:

- [NHL Stats API](https://api.nhle.com/stats/rest) — filter players by jersey number (`cayenneExp`)
- [NHL Web API](https://api-web.nhle.com/v1) — game logs and game stories for recent activity

## Features

- Finds all active NHL players wearing a given jersey number. The program defaults to jersey #27. Because I'm a fan of John Tonelli #27 who played for the New York Islanders back in the early 80s during the dynasty days.
- Shows team and position for each player
- Shows most recent game stat line from the current season
- Shows goals or assists from that game, with clickable clip links when available

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/)

## Installation

```bash
git clone https://github.com/jcasman/nhl-jersey-lookup.git
cd nhl-jersey-lookup
uv sync
```

## Run

```bash
uv run python main.py
```

Defaults to jersey **#27**. Pass any number as an argument, for example:

```bash
uv run python main.py 72
```

## Example output

```
NHL Jersey Lookup — searching for #27...
Fetching last game info for each player...

Found 20 player(s).

                        Current NHL Players Wearing #27
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ Player            ┃ Team ┃ Position   ┃ Last Game         ┃ Highlights       ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ Nikolaj Ehlers    │ CAR  │ Left Wing  │ 2026-06-14 @ VGK: │ Goal (P3 18:52)  │
│                   │      │            │ 1G-0A-1PT (+1), 3 │                  │
│                   │      │            │ SOG               │                  │
│ Hampus Lindholm   │ BOS  │ Defense    │ 2026-05-01 vs     │ Assist on D.     │
│                   │      │            │ BUF: 0G-1A-1PT    │ Pastrnak (P2     │
│                   │      │            │ (+0), 0 SOG       │ 01:54)           │
│ Shea Theodore     │ VGK  │ Defense    │ 2026-06-14 vs     │ —                │
│                   │      │            │ CAR: 0G-0A-0PT    │                  │
│                   │      │            │ (-1), 1 SOG       │                  │
│ ...               │      │            │                   │                  │
└───────────────────┴──────┴────────────┴───────────────────┴──────────────────┘
```

Highlight entries are clickable links in supported terminals. They point to NHL.com video clips.

## How it works

1. Jersey lookup — queries the Stats API with `cayenneExp=sweaterNumber={N} and currentTeamId>0`, paginated (the API returns max 5 records per page)
2. Team names — maps `currentTeamId` to tri-codes via the Stats API `/team` endpoint
3. Last game — for each player, fetches game logs for the current season (playoffs + regular season) and picks the most recent by date
4. Highlights — fetches the game story for that game and extracts any goals or assists involving the player

## Caveats and Places I may want to update

- Not news articles — Output shows recent on-ice activity (stats and highlight clips), not written NHL.com news
- Slow for large result sets — ~2 API calls per player; a full #27 lookup takes ~20 seconds
- No recent games — players who haven't appeared in an NHL game yet show "No recent games"
- Stale data — some players may show outdated last-game info if the API hasn't updated their game log (e.g. minor-league assignments)
- Quiet games — if a player had no goals or assists, Highlights shows `—`

## Project structure

```
nhl-jersey-lookup/
├── main.py           # CLI entry point
├── nhl_stats_api.py  # Stats API (jersey lookup, team mapping)
├── nhl_web_api.py    # Web API (game log, game story, highlights)
├── pyproject.toml
└── uv.lock
```

