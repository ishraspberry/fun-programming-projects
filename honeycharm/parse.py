import random
import poem
import blackjack
import discord

async def parseCommand(message, client):
    if message.content.startswith('!poem'):
        try:
            await poem.poem(message)
        except Exception as e:
            print(e)
    elif message.content.startswith('!blackjack'):
        try:
            await blackjack.play(message, client)
        except Exception as e:
            print(e)
    elif message.content.startswith('!botstop'):
        await client.close()
    elif message.content.startswith('!shake'):
        words = message.content.split()
        if len(words) < 3:
            await message.channel.send("Invalid command. Usage: `!fixup @discord_user new_nickname name`")
            return
        member = message.mentions[0]
        new_name = " ".join(words[2:])
        await member.edit(nick=new_name)

        # Send a confirmation message
        await message.channel.send(f"Changed {member.mention}'s nickname to {new_name}")
    
    elif message.content.startswith('!badcharm'):
        if not message.mentions:
            await message.channel.send("Please make sure you mention the person I gotta curse")
            return
        member = message.mentions[0]
        await member.create_dm()
        response = "SPAMMMM"
        x = 0
        while x < 13:
            await member.dm_channel.send(response)
            x += 1
        await message.channel.send(f"get SPAMMED {member.mention}")