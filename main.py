import os
import discord
import json
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from writeContent import writePregameHit, identifyNames, generateTalkingPoints

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents=discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
  print('Monkey is ready.')

@bot.command()
async def matchup(ctx, *names):
    if len(names) != 2:
      await ctx.send("You gave me more than two names.  They can't all be playing each other today!")
      return
    
    # Identify the names
    identified_names = identifyNames(names, 'leagueTeams.json')
    name_objects = []
    for name in identified_names:
      try:
        name = json.loads(name)
        name_objects.append(name)
      except:
        await ctx.send("I'm not sure what teams you're talking about...  Please try again.")
        return
      
    # Generate talking points about each team
    await ctx.send("I've been working on that piece for a little while... Let me finish the final edits and get that out to you :monkey:")
    talking_points = await asyncio.to_thread(generateTalkingPoints, name_objects)
    if isinstance(talking_points, str):
      await ctx.send(talking_points)
      return
      
    # Write the pregame hit
    await ctx.send(":monkey: :monkey: Just one more moment... :monkey: :monkey:")
    response = await asyncio.to_thread(writePregameHit, talking_points)

    # seperate the response into chunks by looking for 2 new lines as the delimiter
    chunks = response.split('\n\n')
    for chunk in chunks:
      await ctx.send(chunk)
      await asyncio.sleep(1)

    await ctx.send("**Done!**")
    return

@bot.command()
async def ping(ctx):
  print(ctx.message.author, ctx.message.content)
  await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

bot.run(DISCORD_TOKEN) # type: ignore