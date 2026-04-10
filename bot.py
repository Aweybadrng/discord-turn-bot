# bot.py
# Discord Turn Rotation Bot
# Commands:
# !register -> Register as one of 4 players
# !next -> Move to next player's turn
# !list -> Show all players and current turn
# !reset -> Reset game

import os
import discord
from discord.ext import commands

# Load token from Railway environment variable
TOKEN = os.getenv("DISCORD_TOKEN")

# Enable Discord intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Game state
players = []
current_turn = 0
MAX_PLAYERS = 4


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def register(ctx):
    global players

    user = ctx.author

    # Prevent duplicate registration
    if user in players:
        await ctx.send(f"{user.mention}, you are already registered.")
        return

    # Limit to 4 players
    if len(players) >= MAX_PLAYERS:
        await ctx.send("Registration is full! 4 players already registered.")
        return

    players.append(user)

    await ctx.send(
        f"{user.mention} registered successfully! ({len(players)}/{MAX_PLAYERS})"
    )

    # Start game when all 4 joined
    if len(players) == MAX_PLAYERS:
        await ctx.send(
            f"All 4 players registered!\n"
            f"It is now {players[current_turn].mention}'s turn."
        )


@bot.command()
async def next(ctx):
    global current_turn

    if len(players) < MAX_PLAYERS:
        await ctx.send("Need exactly 4 players before starting turns.")
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


# Start bot safely
if TOKEN is None:
    print("ERROR: DISCORD_TOKEN is missing in Railway Variables.")
else:
    bot.run(TOKEN)
