import discord
import random
import time
import asyncio
import AniListAPI
from discord.ext import commands

TOKEN = "ODIxNTU4NzEyNDQyOTQ1NTQ3.YFFeLA.HRAjVsncSHQ-6RgmldKnVXAFaEg"
# client = discord.Client()
AniList = AniListAPI.AniListAPI
bot = commands.Bot(command_prefix='$')

# @client.event
# async def on_ready():
#     print('Hello')

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('$h'):
#         await message.channel.send('Hello')
#
#     if message.content.startswith('!kubo'):
#         await message.channel.send(':star2:Kubo-san wa Boku (Mobu) wo Yurusanai:star2:')
#         await message.channel.send(file=discord.File('pics/kubomanga.jpg'))
#
#     if message.content.startswith('!kub'):
#         title, score, image = AniList.getinfo(112981)
#         await message.channel.send(title)
@bot.event
async def on_ready():
    print('Manga Bot Activated')

@bot.command()
async def getinfo(ctx, mangaid):
    title, score, image = AniList.getinfo(mangaid)
    score = str(int(score / 10)) + "/10"
    embed=discord.Embed(title= ':star2:' + title + ':star2:', color=0x00aaff)
    embed.set_image(url=image)
    embed.set_footer(text=score)
    await ctx.send(embed=embed)

bot.run(TOKEN)
