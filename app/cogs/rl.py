import json
from pathlib import Path

import discord
from discord.ext import commands

from app.utils import print_table


class Rl(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__cog_name__} has loaded!')

    @commands.command(name='rl', help='Prints the ranking table')
    async def rl(self, ctx, p1: discord.Member, p2: discord.Member = None, p3: discord.Member = None):

        print('a')

        file_path_ranking = Path("./app/cogs/ranking.json").resolve()
        file_path_partners = Path("./app/cogs/partners.json").resolve()

        players = []

        with open(file_path_partners, "r") as f:
            partners = json.load(f)
            print('Loaded partners')

            for player in [p1, p2, p3]:
                print('entered first for')
                if player is None:
                    continue

                player_key = player.global_name if player.global_name not in [None, "null", "Null"] else player.display_name
                print('player_key first for')

                # Ensure the player exists in the structure
                if player_key not in partners['players']:
                    partners['players'][player_key] = {}

                for partner in [p1, p2, p3]:
                    if partner is None or partner == player:
                        print('second loop')
                        continue

                    print('second loop')

                    # Ensure the partner exists in the player's dictionary
                    if partner.global_name not in partners['players'][player_key]:
                        partners['players'][player_key][partner.global_name] = 0

                    partners['players'][player_key][partner.global_name] -= 1

        # Write the updated JSON back to the file
        with open(file_path_partners, "w") as f:
            json.dump(partners, f, indent=4)
            print('printed partners')


        with open(file_path_ranking, "r") as f:

            ranking = json.load(f)
            print('Loaded ranking')

            for player in [p1, p2, p3]:

                if player is None:
                    continue

                player_key = player.global_name if player.global_name not in [None, "null", "Null"] else player.display_name

                players.append(player_key)

                if player_key not in ranking['players']:

                    print(f'creating new table for player {player_key}')

                    ranking['players'][player_key] = {
                        "wins": 0,
                        "losses": 1,
                        "win_rate": 0.0,
                        "total_games": 1
                    }

                else:

                    ranking['players'][player_key]['losses'] += 1

                    wins = ranking['players'][player_key]['wins']

                    losses = ranking['players'][player_key]['losses']

                    total_games = wins + losses

                    win_rate = (wins / total_games) * 100

                    ranking['players'][player_key]['win_rate'] = round(win_rate, 2)

                    ranking['players'][player_key]['total_games'] = total_games


        file_path = Path("./app/cogs/ranking.json").resolve()

        with open(Path(file_path_ranking), "w") as f:
            print('writing json')
            json.dump(ranking, f, indent=4)
            print('wrote json')

        table_to_print = await print_table()

        # Respond with success message
        await ctx.send(
            f"Result registered: **{1} LOSS**\n"
            f"Players: {', '.join(players)}\n"
            f"{table_to_print}"
        )

async def setup(bot):
    await bot.add_cog(Rl(bot))


