# bot.py
import asyncio
import csv
import os
import random
from discord.ext import commands
import discord
from dotenv import load_dotenv
import emoji
import requests
from weather_time import get_calgary_weather
import wikipedia
import parse

load_dotenv(dotenv_path='bot_env.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')

intents = discord.Intents.all()

prefixes = 'boop.'
client = commands.Bot(command_prefix=prefixes, intents=intents)

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

@client.command()
async def doggo(ctx):
    rand = random.randint(1, 250)
    url = "http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true"
    response = requests.get(url)
    shiba = response.json()
    image_url = shiba[0]
    embed = discord.Embed(title="Doggo #"+str(rand), description="woof woof", color=0x00FF00)
    embed.set_image(url=image_url)
    await ctx.send(embed=embed)

@client.command()
async def touchGrass(ctx):
    message = get_calgary_weather()
    await ctx.send(message)

@client.command()
async def pokemon(ctx):
    rand = random.randint(1, 100)
    if rand < 35:
        response = requests.get('https://pokeapi.co/api/v2/pokemon?limit=890')
        pokemon_list = response.json()['results']
        random_pokemon = random.choice(pokemon_list)
        name = random_pokemon['name']
        id = random_pokemon['url'].split('/')[-2]
        image_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{id}.png'
        embed = discord.Embed(title=f'{name.capitalize()} #{id}', color=discord.Color.red())
        embed.set_image(url=image_url)
        await ctx.send(embed=embed)
        await ctx.send("Would you like to catch this pokemon?")

        catch_pokemon = await client.wait_for('message', timeout=30.0, check=lambda m: m.author == ctx.author and m.content.lower() in ['yes', 'no'])
        if catch_pokemon.content.lower() == "yes":
            rand = random.randint(1, 100)
            if rand > 50:
                file_path = f"pokemon_storage/{ctx.author.name}.csv"
                with open(file_path, mode="a", newline="") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows([[name]])
                await ctx.send(f"{name} has been caught and added to your pokemon storage. Type boop.pokepals to see all your captures so far!")
            else:
                await ctx.send(f"{name} broke out of the pokeball and ran away!")
        else:
            await ctx.send(f"{name} got away!")
    else:
        await ctx.send("You wandered and wandered the tall grass but no one came near...")

@client.command()
async def pokepals(ctx):
    file_path = f"pokemon_storage/{ctx.author.name}.csv"
    if os.path.exists(file_path):
        with open(file_path, mode="r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            pokemon_list = list(reader)
            if pokemon_list:
                embed = discord.Embed(title=f"{ctx.author.name}'s Pokemon", color=discord.Color.blue())
                for pokemon in pokemon_list:
                    name = pokemon[0]
                    embed.add_field(name=name, value="",inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send("No pokemon in storage :(")
    else:
        await ctx.send("You haven't caught any Pokemon yet!")

async def choose_pokemon(user, channel):
    file_path = f"pokemon_storage/{user.name}.csv"
    if not os.path.exists(file_path):
        await channel.send(f"{user.name} hasn't caught any Pokemon yet.")
        return

    with open(file_path, mode="r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        pokemon_list = list(reader)  # skip the header row

        if not pokemon_list:
            await channel.send(f"{user.name} hasn't caught any Pokemon yet.")
            return

        # Let the user choose a Pokemon to battle with
        embed = discord.Embed(title=f"{user.name}'s Pokemon", color=discord.Color.blue())
        await channel.send("Choose one of the following pokemon by entering its number <3")
        for i, pokemon in enumerate(pokemon_list):
            name = pokemon[0]
            embed.add_field(name=f"{i + 1}. {name}", value=" ", inline=False)

        await channel.send(embed=embed)

        def check(message):
            return message.author == user and message.channel == channel

        message = await client.wait_for('message', check=check)
        user_choice = int(message.content)
        if user_choice < 1 or user_choice > len(pokemon_list):
            await channel.send("Invalid choice. We will choose your first capture")
            user_choice = 1
        return pokemon_list[user_choice - 1][0]
    
def rip_pokemon(pokemon_name, file_path):
    with open(file_path, mode="r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    # Find the row corresponding to the losing pokemon and remove it
    for i, row in enumerate(rows):
        if row[0] == pokemon_name:
            del rows[i]
            break
    # Overwrite the CSV file with the updated list of rows
    with open(file_path, mode="w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    
@client.command()
async def battle(ctx, member: discord.Member):
    user_pokemon = await choose_pokemon(ctx.author, ctx.channel)
    other_user_pokemon = await choose_pokemon(member, ctx.channel)

    rand = random.randint(1, 100)
    await ctx.send(f"{user_pokemon} is battling {other_user_pokemon}!")
    await asyncio.sleep(2)
    if rand > 50:
        await ctx.send(f"{user_pokemon} won the battle! As a result, {other_user_pokemon} ran away from its owner!")
        file_path = f"pokemon_storage/{member.name}.csv"
        rip_pokemon(other_user_pokemon, file_path)
    else:
        await ctx.send(f"{other_user_pokemon} won the battle! As a result, {user_pokemon} ran away from its owner!")
        file_path = f"pokemon_storage/{ctx.author.name}.csv"
        rip_pokemon(other_user_pokemon, file_path)
    
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

    await client.process_commands(message) #so my commands can work
client.run(TOKEN)