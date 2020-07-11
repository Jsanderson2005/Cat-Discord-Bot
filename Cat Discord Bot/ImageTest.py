from PIL import Image, ImageOps

#TESTING PROGRQM
imageLink = "https://cdn.discordapp.com/attachments/730779238114000937/731442681091194880/staffordshire_bull_terrier_4.jpg"
imageLinkList = list(imageLink)
print(imageLinkList)
extension = imageLinkList[len(imageLinkList)-4]
extension = imageLinkList[len(imageLinkList)-3]
extension = extension + imageLinkList[len(imageLinkList)-2]
extension = extension + imageLinkList[len(imageLinkList)-1]
print(extension)

'''
first_image = Image.open("Yes1.jpg")
second_image = Image.open("Test_Cat.jpg")
basewidth = 590
wpercent = (basewidth/float(second_image.size[0]))
hsize = int((float(second_image.size[1])*float(wpercent)))
second_image = second_image.resize((basewidth,hsize), Image.ANTIALIAS)
width, height = first_image.size
width1, height1 = second_image.size
coordx = width-width1
coordy = height - height1
first_image.paste(second_image, (coordx, coordy))
firstimage.show()
img.save("editedImage.jpg")
'''