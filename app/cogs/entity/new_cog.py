from discord.ext import commands
from pathlib import Path

class NewCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.file_path_ranking = Path("./app/repo/season2/ranking.json").resolve()
        self.file_path_partners = Path("./app/cogs/commands/partners.json").resolve()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'{self.__cog_name__} has loaded!')