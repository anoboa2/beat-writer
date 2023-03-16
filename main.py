import os
import discord
import openai
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
    ingredients_string = " ".join(names)

    # Make API call to GPT for recipe
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Please suggest a chicken-based recipe that includes {names}.",
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Get recipe from API response
    recipe = response.choices[0].text.strip()

    # Send recipe to Discord channel
    await ctx.send(f"Here's a recipe that includes {ingredients_string}: {recipe}")

@bot.command()
async def ping(ctx):
  print(ctx.message.author, ctx.message.content)
  await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run(DISCORD_TOKEN)