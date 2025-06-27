
import json
from pathlib import Path

async def print_table():
    table_output = "```"
    table_output += "\nPlayers:\n"
    header = f"{'Player':<24} {'Wins':<5} {'Losses':<7} {'Win Rate':<10} {'Total Games':<8}"
    table_output += f"{header}\n"
    table_output += "-" * len(header) + "\n"

    try:
        print('tried printing')

        with open(Path("./app/cogs/ranking.json"), "r") as f:
            ranking = json.load(f)
            if ranking.get('players') is None:
                ranking['players'] = {}

            # Sort players by win rate (descending), handle missing win rates
            sorted_players = sorted(
                ranking['players'].items(),
                key=lambda item: item[1].get("win_rate", 0.0),
                reverse=True  # Descending order
            )

            for player, data in sorted_players:
                wins = data.get("wins", 0)
                losses = data.get("losses", 0)
                total_games = wins + losses  # Compute total games dynamically
                win_rate = round((wins / total_games) * 100, 2) if total_games > 0 else 0.0
                table_output += f"{player:<24} {wins:<5} {losses:<7} {win_rate:<10} {total_games:<8}\n"

        table_output += "```"
        return table_output  # Return the formatted string for Discord

    except FileNotFoundError:
        return "JSON file not found!"
    except json.JSONDecodeError:
        return "Error decoding JSON!"

