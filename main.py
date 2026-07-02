import argparse

from rich.console import Console
from rich.table import Table

from nhl_stats_api import fetch_players_by_jersey, fetch_team_map

console = Console()

POSITION_NAMES = {
    "C": "Center",
    "L": "Left Wing",
    "R": "Right Wing",
    "D": "Defense",
    "G": "Goalie",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Find current NHL players wearing a given jersey number."
    )
    parser.add_argument(
        "jersey_number",
        nargs="?",
        type=int,
        default=27,
        help="Jersey number to search for (default: 27)",
    )
    return parser.parse_args()


def format_position(position_code):
    return POSITION_NAMES.get(position_code, position_code)


def main():
    args = parse_args()
    jersey_number = args.jersey_number

    console.print(
        f"[bold blue]NHL Jersey Lookup[/bold blue] — searching for #{jersey_number}..."
    )

    team_map = fetch_team_map()
    players = fetch_players_by_jersey(jersey_number)

    if not players:
        console.print(
            f"[yellow]No active NHL players found wearing #{jersey_number}.[/yellow]"
        )
        return

    players.sort(
        key=lambda player: (
            team_map.get(player["currentTeamId"], ""),
            player["lastName"],
        )
    )

    results_table = Table(title=f"Current NHL Players Wearing #{jersey_number}")
    results_table.add_column("Player")
    results_table.add_column("Team")
    results_table.add_column("Position")
    results_table.add_column("Player ID")

    for player in players:
        team_code = team_map.get(player["currentTeamId"], "???")
        results_table.add_row(
            player["fullName"],
            team_code,
            format_position(player["positionCode"]),
            str(player["id"]),
        )

    console.print()
    console.print(f"Found {len(players)} player(s).")
    console.print()
    console.print(results_table)


if __name__ == "__main__":
    main()
