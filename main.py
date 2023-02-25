import discord
import yaml

from discord.ext import commands

import connect4 as c4
from game_client import Connect4Client as c4c

with open("./env/variables.yaml", "r") as f:
    variables = yaml.safe_load(f)

TOKEN = variables["token"]

session = {
    "mode": "default",
    "channel_id": None,
    "env": None,
    "env_client": None,
    "env_msg_id": None
}

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

def reset_to_default():
    session["mode"] = "default"
    session["channel_id"] = None
    session["env"] = None
    session["env_client"] = None
    session["env_msg_id"] = None

### Start ###
@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')

### Connect Four ###
@bot.command(aliases=["c4", "connectfour"])
async def connect4(ctx):
    if session["mode"] == "default":
        session["mode"] = "connect4"

        session["env"] = c4.Game()
        session["env_client"] = c4c()

        status, board = session["env_client"].start(session["env"])

        embed = discord.Embed(
            description=board
        )
        if status == 0:
            piece = session["env_client"].display_symbols["o"]
        elif status == 1:
            piece = session["env_client"].display_symbols["x"]
        embed.add_field(name="Turn", value=piece, inline=False)
        embed.set_footer(text="!reset, !quit")

        # send game message
        message = await ctx.send(embed=embed)

        # save game message id
        session["env_msg_id"] = message.id

        # init reactions for game message
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]
        for emoji in emojis:
            await message.add_reaction(emoji)

@bot.event
async def on_raw_reaction_add(payload):
    if session["mode"] == "connect4":
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣"]

        # if reaction was added to game message
        if payload.message_id == session["env_msg_id"]:
            if str(payload.emoji) in emojis and payload.user_id != bot.user.id:
                # find game message
                channel = bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)

                status, board = session["env_client"].play(session["env"], int(str(payload.emoji)[0])-1)

                if status in [0, 1]:
                    # new embed with updated game
                    embed = discord.Embed(
                        description=board
                    )
                    if status == 0:
                        piece = session["env_client"].display_symbols["o"]
                    elif status == 1:
                       piece = session["env_client"].display_symbols["x"]
                    embed.add_field(name="Turn", value=piece, inline=False)
                    embed.set_footer(text="!reset, !quit")

                    # update game message
                    await message.edit(embed=embed)

                    # remove reaction after it has been used
                    user = await bot.fetch_user(payload.user_id)
                    await message.remove_reaction(payload.emoji, user)
                elif status in [2, 3]:
                    # new embed with updated game
                    embed = discord.Embed(
                        description=board
                    )
                    if status == 2:
                        winner = session["env_client"].display_symbols["o"]
                    elif status == 3:
                        winner = session["env_client"].display_symbols["x"]
                    embed.add_field(name="Winner", value=winner, inline=False)
                    embed.set_footer(text="!ds for new game")

                    # update game message and clear reactions
                    await message.edit(embed=embed)
                    await message.clear_reactions()

                    reset_to_default()
                elif status == 4:
                    # new embed with updated game
                    embed = discord.Embed(
                        description=board
                    )
                    embed.add_field(name="Draw", value="", inline=False)
                    embed.set_footer(text="!ds for new game")

                    # update game message and clear reactions
                    await message.edit(embed=embed)
                    await message.clear_reactions()

                    reset_to_default()

bot.run(TOKEN)