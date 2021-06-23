import discord
import random
import time
import asyncio
import os
import AniListAPI
import CheckingMangaUpdates
import json5
from discord.ext import commands

wishes = ["Ayano Tateyama", "Alpha (RW)", "Kainé", "Yonah", "Devola", "Popola", "Zero (DOD3)", "Helvi", "Yuri Shibasawa", "Aoe Nagi", "Yuko Kurose"]
TOKEN = "YOUR TOKEN HERE"
romcoms = ['Kubo-san wa Mob wo Yurusanai', 'Sakurai-san wa Kizuite Hoshii', "Nega-kun to Poji-chan",
"Kimi no Koto ga Dai Dai Dai Dai Daisuki na 100-nin no Kanojo", "Kanojo mo Kanojo"]
targetuser = 0
# client = discord.Client()
AniList = AniListAPI.AniListAPI
MangaUpdates = CheckingMangaUpdates.manga_updates
bot = commands.Bot(command_prefix=['kubo', 'amo', 'su', 'lis'])

# @client.event
# async def on_ready():
#     print('Hello')
#
# @client.event
# async def on_message(message):
    # if message.content.startswith('$h'):
    #     await message.channel.send('Hello')
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

@bot.listen()
async def on_message(message):
    try:
        if message.author.id == 432610292342587392:
            embeds = message.embeds

            for embed in embeds:
                want = embed.to_dict()

            for wish in wishes:
                if want.get('author').get('name') == wish:
                    await message.add_reaction("😳")
    except:
        print("was not your wish")

# @bot.listen()
# async def on_message(message):
#     if message.author.id == targetuser:
#         await message.add_reaction(':PepeYikes:818672594718163004')

@bot.command()
async def react(ctx, user: discord.Member):
    global targetuser
    print(user.id)
    if user.id == targetuser:
        targetuser = 0
        print(targetuser)
    else:
        targetuser = user.id
        print(targetuser)

# @bot.command()
# async def s(ctx):
#     await ctx.message.add_reaction(':PepeYikes:818672594718163004')
#
# @bot.event
# async def kubohelp(ctx):
#     await ctx.send('```$getinfo {manga name} - get Reviews and notlaD\'s recommendation on a certain manga'
#                    '\n...work in progress...```')

@bot.command()
async def ts(ctx):
    await ctx.send('Here are notlaD\'s current Top Manga Lists:'
                   '\n1. romcoms'
                   '\n2. Psychological'
                   '\n3. Story Rich'
                   '\n4. Fun/Adventurous'
                   '\n5. 18+'
                   '\nUse command "list {genre}" to see the list')

@bot.command()
async def getupdate(ctx, *, manganame):
    chapter, url = MangaUpdates.getupdate(manganame)
    update = manganame + " is currently on chapter " + chapter
    embed = discord.Embed(title='Manga Updates!', color=0x00aaff)
    embed.set_footer(text='Dpang certified')
    embed.add_field(name='The Update', value=update)
    embed.add_field(name='Link', value="[Read Here](https://manganelo.com/{})".format(url))
    await ctx.send(embed=embed)

@bot.command()
async def t(ctx, genre):
    result = ''
    if genre == 'romcoms':
        for manga in romcoms:
            result += manga + "\n"
        embed = discord.Embed(title=':heart_decoration: RomComs :heart_decoration: ', color=0x00aaff)
        embed.set_footer(text='Dpang certified')
        embed.add_field(name='My Top RomComs', value=result)

    await ctx.send(embed=embed)

@bot.command()
async def honorcode(ctx):
    await ctx.send("I pledge on my honor that I have not given or received any "
                   "unauthorized assistance on this assignment")

@bot.command()
async def cchi(ctx):
    kubofolder = 'kubo'
    kubo_image = random.choice(os.listdir(r"C:\Users\Dalton\PycharmProjects\DiscordBot\kubo"))
    await ctx.send(file=discord.File('kubo/' + kubo_image))

@bot.command()
async def gus(ctx):
    await ctx.message.add_reaction(':PepeYikes:818672594718163004')

@bot.command()
async def gabus(ctx):
    await ctx.send(file=discord.File('Memes/gabusanilist.mp4'))

@bot.command()
async def zek(ctx):
    await ctx.send('<@394927383637000195>')
    await ctx.send(file=discord.File('Memes/zek.mp4'))

@bot.command(help='returns status of bot')
async def ping(ctx):
    ping = bot.latency
    await ctx.send('pong ('+str(int(1000*ping))+'ms)')

@bot.command()
async def getinfo(ctx, *, manganame):
    title, score, image = AniList.getinfo(manganame)
    print(score)
    with open('reviews.json') as f:
        review_data = json5.load(f)

    with open('recommendations.json') as f:
        rec_data = json5.load(f)

    reviews = ''

    for author in review_data:
        try:
            reviews += review_data[author][str(title)] + '\n' + '-' + author + '\n'
        except:
            reviews += ""
            continue

    try:
        rec = rec_data[str(title)]
    except:
        rec = " "

    if not reviews:
        reviews = 'No Reviews'

    score = str(int(score / 10)) + "/10"
    if score.__eq__('0/10'):
        score = "Have Not Read"
    embed = discord.Embed(title= ':star2:' + title + ':star2:', color=0x00aaff)
    embed.set_thumbnail(url=image)
    embed.set_footer(text='Dpang certified')
    embed.add_field(name='Review', value=reviews)
    embed.add_field(name='notlaD\'s Recommendation', value=rec + '\n' + score)
    await ctx.send(embed=embed)

@bot.command()
async def setreview(ctx, *, manganame):
    title, score, image = AniList.getinfo(manganame)
    # manganame = ''.join(manganame)
    await ctx.send('The next line you type will be your review for ' + title + ', you have 60 seconds to type it:')

    review = await bot.wait_for('message', check=check(ctx.author), timeout=60)

    await ctx.send(review.content)
    # already have review variable
    review_dict = {}
    with open('reviews.json') as f:
        review_dict = json5.load(f)

    author = ctx.author.name

    # dont need to check if the user (author) is in there bc the following
    # line will auto create the key:val pair if its not in there, otherwise itll update it
    if review_dict.get(author, None) is not None: # dict of reviews for the user
        reviews = review_dict[author]
    else:
        review_dict[author] = {}
        reviews = review_dict[author]

    # same deal here, it'll just create a new entry if non-existent and overrides the existing
    # review of showname if it already existed
    reviews[title] = review.content

    review_dict[author] = reviews

    jsonfile = json5.dumps(review_dict)
    f = open("reviews.json", "w")
    f.write(jsonfile)
    f.close()

@bot.command()
async def setrec(ctx, *, manganame):
    title, score, image = AniList.getinfo(manganame)
    if ctx.author.id == 192767908852531201:
        await ctx.send('The next line you type will be the recommendation for ' + title + ', you have 60 seconds to type it:')
        rec = await bot.wait_for('message', check=check(ctx.author), timeout=60)
        rec_dict = {}

        with open('recommendations.json', 'r') as f:
            rec_dict = json5.load(f)
            rec_dict[title] = rec.content
            f.close()

        with open('recommendations.json', 'w') as f:
            json5.dump(rec_dict, f)
            f.close()
    else:
        await ctx.send("You are unauthorized to use this command")


def check(author):
    def inner_check(message):
        return message.author == author and message.content != ""

    return inner_check

# @bot.command()
# async def make_json(ctx):
#     json_obj = {}
#     with open('reviews.json', 'w') as jsonFile:
#         json5.dump(json_obj, jsonFile)

bot.run(TOKEN)


