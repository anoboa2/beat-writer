import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents=discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print('Monkey is ready.')

@bot.command(aliases=['hi'])
async def write(ctx, *names):
  print(ctx.author, ctx.message.content)
  await ctx.send(f'Hello {names}!')

@bot.command()
async def ping(ctx):
  print(ctx.message.author, ctx.message.content)
  await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run(DISCORD_TOKEN)