# bot.py
# Discord Turn Rotation Bot
# Commands:
# !register -> Register as one of 5 players
# !next -> Move to next player's turn
# !list -> Show all players and current turn
# !reset -> Reset game

import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

players = []
current_turn = 0
MAX_PLAYERS = 5  # ✅ changed to 5


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def register(ctx):
    global players

    user = ctx.author

    if user in players:
        await ctx.send(f"{user.mention}, you are already registered.")
        return

    if len(players) >= MAX_PLAYERS:
        await ctx.send(f"Registration is full! {MAX_PLAYERS} players already registered.")
        return

    players.append(user)

    await ctx.send(
        f"{user.mention} registered successfully! ({len(players)}/{MAX_PLAYERS})"
    )

    if len(players) == MAX_PLAYERS:
        await ctx.send(
            f"All {MAX_PLAYERS} players registered!\n"
            f"It is now {players[current_turn].mention}'s turn."
        )


@bot.command()
async def next(ctx):
    global current_turn

    if len(players) < MAX_PLAYERS:
        await ctx.send(f"Need exactly {MAX_PLAYERS} players before starting turns.")
        return

    current_turn = (current_turn + 1) % MAX_PLAYERS

    await ctx.send(
        f"It is now {players[current_turn].mention}'s turn."
    )


@bot.command()
async def list(ctx):
    if len(players) == 0:
        await ctx.send("No players registered yet.")
        return

    message = "**Registered Players:**\n"

    for i, player in enumerate(players):
        if len(players) == MAX_PLAYERS and i == current_turn:
            message += f"{i+1}. {player.name} ← CURRENT TURN\n"
        else:
            message += f"{i+1}. {player.name}\n"

    await ctx.send(message)


@bot.command()
async def reset(ctx):
    global players, current_turn

    players = []
    current_turn = 0

    await ctx.send("Game reset. All players cleared.")


if TOKEN is None:
    print("ERROR: DISCORD_TOKEN is missing in Railway Variables.")
else:
    bot.run(TOKEN)
