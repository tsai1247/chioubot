#!/usr/bin/env python3
# coding=utf-8
import asyncio
from datetime import datetime
from functools import partial
import logging
import threading
from time import sleep
import webbrowser
from dotenv import load_dotenv
import tkinter as tk

from Command import *
from TelegramApi import app
from window import *
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, ApplicationBuilder, filters
from tkHyperLinkManager import HyperlinkManager

load_dotenv()
logging.basicConfig(level=logging.INFO)
if not os.path.exists("photo"):
    os.makedirs("photo")
if not os.path.exists("sticker"):
    os.makedirs("sticker")

async def CreateImage(textfield, photo):
    textfield.image_create('end', image=photo)

def InputLoop():
    def UpdateMessage():
        curlen = 0
        while True:
            if len(receivedList) > curlen:
                if len(receivedList) > receivedlimit:
                    receivedList.pop(0)
                receivefield.config(state='normal')
                receivefield.delete('1.0', 'end')
                for data in receivedList:
                    if type(data) is tuple:
                        receivefield.insert('end', data[0] + '\n')
                        
                        # sendingphoto = asyncio.new_event_loop()
                        # asyncio.set_event_loop(sendingphoto)

                        # sendingphoto.run_until_complete(CreateImage(receivefield, getTextPhoto(data[1])))
                        # sendingphoto.close()
                        fullfilename = os.path.abspath(data[1])
                        receivefield.insert('end', data[1], hyperlink.add(partial(webbrowser.open, f'file:///{fullfilename}')))

                        receivefield.insert('end', '\n')    
                    else:
                        receivefield.insert('end', data + '\n')

                receivefield.config(state='disabled')
                curlen = len(receivedList)
            sleep(1)

    window = tk.Tk()
    window.title('邱p')
    istopmost = tk.BooleanVar()
    istopmost.set(True)
    def settopmost():
        window.attributes('-topmost', istopmost.get())
    settopmost()
    tpmost_checkbox = tk.Checkbutton(window, text='topmost', variable=istopmost, command=settopmost)
    tpmost_checkbox.pack(anchor='ne')

    def send():
        if chat_id != 0:
            sending = asyncio.new_event_loop()
            asyncio.set_event_loop(sending)
            messagetime = datetime.now().strftime("%m/%d %H:%M")
            message = inputfield.get("1.0", "end")
            message =   f'You:    {messagetime}\n' + \
                        f'    {message}'
            receivedList.append(message)
            saveMessage(message)

            sending.run_until_complete(Send(chat_id, inputfield.get("1.0", "end")))
            inputfield.delete("1.0", "end")
            sending.close()

    inputframe = tk.Frame(window)
    inputfield = tk.Text(inputframe, width=50, height=6, font=('Arial', 12))
    sendbutton = tk.Button(inputframe, text="送出", command=send, width=10, height=6, font=('Arial', 12))
    receivefield = tk.Text(window, background='lightblue',
        width=60, height=20, font=('Arial', 12), foreground='black')
    hyperlink = HyperlinkManager(receivefield)
    receivefield.config(state='disabled')
    scrollbar=tk.Scrollbar(window)
    receivefield.config(yscrollcommand=scrollbar.set) 
    scrollbar.config(command=receivefield.yview) 

    inputframe.pack(side='bottom')
    sendbutton.pack(side='right')
    inputfield.pack(side='left')
    scrollbar.pack(side='right', fill=tk.Y)
    receivefield.pack(side='left', fill=tk.Y)

    threading.Thread(target= UpdateMessage).start()

    window.mainloop()

# Main
def main():
    threading.Thread(target= InputLoop).start()
    
    # commands
    app.add_handler(MessageHandler(filters.TEXT, getText))
    app.add_handler(MessageHandler(filters.PHOTO, getPhoto))
    app.add_handler(MessageHandler(filters.ALL, getSticker))

    # run
    logging.info("KaTsuGenshinBot Server Running...")
    app.run_polling(stop_signals=None)

if __name__ == '__main__':
    main()

