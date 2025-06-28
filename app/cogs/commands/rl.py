import json
from pathlib import Path
import discord
from discord.ext import commands
from app.utils import print_table
from ..entity.new_cog import NewCog


class Rl(NewCog):

    #inicializa super classe passando a instancia do bot
    def __init__(self, bot):
        super().__init__(bot)

    #estrutura da mensagem do comando, prefixo e descrição
    @commands.command(name='rl', help='Prints the ranking table')
    async def rl(self, ctx, p1: discord.Member, 
                            p2: discord.Member = None, 
                            p3: discord.Member = None,
                            p4: discord.Member = None,
                            p5: discord.Member = None):

        print('a')

        players = []

        #abrindo o arquivo de rankeamento com caminho definido na superclasse
        with open(self.file_path_ranking, "r") as f:
            partners = json.load(f)
            print('Loaded partners')

            #registrando para cada player
            for player in [p1, p2, p3, p4, p5]:
                print('entered first for')

                #caso o player nao foi passado continua o for
                if player is None:
                    continue

                #pegando o nome / key do player
                #TODO implementar o sistema de multiplos nomes para facilitar o registro
                player_key = player.global_name if player.global_name not in [None, "null", "Null"] else player.display_name
                print('player_key first for')

                #inicializa a key do player no json caso nao exista
                if player_key not in partners['players']:
                    partners['players'][player_key] = {}

                #loop para registro de wl com parceiros
                for partner in [p1, p2, p3, p4, p5]:
                    #caso p seja nulo (nao tenha sido passado)
                    if partner is None or partner == player:
                        print('second loop')
                        continue

                    print('second loop')

                    #registrando a key caso nao exista
                    if partner.global_name not in partners['players'][player_key]:
                        partners['players'][player_key][partner.global_name] = 0

                    #registrando a derrota com respectivo parceiro
                    partners['players'][player_key][partner.global_name] -= 1

        #subescrevendo o json de parceiros
        with open(self.file_path_partners, "w") as f:
            json.dump(partners, f, indent=4)
            print('printed partners')

        #abrindo o arquivo ranking para registrar derrota na tabela
        #TODO unir dentro de um unico open o registro de parceiros e tabela
        with open(self.file_path_ranking, "r") as f:

            #abrindo o json como uma variavel dicionario
            ranking = json.load(f)
            print('Loaded ranking')

            #loop para cada player
            for player in [p1, p2, p3, p4, p5]:

                #caso nulo
                if player is None:
                    continue

                #pegando a key/nome do player passado
                player_key = player.global_name if player.global_name not in [None, "null", "Null"] else player.display_name

                #TODO ???
                players.append(player_key)

                #caso nao tenha a key inicializa uma nova
                if player_key not in ranking['players']:

                    print(f'creating new table for player {player_key}')

                    ranking['players'][player_key] = {
                        "wins": 0,
                        "losses": 1,
                        "win_rate": 0.0,
                        "total_games": 1
                    }

                #caso ja tenha, registra os dados na tabela
                else:

                    ranking['players'][player_key]['losses'] += 1

                    wins = ranking['players'][player_key]['wins']

                    losses = ranking['players'][player_key]['losses']

                    total_games = wins + losses

                    win_rate = (wins / total_games) * 100

                    ranking['players'][player_key]['win_rate'] = round(win_rate, 2)

                    ranking['players'][player_key]['total_games'] = total_games


        #TODO ??? unir isso com o open de cima
        file_path = Path("./app/cogs/ranking.json").resolve()

        with open(Path(self.file_path_ranking), "w") as f:
            print('writing json')
            json.dump(ranking, f, indent=4)
            print('wrote json')

        #metodo de printar a tabela vindo do utils
        table_to_print = await print_table()

        #registra strings para a mensagem de resposta ao discord
        await ctx.send(
            f"Result registered: **{1} LOSS**\n"
            f"Players: {', '.join(players)}\n"
            f"{table_to_print}"
        )

async def setup(bot):
    #adicionar o cog ao bot
    await bot.add_cog(Rl(bot))


