from datetime import timedelta, datetime
import random
import sys
from TelegramApi import *
from window import *



async def getText(update: Update, bot):
    if update.message != None:
        messagetime = (update.message.date + timedelta(days=0, hours=8)).strftime("%m/%d %H:%M")
    else:
        messagetime = datetime.now().strftime("%m/%d %H:%M")
    originmessage = update.message.text.replace('\n', '\n    ')
    message = ''
    onelinetextlimit = 20
    for i in range(0, len(originmessage), onelinetextlimit):
        if i + onelinetextlimit > len(originmessage):
            message += '    ' + originmessage[i:] + '\n'
        else:
            message += '    ' + originmessage[i:i+onelinetextlimit] + '\n'
    message =   f'{update.message.from_user.full_name}({update.message.from_user.name}):    {messagetime}\n' + \
                f'{message}'
    receivedList.append(message)
    saveMessage(message)
    print(f'get {message}')

async def getPhoto(update: Update, bot):
    messagetime = (update.message.date + timedelta(days=0, hours=8)).strftime("%m/%d %H:%M")
    if update.message.caption == None:
        originmessage = ''
    else:
        originmessage = update.message.caption.replace('\n', '\n    ')
    message = ''
    onelinetextlimit = 20
    for i in range(0, len(originmessage), onelinetextlimit):
        if i + onelinetextlimit > len(originmessage):
            message += '    ' + originmessage[i:] + '\n'
        else:
            message += '    ' + originmessage[i:i+onelinetextlimit] + '\n'
    message =   f'{update.message.from_user.full_name}({update.message.from_user.name}):    {messagetime}\n' + \
                f'{message}'

    filename = 'photo/' + messagetime.replace(' ', '').replace('/', '').replace(':', '') + '_' + \
                str(random.randint(0, sys.maxsize)) + '.png'
    file = await bot.bot.getFile(update.message.photo[-1].file_id)
    
    await file.download(filename)

    receivedList.append((message, filename))
    saveMessage(message)
    print(f'get {message}')


async def getSticker(update: Update, bot):
    messagetime = (update.message.date + timedelta(days=0, hours=8)).strftime("%m/%d %H:%M")
    if update.message.caption == None:
        originmessage = ''
    else:
        originmessage = update.message.caption.replace('\n', '\n    ')
    message = ''
    onelinetextlimit = 20
    for i in range(0, len(originmessage), onelinetextlimit):
        if i + onelinetextlimit > len(originmessage):
            message += '    ' + originmessage[i:] + '\n'
        else:
            message += '    ' + originmessage[i:i+onelinetextlimit] + '\n'
    message =   f'{update.message.from_user.full_name}({update.message.from_user.name}):    {messagetime}\n' + \
                f'{message}'

    filename = 'sticker/' + messagetime.replace(' ', '').replace('/', '').replace(':', '') + '_' + \
                str(random.randint(0, sys.maxsize)) + '.png'
    file = await bot.bot.getFile(update.message.sticker.file_id)
    
    await file.download(filename)

    receivedList.append((message, filename))
    saveMessage(message)
    print(f'get {message}')