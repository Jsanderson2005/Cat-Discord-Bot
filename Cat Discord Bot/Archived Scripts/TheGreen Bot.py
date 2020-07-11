import discord
import math
from discord.ext import commands
import os
import praw
import random
from googlesearch import search
#from CatDetector import CatDetector
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import requests
from scipy import misc
import imageio
import io
import urllib.request
import numbers
import decimal

bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
reddit = praw.Reddit(client_id='o7-kUtRSpT3iKA', client_secret='WLCfuJD6XJVSke9C979n1b-1_bI', user_agent='DISCORD:The green bot: version 1.0 (by /u/joshiwoshi2005)')

np.set_printoptions(suppress=True)
model = tensorflow.keras.models.load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

#VOltage drop from a wire
@bot.command()
async def drop(ctx, length: int, current: int, diameter: int):
    area = math.pi * (diameter / 2) * (diameter / 2)
    volts = (length * current * 0.017) / area

    string = str(volts)

    drop = discord.Embed(
        title='Voltage drop:',
        description=string,
        colour=discord.Colour.blue())
    drop.set_footer(text='The green bot. Prefix = !')
    drop.set_author(
        name="Voltage drop calculator",
        icon_url=
        "https://media.discordapp.net/attachments/637336145575018498/645256795282997248/Screenshot_2019-11-16_at_13.39.46.png"
    )
    drop.add_field(name="Length:", value=length, inline=False)
    drop.add_field(name="Current:", value=current, inline=False)
    drop.add_field(name="diameter:", value=diameter, inline=False)

    await ctx.send(embed=drop)

    #await ctx.send("The amount of voltage you will drop is: {}".format(volts))

#Help command
@bot.command()
async def help(ctx):
    hlp = discord.Embed(
        title='Help',
        description='Shows help commands',
        colour=discord.Colour.blue())
    hlp.set_footer(text='The green bot. Prefix = !')
    hlp.set_author(
        name="The Green Bot Commands",
        icon_url=
        "https://media.discordapp.net/attachments/637336145575018498/645256795282997248/Screenshot_2019-11-16_at_13.39.46.png"
    )
    hlp.add_field(
        name="drop",
        value=
        "Calculates a voltage drop across wires. Template: !drop [length (m)] [current (a)] [diameter (mm)]",
        inline=False)
    hlp.add_field(
        name="binary",
        value=
        "Changes the decimal to binary. Template: !binary [decimal]",
        inline=False)
    hlp.add_field(
        name="delay",
        value=
        "Calculates delay for speakers in dry air, at 20 degress celsius: !binary [Distance from main speakers (m)]",
        inline=False)
    hlp.add_field(
        name="bridle",
        value=
        "Calculates bridle angles and lengths. Template: !drop [span (m)] [offset (m)] [height (m)]",
        inline=False)
    hlp.add_field(
        name="hot",
        value=
        "Shows what is hot right now on r/techtheatre Template: !hot",
        inline=False)
    hlp.add_field(
        name="CatDetector",
        value=
        "Detects the pet in your photo: cat, dog or other.",
        inline=False)
    await ctx.send(embed=hlp)

#Number to binary for DIM switches
@bot.command()
async def binary(ctx, decimal: int):
    if decimal == 512:
        binary = str("{0:b}".format(decimal))
        reverse = binary[::-1]
        din = discord.Embed(
          title='Decimal',
          description='Your origial decimal: {}'.format(decimal),
        colour=discord.Colour.blue())
        din.set_footer(text='The green  bot. Prefix = !')
        din.set_author(
          name="Calculates Binary",
          icon_url=
          "https://media.discordapp.net/attachments/637336145575018498/645256795282997248/Screenshot_2019-11-16_at_13.39.46.png"
        )
        din.add_field(
          name="Binary",
          value=
          "Your binary is: {}".format(binary),
          inline=False)
        din.add_field(
          name="DIN switches",
          value=
          "Your din switch should look like this: 000000000 (0 = off, 1 = on) (Please note that if your switch has more switches, keep the rest at 0)".format(reverse),
          inline=False)
        await ctx.send(embed=din)
    elif decimal <= 511:
        num = int(decimal)
        binary = str("{0:b}".format(num))
        reverse = binary[::-1]
        din = discord.Embed(
          title='Decimal',
          description='Your origial decimal: {}'.format(decimal),
        colour=discord.Colour.blue())
        din.set_footer(text='The green  bot. Prefix = !')
        din.set_author(
          name="The Green Bot",
          icon_url=
          "https://media.discordapp.net/attachments/637336145575018498/645256795282997248/Screenshot_2019-11-16_at_13.39.46.png"
        )
        din.add_field(
          name="Binary",
          value=
          "Your binary is: {}".format(binary),
          inline=False)
        din.add_field(
          name="DIN switches",
          value=
          "Your din switch should look like this: {} (0 = off, 1 = on) (Please note that if your switch has more switches, keep the rest at 0)".format(reverse),
          inline=False)
        await ctx.send(embed=din)
    else:
        await ctx.send("You have inputted a number over 512! Try again!")


#Calculates Speaker Delays
@bot.command()
async def delay(ctx, delay: int):
  Ds = delay/343*1000
  dl = discord.Embed(
      title='The distance between the main speakers and the delays: '.format(delay),
      description='Distance: {}m'.format(delay),
      colour=discord.Colour.blue())
  dl.set_footer(text='The green bot. Prefix = !')
  dl.set_author(
      name="Calculates a delay with dry air at 20 degrees celcius",
      icon_url=
        "https://media.discordapp.net/attachments/637336145575018498/645256795282997248/Screenshot_2019-11-16_at_13.39.46.png"
    )
  dl.add_field(
      name="Delay:",
      value=
       "Your delay is: {}miliseconds".format(Ds),
        inline=False)
  await ctx.send(embed=dl)

#Bridle Calculations
@bot.command()
async def bridle(ctx, span: int, offset: int, height: int):
  FixLeft = math.sqrt(offset*offset+height*height)
  offsetRight = span-offset
  FixRight = math.sqrt(offsetRight*offsetRight+height*height)
  AngleOne = math.degrees(math.atan(offset/height))
  AngleTwo = math.degrees(math.atan(offsetRight/height))
  Totalangle = AngleOne + AngleTwo
  dl = discord.Embed(
      title='The angle is:',
      description='{}'.format(Totalangle),
      colour=discord.Colour.blue())
  dl.set_footer(text='The green bot. Prefix = !')
  dl.set_author(
      name="Calculates bridle angle and 'leg' lengths",
      icon_url=
        "https://media.discordapp.net/attachments/637336145575018498/645256795282997248/Screenshot_2019-11-16_at_13.39.46.png"
    )
  dl.add_field(
      name="Fix Left (m)",
      value=
      FixLeft,
        inline=False)
  dl.add_field(
      name="Fix Right (m)",
      value=
      FixRight,
        inline=False)
  await ctx.send(embed=dl)

#Playing Status
@bot.command()
async def playing(ctx, *activ):
  await bot.change_presence(activity=discord.Game(name=" ".join(activ[:])))

#What is hot on reddit
@bot.command()
async def hot(ctx):
  for submission in reddit.subreddit('techtheatre').hot(limit=random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])):
    title = submission.title
    description = submission.score
    url = submission.url
  dl = discord.Embed(
      title=title,
      description='{}'.format(url),
      colour=discord.Colour.blue())
  dl.set_footer(text='The green bot. Prefix = !')
  dl.set_author(
      name="Shows what is hot right now on reddit",
      icon_url=
        "https://media.discordapp.net/attachments/637336145575018498/645256795282997248/Screenshot_2019-11-16_at_13.39.46.png"
    )
  await ctx.send(embed=dl)

@bot.command()
async def search(ctx, *arg):       
  dl = discord.Embed(
      title='Your search results:',
      description='',
      colour=discord.Colour.blue())
  dl.set_footer(text='The green bot. Prefix = !')
  dl.set_author(
      name="Googles stuff",
      icon_url=
        "https://media.discordapp.net/attachments/637336145575018498/645256795282997248/Screenshot_2019-11-16_at_13.39.46.png"
    )
  for i in search(arg,        # The query you want to run
                tld = 'com',  # The top level domain
                lang = 'en',  # The language
                num = 5,     # Number of results per page
                start = 0,    # First result to retrieve
                stop = None,  # Last result to retrieve
                pause = 2.0,  # Lapse between HTTP requests
               ):
      dl.add_field(
          name="",
          value=i,
            inline=False)
  await ctx.send(embed=dl)
  
@bot.command()
async def role(ctx, *arg):  
       await ctx.send("This command is under construction, Check it out later!")

@bot.command()
async def CatDetector(ctx, *arg):  
        imageLink = ctx.message.attachments[0].url
        opener = urllib.request.URLopener()
        opener.addheader('User-Agent', 'Mozilla/5.0')
        filename, headers = opener.retrieve(imageLink, 'Pet.jpg')
        image = imageio.imread("Pet.jpg")
        print("Image Read")
        image = Image.open('Pet.jpg')
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        prediction = model.predict(data)
        print("Image {} has been predicted:".format(imageLink))
        print(prediction)
        #[[0. 1. 0.]]
        prediction = str(prediction)
        #['[''0''.'' ''1''.'' ''0''.'']']
        print(prediction)
        temp = ""
        cat = ""
        dog = ""
        other = ""
        petdata = prediction.replace("[","")
        petdata = petdata.replace("]","")
        petdata = petdata.split()
        print("petdata")
        cat = petdata[0]
        dog = petdata[1]
        other = petdata[2]
        '''
        for i in range(len(predictionList)): 
            if predictionList[i] != " " and predictionList[i] != "[" and predictionList[i] != "]":
                temp = temp + predictionList[i]
            elif temp != "":
                if cat == "":
                    cat = temp
                elif dog == "":
                    dog = temp
                elif other == "":
                    other = temp
            if predictionList[i].isspace() == True:
                temp = ""
                print("Variable has been cleared")
        '''

        print("Cat:", cat)
        print("Dog:", dog)
        print("Other:", other)
        if  cat >= dog and cat >= other:
            await ctx.channel.send(file=discord.File('Yes1.jpg'))
        elif dog >= other:
            await ctx.channel.send(file=discord.File('No1.jpg'))
            await ctx.channel.send("That is a dog! Not a cat!")
        else:
            await ctx.channel.send(file=discord.File('No1.jpg'))
        os.remove("Pet.jpg")


bot.run("")