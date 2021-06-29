import config #Конфинурация для Telegram Bot
import requests # Модуль для обработки URL
from bs4 import BeautifulSoup  as BS # Модуль для работы с HTML
import time # Модуль для остановки программы
import telebot
import emoji #Смайлики 
from telebot import types

# Парсер 
Main = "https://kaliningrad.bankiros.ru/currency"    
    # Заголовки для передачи вместе с URL
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
#######
# Ищем доллар покупка 
current_alls = requests.get(Main ,headers=headers)
####################
soup_current_all = BS(current_alls.content,'html.parser')


# Финальный Парсинг 
conver_soup_dollars = soup_current_all.find_all("span",{"class":"conv-val triger-usd"})
conver_soup_dollars_sell = soup_current_all.find_all("span",{"class":"conv-val triger-usd"})
# Для удобства 

USD_BUY = conver_soup_dollars[0].text
USD_SELL = conver_soup_dollars[1].text
USD_NEXT_DAY = conver_soup_dollars[3].text

print(USD_BUY,USD_SELL,USD_NEXT_DAY)

# Начало 
bot = telebot.TeleBot(config.token)
@bot.message_handler(commands=['start'])
def get_user_info(message):
    # Вывод клавиатуры Шаг 1 
    markup_inline =types.InlineKeyboardMarkup()
    btn_inline_1 = types.InlineKeyboardButton(text="✅Лучший курс для обмена валюты ",callback_data = 'current')
    btn_inline_2 = types.InlineKeyboardButton(text="Курс ЦБ",callback_data = 'cbank')
    btn_inline_3 = types.InlineKeyboardButton(text="Курс Биржы ",callback_data = 'no')
    markup_inline.add(btn_inline_1,btn_inline_2)
    bot.send_message(message.chat.id, "Привет👋🏻 я бот , показываю лучший курс валюты в Калининграде \n  Курс ЦБ \n  Курс Биржа \n  " ,reply_markup = markup_inline)


@bot.callback_query_handler(func=lambda call:True)
def answer(call):
    if call.data== 'current':
        # Вывод клавиатуры Шаг 2 
        markup_inline_step_2 =types.InlineKeyboardMarkup()
        btn_inline_1_step_2 = types.InlineKeyboardButton(text="🇺🇸 Доллар ",callback_data = 'dollars')
        btn_inline_2_step_2 = types.InlineKeyboardButton(text="🇪🇺 Евро",callback_data = 'euro')
        btn_inline_3_step_2 = types.InlineKeyboardButton(text="🇵🇱 Злоты",callback_data = 'zlt')
        markup_inline_step_2.add(btn_inline_1_step_2,btn_inline_2_step_2,btn_inline_3_step_2)
        msg = bot.send_message(call.message.chat.id," Выберете на клавиатуре что хотите узнать  ",reply_markup = markup_inline_step_2)
    
    # Вывод dollars Шаг 3 
    elif call.data =='dollars':
        bot.send_message(call.message.chat.id,"🇺🇸 Покупка|Продажа \n \n ✅  {0}  |  {1} \n \n 🏞  Курс на след день {2} ".format(USD_BUY,USD_SELL,USD_NEXT_DAY ))

    # Вывод euro Шаг 3 
    elif call.data =='euro':
        bot.send_message(call.message.chat.id,"Привет евро ")

    # Вывод злоты Шаг 3 
    elif call.data =='zlt':
        bot.send_message(call.message.chat.id,"Привет злоты   ",'''reply_markup=markup_reply''')

    # Что то другое Шаг 3 
    else:
        bot.send_message(call.message.chat.id,"Пожалуйста выберете  раздел на клавиатуре ",'''reply_markup=markup_reply''')
    
    # bot.register_next_step_handler(msg )








bot.polling()