import telebot
from telebot import types
from telebot.types import Message
import requests
import pandas as pd
import os
import numpy as np
from datetime import datetime

date = datetime.today().strftime('%d.%m.%y, %H:%M')


st_list=[]
tacking_info = {}

r = requests.get("https://upload.wikimedia.org/wikipedia/commons/7/74/Chocolate_Pie.jpg")

#token = "1658879405:AAEH4OqCj0zdqZZbq6EyZQJK8tAbDnfo_wE"
token = "1658158246:AAHyshd-PXVQUmXoVsbDSPJCqZBIHA6FRCM"
bot = telebot.TeleBot(token)

location="https://www.google.com/maps/place/Baiqonyr+Coffee+Station/@42.3579245,69.6491974,17.27z/data=!4m5!3m4!1s0x38a91dda3e80a7f3:0x6466c0e3562bde76!8m2!3d42.3580197!4d69.6509338"



@bot.message_handler(commands=["location"])
def command_handler(message: Message):
    bot.reply_to(message,location)
    
@bot.message_handler(commands=["help"])
def command_handler(message: Message):
    bot.reply_to(message,str(f"{message.from_user.first_name}, Тапсырып беру үшін /go батырмасын басыңыз"))
    
@bot.message_handler(commands=["start"])
def command_handler(message: Message):
    bot.reply_to(message,str(f"Сәлем {message.from_user.first_name}!\n Магазинге қош келдіңіз..\n Тапсырып беру үшін /go батырмасын басыңыз "))

categories=requests.get("https://app.dev.domme.kz/api/v1/finance/cats")
button1 = types.InlineKeyboardButton(text=categories.json()[0]["title"], callback_data = "c1")
button2 = types.InlineKeyboardButton(text=categories.json()[1]["title"], callback_data = "c2")
keyboardmain = types.InlineKeyboardMarkup()
keyboardmain.add(button1,button2)

@bot.message_handler(content_types=["text"])
def any_msg(message):
    if "go" in message.text :
        bot.send_message(message.chat.id, "Неге тапсырыс бергіңіз келеді?", reply_markup=keyboardmain)
    elif "Мекен жайы" in message.text:
        bot.reply_to(message,location)
    elif "7" in message.text and len(message.text)==11:
        tacking_info["Id"] =message.from_user.id
        if message.from_user.id is None:
            tacking_info["Id"] = 1
        print(message.from_user.id)
        tacking_info["Имя"] =message.from_user.first_name
        print(message.from_user.first_name)
        tacking_info["Фамилия"] =message.from_user.last_name
        print(message.from_user.last_name)
        tacking_info["Номер телефона"] = message.text
        tacking_info["Дата заказа"] = date
        print(tacking_info)
        keyboard_last = types.InlineKeyboardMarkup()
        last_button = types.InlineKeyboardButton(text="Төлеу",url="https://kaspi.kz/business/SignIn", callback_data="last")
        keyboard_last.add(last_button)
        bot.send_message(message.chat.id, "Тапсырыс қабылданды",reply_markup = keyboard_last)
        saving(tacking_info)
    elif message.text.isdecimal():
        tacking_info["Тауар саны"] = message.text
        bot.send_message(message.chat.id, "Телефон нөмірін енгізіңіз")
        print(message.text)
    else:
       
        if "Тапсырыс беру" not in message.text :
            markup_reply=types.ReplyKeyboardMarkup(resize_keyboard = True,one_time_keyboard = True)
            item1=types.KeyboardButton("Тапсырыс беру")
            item2=types.KeyboardButton("Мекен жайы")
            markup_reply.add(item1 , item2)
            bot.send_message(message.chat.id, "Берілгендердің бірін таңдаңыз", reply_markup = markup_reply)
            print(message.from_user.first_name,":",message.text)
        elif "Тапсырыс беру" in message.text:
            print(categories.json()[0]["title"])
            for c in categories.json():
                pass
            bot.send_message(message.chat.id, "Неге тапсырыс?", reply_markup=keyboardmain)

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    fruits=requests.get("https://app.dev.domme.kz/api/v1/finance/prods?cat=Фрукты")
    vegetables=requests.get("https://app.dev.domme.kz/api/v1/finance/prods?cat=Овощи")
    keyboard_back=types.InlineKeyboardMarkup()
    backbutton = types.InlineKeyboardButton(text="артқа", callback_data="mainmenu")
    order = types.InlineKeyboardButton(text="Заказать", callback_data="go1")
    keyboard_back.add(order,backbutton)
    bot.answer_callback_query(callback_query_id=call.id)
    
    if call.data == "mainmenu":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Неге тапсырыс бергіңіз келеді?",reply_markup=keyboardmain)
        
    elif call.data == "c1":
        print(fruits.json())
        keyboard_r1 = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text=fruits.json()[0]["title"], callback_data="f1")
        button2 = types.InlineKeyboardButton(text=fruits.json()[1]["title"], callback_data="f2")
        keyboard_r1.add(button1,button2,backbutton)
        
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Қай жеміс түрі",reply_markup=keyboard_r1)
          
        
    elif call.data == "c2":
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text=vegetables.json()[0]["title"], callback_data="v1")
        button2 = types.InlineKeyboardButton(text=vegetables.json()[1]["title"], callback_data="v2")
        keyboard.add(button1, button2, backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Қай көкөніс түрі" ,reply_markup=keyboard)

    elif call.data == "f1":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text = fruits.json()[0]["title"] + ", барлығы " + str(fruits.json()[0]["amount"]) + ", бағасы " + str(fruits.json()[0]["price"]),reply_markup=keyboard_back)

    elif call.data == "f2":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text = fruits.json()[1]["title"] + ", барлығы " + str(fruits.json()[1]["amount"]) + ", бағасы " + str(fruits.json()[1]["price"]),reply_markup=keyboard_back)
       
    elif call.data == "v1":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text = vegetables.json()[0]["title"] + ", барлығы " + str(vegetables.json()[0]["amount"]) + ", бағасы " + str(vegetables.json()[0]["price"]),reply_markup = keyboard_back)
        
        
    elif call.data == "v2":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text = vegetables.json()[1]["title"] + ", барлығы " + str(vegetables.json()[1]["amount"]) + ", бағасы " + str(vegetables.json()[1]["price"]),reply_markup =keyboard_back)
        
    
    elif call.data == "go1":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Санын енгізіңіз")
        st=call.message.text.split(" ")
        #st_list.append(st[0])
        tacking_info["Заказ"] = st[0]
        #saving(tacking_info)
        print(st[0])

        
    #elif "7" in call.message.text and len(call.message.text)==11:
        
    #tacking_info["Заказ"] = st_list
    
def saving(tacking_info):
    filename = "information.csv"
    if filename in os.listdir():
        pd_data1 = pd.read_csv(filename)
    else:
        pd_data1 = pd.DataFrame()
    s_dict = pd.Series(tacking_info)
    pd_data2=pd.DataFrame(s_dict).T
    pd_data2 = pd.concat([pd_data1, pd_data2])
    #pd_data2.set_index("Id",inplace=True)
    pd_data2=pd_data2[['Id','Имя','Фамилия','Номер телефона','Заказ','Тауар саны','Дата заказа']]
    pd_data2.to_csv(filename)
   

bot.polling()
if __name__ == "__main__":
    bot.polling(none_stop=True)
    
    
#res_pd.set_index('Номер', inplace=True)