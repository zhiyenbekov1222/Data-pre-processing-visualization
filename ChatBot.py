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
cart_dict = {}
c_dict = {}
pro_dict={}
num = 1

r = requests.get("https://upload.wikimedia.org/wikipedia/commons/7/74/Chocolate_Pie.jpg")

#token = "1658879405:AAEH4OqCj0zdqZZbq6EyZQJK8tAbDnfo_wE"
token = "1658158246:AAHyshd-PXVQUmXoVsbDSPJCqZBIHA6FRCM"
bot = telebot.TeleBot(token)

location="https://www.google.com/maps/place/Baiqonyr+Coffee+Station/@42.3579245,69.6491974,17.27z/data=!4m5!3m4!1s0x38a91dda3e80a7f3:0x6466c0e3562bde76!8m2!3d42.3580197!4d69.6509338"

categories=requests.get("https://app.dev.domme.kz/api/v1/finance/cats")
keyboardmain = types.InlineKeyboardMarkup()
for c in categories.json():
    _callback = "c_" + str(c['id'])
    button = types.InlineKeyboardButton(text=c['title'], callback_data = _callback)
    keyboardmain.add(button)

keyboard_last = types.InlineKeyboardMarkup()
last_button = types.InlineKeyboardButton(text="Төлеу",url="https://kaspi.kz/business/SignIn", callback_data="last")
keyboard_last.add(last_button)

@bot.message_handler(commands=["location"])
def command_handler(message: Message):
    bot.reply_to(message,location)
    
@bot.message_handler(commands=["help"])
def command_handler(message: Message):
    bot.reply_to(message,str(f"{message.from_user.first_name}, Тапсырып беру үшін /go батырмасын басыңыз"))
    
@bot.message_handler(commands=["start"])
def command_handler(message: Message):
    bot.reply_to(message,str(f"Сәлем {message.from_user.first_name}!\n Магазинге қош келдіңіз..\n Тапсырып беру үшін /go батырмасын басыңыз "))



@bot.message_handler(content_types=["text"])
def any_msg(message):
    if "go" in message.text :
        bot.send_message(message.chat.id, "Неге тапсырыс бергіңіз келеді?", reply_markup=keyboardmain)
        
    elif "Мекен жайы" in message.text:
        bot.reply_to(message,location)
        
    elif "7" in message.text and len(message.text)==11:
        tacking_info["Id"] =message.from_user.id
        tacking_info["Имя"] =message.from_user.first_name
        print(message.from_user.first_name)
        tacking_info["Фамилия"] =message.from_user.last_name
        print(message.from_user.last_name)
        tacking_info["Тауар аты"] = str(pro_dict['name'])
        tacking_info["Тауар саны"] = str(cart_dict["num"])
        tacking_info["Толық бағасы"] = str(cart_dict["price"])
        tacking_info["Номер телефона"] = message.text
        tacking_info["Дата заказа"] = date
        print(tacking_info)
        
        keyboard_pre = types.InlineKeyboardMarkup()
        pre_button = types.InlineKeyboardButton(text="Растау", callback_data="Confirm")
        keyboard_pre.add(pre_button)
        bot.send_message(message.chat.id, text = "Cіздің тапсырысыңыз:\n"+ str(pro_dict['name'])+": "+str(cart_dict["num"])+"дана,Бағасы: "
                         + str(cart_dict["price"]) +"\n Телефон нөміріңіз: "+ str(message.text) ,reply_markup = keyboard_pre)

    else:
       
        if "Тапсырыс беру" not in message.text :
            markup_reply=types.ReplyKeyboardMarkup(resize_keyboard = True,one_time_keyboard = True)
            item1=types.KeyboardButton("Тапсырыс беру")
            item2=types.KeyboardButton("Мекен жайы")
            markup_reply.add(item1 , item2)
            bot.send_message(message.chat.id, "Берілгендердің бірін таңдаңыз", reply_markup = markup_reply)
            print(message.from_user.first_name,":",message.text)
            
        elif "Тапсырыс беру" in message.text:
            bot.send_message(message.chat.id, "Неге тапсырыс бересіз?", reply_markup=keyboardmain)

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
    
    if call.data.startswith("c_"):
        print(categories.json())
        for c in categories.json():
            if str(c["id"]) == call.data[2:]:
                products = requests.get("https://app.dev.domme.kz/api/v1/finance/prods?cat=" + str(c["title"]))
                keyboard_pro = types.InlineKeyboardMarkup()
                for p in products.json():
                    _callback = "p_" +  str(p["title"])
                    button = types.InlineKeyboardButton(text=p['title'], callback_data = _callback)
                    keyboard_pro.add(button)
                keyboard_pro.add(backbutton)
                bot.send_message(call.message.chat.id, "Біреуін таңдаңыз?", reply_markup = keyboard_pro)
        #[{"id":1,"titile":"Fruit}, {"id": 2, "title":"Vegetable"}]
    
    if call.data.startswith("p_"):
        print(call.data[2:])
        product = requests.get("https://app.dev.domme.kz/api/v1/finance/prod_info?prod=" + call.data[2:])
        name = call.data[2:]
        amount = product.json()['amount']
        price = product.json()['price']
        bot.send_message(call.message.chat.id, name + ", cаны: " + str(amount) + ", Бағасы: " + str(price),reply_markup=keyboard_back)
        pro_dict['amount'] = amount
        pro_dict['price'] = price
        pro_dict['name'] = call.data[2:]
          
  
    elif call.data == "go1" :
        keyboardlast = types.InlineKeyboardMarkup()
        button0 = types.InlineKeyboardButton(text = "+", callback_data="plus")
        button1 = types.InlineKeyboardButton(text = "-", callback_data="minus")
        button2 = types.InlineKeyboardButton(text = 1 , callback_data="num")
        button3 = types.InlineKeyboardButton(text = "Сумма " + str(pro_dict['price']) + " Тг" , callback_data="price")
        button4 = types.InlineKeyboardButton(text = "Заказать", callback_data="finish")
        keyboardlast.add(button0,button1,button2,button3,button4,backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text = str(pro_dict['name']) + ", Санын енгізіңіз:",reply_markup=keyboardlast)
        cart_dict["num"]=button2.text
        cart_dict["price"] = pro_dict['price']
        #if call.data == "plus":
         #   print("Hii")
          #  num = 1
           # num +=1
            #bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="өзгертілді",reply_markup=keyboardlast)
            
    elif call.data.startswith("plus"):
        msg = "Шектік санына жетті"
        price = cart_dict["num"] * pro_dict['price']
        cart_dict["price"] = price
        if cart_dict["num"] < pro_dict['amount']:
            cart_dict["num"] +=1
            price = (cart_dict["num"]) * pro_dict['price']
            cart_dict["price"] = price
            msg = "Санын енгізіңіз" 
        keyboardlast = types.InlineKeyboardMarkup()
        button0 = types.InlineKeyboardButton(text = "+", callback_data="plus")
        button1 = types.InlineKeyboardButton(text = "-", callback_data="minus")
        button2 = types.InlineKeyboardButton(text = cart_dict["num"], callback_data="num")
        button3 = types.InlineKeyboardButton(text = "Сумма " + str(price) + " Тг" , callback_data="price")
        button4 = types.InlineKeyboardButton(text = "Заказать", callback_data="finish")
        keyboardlast.add(button0,button1,button2,button3,button4,backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=msg,reply_markup=keyboardlast)
            
            
    elif call.data.startswith("minus"):
        msg = "Шектік санына жетті"
        price = (cart_dict["num"]) * pro_dict['price']
        cart_dict["price"] = price
        if cart_dict["num"] > 1:
            cart_dict["num"] +=-1
            price = cart_dict["num"] * pro_dict['price']
            cart_dict["price"] = price
            msg = "Санын енгізіңіз" 
        keyboardlast = types.InlineKeyboardMarkup()
        button0 = types.InlineKeyboardButton(text = "+", callback_data="plus")
        button1 = types.InlineKeyboardButton(text = "-", callback_data="minus")
        button2 = types.InlineKeyboardButton(text = cart_dict["num"], callback_data="num")
        button3 = types.InlineKeyboardButton(text ="Сумма " + str(price) + " Тг" , callback_data="price")
        button4 = types.InlineKeyboardButton(text = "Заказать", callback_data="finish")
        keyboardlast.add(button0,button1,button2,button3,button4,backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text=msg,reply_markup=keyboardlast)
    
    elif call.data == "finish":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text= "Телефон нөміріңізді қалдырыңыз :")
    
    elif call.data == "Confirm":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text = "Төлем",reply_markup=keyboard_last)
        
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
    pd_data2=pd_data2[['Id','Имя','Фамилия',"Тауар аты",'Тауар саны',"Толық бағасы",'Номер телефона','Дата заказа']]
    pd_data2.to_csv(filename)
   

bot.polling()
if __name__ == "__main__":
    bot.polling(none_stop=True)
    
    
#res_pd.set_index('Номер', inplace=True)