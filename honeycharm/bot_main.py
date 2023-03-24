# bot.py
import os
import random
import unicodedata
from discord.ext import commands
import discord
from dotenv import load_dotenv
import emoji
import parse
import wikipedia

load_dotenv(dotenv_path='bot_env.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')

intents = discord.Intents.all()

client = discord.Client(intents=intents)
prefixes = 'play.'
bot = commands.Bot(command_prefix=prefixes, intents=intents)

talk_points = []
with open("list_of_reactions.txt", "r", encoding="utf8") as file:
    for line in file:
        if line != "\n":
            if line.endswith("\n"):
                line = line[:-1]
            talk_points.append(line)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#responding to a fellow user when mentioned :)
@client.event
async def on_message(message):
    print(message.content)
    if message.author == client.user:
        return
    if "honeycharm" in message.content.lower():
        try:
            emoji_list = list(emoji.EMOJI_DATA.keys())
            emoji_choice = random.choice(emoji_list)
            await message.add_reaction(emoji_choice)
        except discord.errors.HTTPException as e:
            await message.add_reaction("\U0001F600") # default emoji
    
    if message.content.lower().startswith('wikime'):
        args = message.content.split(" ")
        if len(args) < 2:
            await message.channel.send("Please enter a search term after `wiki`.")
            return
        item_search_title=" ".join(args[1:])
        try:
            item_summary=wikipedia.summary(item_search_title)
            item_summary_sentences = item_summary.split(". ")
            summary = ". ".join(item_summary_sentences[:3]) + "."
            embed=discord.Embed(title='Wikipedia Summary',description='',colour=discord.Colour.blue())
            embed.add_field(name=item_search_title.capitalize(),value=summary,inline=False)
            await message.channel.send(embed=embed)
        except wikipedia.exceptions.DisambiguationError as e:
            await message.channel.send(f"There were multiple results for `{item_search_title}`. Please enter a more specific search term.")
            return

    if message.content.startswith('!'):
        await parse.parseCommand(message, client)
        
    if f'<@{client.user.id}>' in message.content:
        response = f"{random.choice(talk_points)}"
        if response == "Hop off my dick pls <3":
            response = f"{random.choice(talk_points)} {message.author.mention}"
        await message.channel.send(response)
client.run(TOKEN)