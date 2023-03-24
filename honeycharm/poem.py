import requests
from bs4 import BeautifulSoup
import discord
import random
async def poem(message):
    while True:
        response = requests.get('https://poetrydb.org/random')
        if response.status_code == 200:
            poem = response.json()[0]
            lines = poem['lines']
            if int(poem['linecount']) < 20:
                async with message.channel.typing():
                    title = poem['title']
                    poem_text = '\n'.join(lines)
                    await message.channel.send("**"+title+"**"+"\n\n"+poem_text)
                    break
            else:
                print
                continue
        else:
            continue