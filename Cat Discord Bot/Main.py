#Import catness libaries
#blah blah
import discord
import math
from discord.ext import commands
import os
import praw
import random
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
import mmap


#Sets up Reddit API
bot = commands.Bot(command_prefix='!')
bot.remove_command('help')
reddit = praw.Reddit(client_id='o7-kUtRSpT3iKA', client_secret='WLCfuJD6XJVSke9C979n1b-1_bI', user_agent='DISCORD:The green bot: version 1.0 (by /u/joshiwoshi2005)')

#Sets up cat AI
np.set_printoptions(suppress=True)
model = tensorflow.keras.models.load_model('keras_model.h5')
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)


#Help command
@bot.command()
async def help(ctx):
    hlp = discord.Embed(
        title='Help',
        description='Shows help commands',
        colour=discord.Colour.green())
    hlp.set_footer(text='Cat Bot help. Prefix = !')
    hlp.add_field(
        name="hot",
        value=
        "Shows what is hot right now on r/cat Template: !hot",
        inline=False)
    hlp.add_field(
        name="CatDetector",
        value=
        "Detects the pet in your photo: cat, dog or other. Template: !CatDetector [Attached Image]",
        inline=False)
    hlp.add_field(
        name="AutoDetect",
        value="Toggle whitelist your username to our Cat autodetect. I will verify your cat-ness automatically! Template: !AutoDetect",
        inline=False)
    await ctx.send(embed=hlp)

#What is hot on reddit
@bot.command()
async def hot(ctx):
  for submission in reddit.subreddit('cats').hot(limit=random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])):
    title = submission.title
    description = submission.score
    url = submission.url
  dl = discord.Embed(
      title=title,
      description='{}'.format(url),
      colour=discord.Colour.green())
  dl.set_footer(text='Straight off of reddit')
  await ctx.send(embed=dl)

##IGNORE THIS, IT'S A MESS IN PROGRESS##
@bot.command()
async def AutoDetect(ctx, *arg):
    user = False
    if open('AutoDetect.txt', 'r').read().find(str(ctx.message.author)):
        user = True
    if user == True:
        with open("AutoDetect.txt", "r") as f:
                lines = f.readlines()
        with open("AutoDetect.txt", "w") as f:
            for line in lines:
                if line.strip("\n") != str(ctx.message.author):
                    f.write(line)
        await ctx.send("We have deleted you from my detector whitelist.")
    if user == False:
        author = str(ctx.message.author)
        f.write(author)
        f.close()
        await ctx.send("We have added you to my detector whitelist.")
########################################

#Cat Detector Command
@bot.command()
async def CatDetector(ctx, img:str = None): 
    #Grabs image attachment
    attachedimage = True
    try:
        test = ctx.message.attachments[0].url
    except IndexError:
        if img == None:
            await ctx.send("You have not attached an image, try again.")
            attachedimage = False
        else:
            imageLink = img
    if attachedimage == True:
        #Sets Headers and downloads image as Pet.jpg
        imageLinkList = list(imageLink)
        extension = imageLinkList[len(imageLinkList)-4]
        extension = imageLinkList[len(imageLinkList)-3]
        extension = extension + imageLinkList[len(imageLinkList)-2]
        extension = extension + imageLinkList[len(imageLinkList)-1]
        if extension == ".jpg":
            opener = urllib.request.URLopener()
            opener.addheader('User-Agent', 'Mozilla/5.0')
            filename, headers = opener.retrieve(imageLink, "Pet.jpg")
        elif extension == ".png":
            opener = urllib.request.URLopener()
            opener.addheader('User-Agent', 'Mozilla/5.0')
            filename, headers = opener.retrieve(imageLink, "Pet.png")
            image = Image.open("Pet.png")
            image.save("Pet.jpg")
            image = None
            os.remove("Pet.png")
        else:
            ctx.send("Unsupported file format. Please try again with a .png or .jpg file.")
        #Opens image
        image = Image.open('Pet.jpg')
        #Re-sizes image
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        #Changes image into a numpy array
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        #Sends data off to tensorflow, to predict data
        prediction = model.predict(data)
        #Converts output into string
        prediction = str(prediction)
        temp = ""
        cat = ""
        dog = ""
        other = ""
        #Converts the petdata output into a list
        petdata = prediction.replace("[","")
        petdata = petdata.replace("]","")
        petdata = petdata.split()
        #Splits the list out into variables
        cat = petdata[0]
        percentagecat = "{:.0%}".format(float(cat))
        dog = petdata[1]
        percentagedog = "{:.0%}".format(float(dog))
        other = petdata[2]
        percentageother = "{:.0%}".format(float(other))
        #Looks at the predictions and check which one is more confident
        if  cat >= dog and cat >= other:
            first_image = Image.open("Yes1.jpg")
            second_image = Image.open("Pet.jpg")
            basewidth = 590
            wpercent = (basewidth/float(second_image.size[0]))
            hsize = int((float(second_image.size[1])*float(wpercent)))
            second_image = second_image.resize((basewidth,hsize), Image.ANTIALIAS)
            width, height = first_image.size
            width1, height1 = second_image.size
            if height1 > height:
                ratio = (float(height) / float(height1))
            else:
                ratio = (590 / float(width1))
            width1 = int(float(width1) * ratio)
            height1 = int(float(height1) * ratio)
            second_image = second_image.resize((width1, height1), Image.ANTIALIAS)
            if height1 < 590:
                coordy = height - 590
            else:
                coordy = height - height1
            if width1 < 590:
                coordx = width - 590
            else:
                coordx = width - width1
            first_image.paste(second_image, (coordx, coordy))
            first_image.save("editedImage.jpg")
            file = discord.File("editedImage.jpg", filename="editedImage.jpg")
            embed = discord.Embed(
            title='Cat Detector',
            description='YES, that is a cat. MEOW!',
            colour=discord.Colour.green())
            embed.set_image(url="attachment://editedImage.jpg")
            embed.set_footer(text="I am {} sure that is a cat, {} sure that is a dog and {} that isn't either.".format(percentagecat, percentagedog, percentageother))
            await ctx.channel.send(file=file, embed=embed)
        elif dog >= other:
            first_image = Image.open("No1.jpg")
            second_image = Image.open("Pet.jpg")
            basewidth = 590
            wpercent = (basewidth/float(second_image.size[0]))
            hsize = int((float(second_image.size[1])*float(wpercent)))
            second_image = second_image.resize((basewidth,hsize), Image.ANTIALIAS)
            width, height = first_image.size
            width1, height1 = second_image.size
            if height1 > height:
                ratio = (float(height) / float(height1))
            else:
                ratio = (590 / float(width1))
            width1 = int(float(width1) * ratio)
            height1 = int(float(height1) * ratio)
            second_image = second_image.resize((width1, height1), Image.ANTIALIAS)
            if height1 < 590:
                coordy = height - 590
            else:
                coordy = height - height1
            if width1 < 590:
                coordx = width - 590
            else:
                coordx = width - width1
            first_image.paste(second_image, (coordx, coordy))
            first_image.save("editedImage.jpg")
            file = discord.File("editedImage.jpg", filename="editedImage.jpg")
            embed = discord.Embed(
            title='Cat Detector',
            description='That is a dog! Not a Cat. BARK!',
            colour=discord.Colour.green())
            embed.set_image(url="attachment://editedImage.jpg")
            embed.set_footer(text="I am {} sure that is a cat, {} sure that is a dog and {} that isn't either.".format(percentagecat, percentagedog, percentageother))
            await ctx.channel.send(file=file, embed=embed)
        else:
            first_image = Image.open("No1.jpg")
            second_image = Image.open("Pet.jpg")
            basewidth = 590
            wpercent = (basewidth/float(second_image.size[0]))
            hsize = int((float(second_image.size[1])*float(wpercent)))
            second_image = second_image.resize((basewidth,hsize), Image.ANTIALIAS)
            width, height = first_image.size
            width1, height1 = second_image.size
            if height1 > height:
                ratio = (float(height) / float(height1))
            else:
                ratio = (590 / float(width1))
            width1 = int(float(width1) * ratio)
            height1 = int(float(height1) * ratio)
            second_image = second_image.resize((width1, height1), Image.ANTIALIAS)
            if height1 < 590:
                coordy = height - 590
            else:
                coordy = height - height1
            if width1 < 590:
                coordx = width - 590
            else:
                coordx = width - width1
            first_image.paste(second_image, (coordx, coordy))
            first_image.save("editedImage.jpg")
            file = discord.File("editedImage.jpg", filename="editedImage.jpg")
            embed = discord.Embed(
            title='Cat Detector',
            description="I don't know what that is. It isn't a cat or a dog...",
            colour=discord.Colour.green())
            embed.set_image(url="attachment://editedImage.jpg")
            embed.set_footer(text="I am {} sure that is a cat, {} sure that is a dog and {} that isn't either.".format(percentagecat, percentagedog, percentageother))
            await ctx.channel.send(file=file, embed=embed)
        os.remove("Pet.jpg")
        os.remove("editedImage.jpg")

@bot.command()
async def RandomCat(ctx, *arg): 
    image_types = ["jpeg", "jpg"]
    random.shuffle(image_types)
    if image_types[0] == "jpg":
        randomnumber = int(random.randint(1, 11445))
        file = discord.File("CatPictures/Cat ({}).jpg".format(randomnumber), filename="CatImage.jpg")
        embed = discord.Embed(
        title='Random Cat Image',
        description="Here is your cat image: ",
        colour=discord.Colour.green())
        embed.set_image(url="attachment://CatImage.jpg")
        await ctx.channel.send(file=file, embed=embed)
    elif image_types[0] == "jpeg":
        randomnumber = int(random.randint(1, 1071))
        file = discord.File("CatPictures/Cat ({}).jpeg".format(randomnumber), filename="CatImage.jpg")
        embed = discord.Embed(
        title='Random Cat Image',
        description="Here is your cat image: ",
        colour=discord.Colour.green())
        embed.set_image(url="attachment://CatImage.jpg")
        await ctx.channel.send(file=file, embed=embed)

bot.run("")