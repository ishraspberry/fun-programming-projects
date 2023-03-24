import asyncio
import random
import discord

def cardsHit():
    cards = {"Ace":1, 
             "Two":2, 
             "Three":3, 
             "Four":4, 
             "Five":5, 
             "Six":6, 
             "Seven":7,
             "Eight":8,
             "Nine":9,
             "Ten":10,
             "Jack":10,
             "Queen":10,
             "King":10}
    chosen_one = random.choice(list(cards.keys()))
    return [chosen_one,cards[chosen_one]]


async def play(message, client):
    await message.channel.send(f'<@{message.author.id}>'+" Welcome to blackjack! Type 'hit' to draw a card, or 'stop' to end the game.")
    player = message.author
    stop_take_player = 0
    stop_take_bot = 0
    player_score = 0
    bot_score = 0
    while True:
        if message.author!= player:
            continue
        await message.channel.send("these are the scores so far: \n"+f'<@{message.author.id}>: '+str(player_score)+"\n me - "+str(bot_score))
        if player_score == 21 and bot_score == 21:
            await message.channel.send("We have tied! How unfortunate I wanted to beat you~")
            break
        elif player_score > 21 and bot_score > 21:
            await message.channel.send("Aw shucks looks like we both loose~")
            break
        elif player_score == 21:
            await message.channel.send("You win!! You should take on a gambling habit")
            break
        elif bot_score == 21:
            await message.channel.send("You lose I win nah nah nah boo boo")
            break
        elif stop_take_bot == 1 and stop_take_player == 1:
            await message.channel.send("Aw shucks looks like we both loose~")
            break
        if(stop_take_player == 0):
            reply = await client.wait_for("message", check=lambda m: m.author == message.author)
            if reply.content.lower() == "stop":
                stop_take_player += 1
                await message.channel.send("You gave in, but lets see what your competitor chooses")
            elif reply.content.lower() == "hit":
                cardDrawn = cardsHit()
                await message.channel.send("The dealer flips you this card: "+cardDrawn[0])
                player_score += cardDrawn[1]
            else:
                await message.channel.send("Please respond with 'hit' to draw a card or 'stop' to stop drawing")
                continue 

        if(stop_take_bot == 0):    
            await asyncio.sleep(2)
            await message.channel.send("\n\nMy turn~ la dee da~")
            await asyncio.sleep(2)

            if bot_score < 17:
                cardDrawn = cardsHit()
                await message.channel.send("I hit! The dealer flips me this card: "+cardDrawn[0])
                bot_score += cardDrawn[1]
            else:
                winning_chance = (21 - player_score) / 21
                # calculate the bot's chance of winning based on their current score
                bot_winning_chance = (21 - bot_score) / 21
                # if the bot has a higher chance of winning, draw another card
                if bot_winning_chance > winning_chance:
                    cardDrawn = cardsHit()
                    await message.channel.send("I hit! The dealer flips me this card: "+cardDrawn[0])
                    bot_score += cardDrawn[1]
                else:
                    await message.channel.send("I'm so stopping omg")
                    stop_take_bot += 1