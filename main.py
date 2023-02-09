# lbraries for create bot
from telegram.ext import Updater,CommandHandler,MessageHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.filters import Filters
import re


def start(update,context):
    update.message.reply_text(
        f'Assalomu alaykum, botdan foydalanish uchun biror gap jo\'nating!!!'
        )


def buyruq(update, context):
    chat_id = update.message.chat.id
    text_user = update.message.text
    data = text_user.lower()
    listing = data.split()

    i=0
    while i < len(listing):
        if listing[i]=="№" or listing[i]=="N" or listing[i]=="n" or listing[i]=="Н":
            listing[i] = listing[i] + listing[i+1]
            listing.pop(i+1)
            i-=1
        i+=1
    i=0
    while i < len(listing):
        if listing[i]=="%":
            listing[i-1] = listing[i-1] + listing[i]
            listing.pop(i)
            i-=1
        i+=1
    
    sana, raqam = sana_raqam(listing)
    context.bot.send_message(
        chat_id=chat_id,
        text=f"Sana: {sana}\nRaqam: {raqam}"
    )


def date(x):
    if re.search(r"(\d{1,2}\.\d{1,2}\.\d{4})|(\d{1,2}-\d{1,2}-\d{4})|(\d{1,2}\\\d{1,2}\\\d{4})|(\d{1,2},\d{1,2},\d{4})",x):
        return True
    
def invoice(x):
    if x.startswith("№") or x.startswith("N") or x.startswith("n") or x.startswith("Н"):
        return True
    else:
        return False
    
def near_invoice(x):
    S = 0
    if "/" in x:
        S+=1
    if not "%" in x:
        S+=1
    if "-" in x:
        S+=1
    if 1<=len(x)<=4:
        S+=1
    return S
    
def number_or_string(x):
    S = 0
    for i in x:
        if i.isnumeric():
            S+=1
    if S>=1:
        return True
    else:
        return False

def sana_raqam(listing):    
    sanalar = []
    sana=None; raqam=None
    for i in listing:
        if date(i):
            sanalar.append(i)
        if invoice(i):
            raqam = i
    if sanalar:
        sana = max(sanalar)

    if raqam==None:
        raqam = ""
        for i in range(len(listing)):
            if listing[i]=="от":
                try:
                    if number_or_string(listing[i-1]):
                        raqam = listing[i-1] + raqam
                    if number_or_string(listing[i-2]):
                        raqam = listing[i-2] + raqam
                except:
                    try:
                        if number_or_string(listing[i-1]):
                            raqam = listing[i] + raqam
                    except:
                        pass

    if raqam == "":
        maxi = 0
        for i in range(len(listing)):
            if number_or_string(listing[i]):
                if near_invoice(listing[i]):
                    S = near_invoice(listing[i])
                    if maxi<S:
                        maxi=S
                        raqam=listing[i]
                        
    if raqam == "" or raqam==None:
        raqam = "Raqamsiz"
    if sana =="" or sana == None:
        sana = "Sana yo'q"
        
    return sana,raqam.upper() 


updater = Updater(token="6229204556:AAHkwO8slPfSU7HkV-DgZimfmk8RaJ9qVWI")

dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('restart', start))
dispatcher.add_handler(MessageHandler(Filters.text, buyruq))

updater.start_polling()
updater.idle()
