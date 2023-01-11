from TelegramApi import *

from PIL import ImageTk, Image

def getTextPhoto(filename, width = 300):
    image = Image.open(filename)
    image_size_basic = width
    imagewidth, image_height = image_size_basic, int(image_size_basic * image.height / image.width)
    image = image.resize((imagewidth, image_height), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    return photo

def saveMessage(text):
    with open('history.backup', 'a', encoding='utf-8') as fa:
        fa.write(text + '\n')
receivedlimit = 10
receivedList = []
chat_id = -1001454046703
