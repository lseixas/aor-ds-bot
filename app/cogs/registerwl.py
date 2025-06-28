import json
import discord
from discord.ext import commands
from pathlib import Path
from app.utils import print_table

class Registerwl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__cog_name__} has loaded!')

    @commands.command(name='registerwl', help='Register win for at least 1 player and max 3 players')
    async def registerwl(
                self,
                ctx,
                quantity: int,
                result: str,
                p1: discord.Member,
                p2: discord.Member = None,
                p3: discord.Member = None
            ):
        # Validate the `result` parameter
        if result.lower() not in ["win", "loss"]:
            await ctx.send("Invalid result! Please use 'win' or 'loss'.")
            return

        players = []

        print('before json')

        file_path_ranking = Path("./app/repo/season2/ranking.json").resolve()
        file_path_partners = Path("./app/cogs/partners.json").resolve()

        with open(file_path_partners, "r") as f:
            partners = json.load(f)
            print('Loaded partners')

            for player in [p1, p2, p3]:
                if player is None:
                    continue

                player_key = player.global_name if player.global_name not in [None, "null", "Null"] else player.display_name

                # Ensure the player exists in the structure
                if player_key not in partners['players']:
                    partners['players'][player_key] = {}

                for partner in [p1, p2, p3]:
                    if partner is None or partner == player:
                        continue

                    # Ensure the partner exists in the player's dictionary
                    if partner.global_name not in partners['players'][player_key]:
                        partners['players'][player_key][partner.global_name] = 0

                    # Update the value based on the result
                    if result == 'win':
                        partners['players'][player_key][partner.global_name] += quantity
                    else:
                        partners['players'][player_key][partner.global_name] -= quantity

        # Write the updated JSON back to the file
        with open(file_path_partners, "w") as f:
            json.dump(partners, f, indent=4)
            print('Updated partners JSON')


        with open(file_path_ranking, "r") as f:

            print('opened json')

            ranking = json.load(f)

            print('loaded json')

            for player in [p1, p2, p3]:

                print('iterate')

                if player is None:
                    continue

                player_key = player.global_name if player.global_name not in [None, "null", "Null"] else player.display_name

                players.append(player_key)

                if player_key not in ranking['players']:

                    print(f'creating new table for player {player_key}')

                    ranking['players'][player_key] = {
                        "wins": 0 if result == "loss" else quantity,
                        "losses": 0 if result == "win" else quantity,
                        "win_rate": 0.0 if result == "loss" else 100.0,
                        "total_games": quantity
                    }

                else:
                    if result.lower() == "win":
                        print('appending win')
                        ranking['players'][player_key]['wins'] += quantity
                        print('appended win')
                    else:
                        print('appending loss')
                        ranking['players'][player_key]['losses'] += quantity
                        print('appended loss')

                    wins = ranking['players'][player_key]['wins']
                    losses = ranking['players'][player_key]['losses']
                    total_games = wins + losses
                    win_rate = (wins / total_games) * 100
                    ranking['players'][player_key]['win_rate'] = round(win_rate, 2)
                    ranking['players'][player_key]['total_games'] = total_games


        file_path = Path("./app/cogs/ranking.json").resolve()

        with open(Path(file_path), "w") as f:
            print('writing json')
            json.dump(ranking, f, indent=4)
            print('wrote json')

        table_to_print = await print_table()

        # Respond with success message
        await ctx.send(
            f"Result registered: **{quantity} {result.upper()}**\n"
            f"Players: {', '.join(players)}\n"
            f"{table_to_print}"
        )

async def setup(bot):
    await bot.add_cog(Registerwl(bot))
