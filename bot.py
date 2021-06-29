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
conver_soup_euro = soup_current_all.find_all("span",{"class":"conv-val triger-eur"})
conver_soup_pl = soup_current_all.find_all("span",{"class":"conv-val triger-pln"})
conver_soup_time = soup_current_all.find_all("div",{"class":"actual-currency"})
# Для удобства 

# Переменный доллар 
USD_BUY = conver_soup_dollars[0].text
USD_SELL = conver_soup_dollars[1].text
USD_NEXT_DAY = conver_soup_dollars[3].text
# Переменные Евро 
EURO_BUY = conver_soup_euro[0].text
EURO_SELL = conver_soup_euro[1].text
EURO_NEXT_DAY = conver_soup_euro[3].text
# Переменные PLN
PL_BUY = conver_soup_pl[0].text
PL_SELL = conver_soup_pl[1].text
PL_NEXT_DAY = conver_soup_pl[3].text
# Прочее
actual_time = conver_soup_time[0].text



# print(EURO_BUY,EURO_SELL,EURO_NEXT_DAY)
# print(USD_BUY,USD_SELL,USD_NEXT_DAY)
# print(PL_BUY,PL_SELL,PL_NEXT_DAY)

# Начало 
bot = telebot.TeleBot(config.token)
@bot.message_handler(commands=['start'],content_types=["text", "sticker", "pinned_message", "photo", "audio"])
def get_user_info(message):
    # Вывод клавиатуры Шаг 1 
    markup_inline =types.InlineKeyboardMarkup()
    btn_inline_1 = types.InlineKeyboardButton(text="✅Лучший курс в обменниках ",callback_data = 'current')
    btn_inline_2 = types.InlineKeyboardButton(text="Курс ЦБ",callback_data = 'cbank')
    btn_inline_3 = types.InlineKeyboardButton(text="Курс Биржы ",callback_data = 'no')
    btn_inline_4 = types.InlineKeyboardButton(text=" Кнопка ",callback_data = 'help')
    markup_inline.add(btn_inline_1,btn_inline_2)
    bot.send_message(message.chat.id, "Привет👋🏻 друзья , я бот \n \n Умею показывать  лучший курс валюты в Калининграде в отделениях банков \n \n  Курс по Центральному банку \n \n  Курс Московской биржы  \n Для повторного запуска используете комманду /start или напишите в чат /start " ,reply_markup = markup_inline)
        

@bot.callback_query_handler(func=lambda call:True)
def answer(call):
    if call.data== 'current':
        # Вывод клавиатуры Шаг 2 
        markup_inline_step_2 =types.InlineKeyboardMarkup()
        btn_inline_1_step_2 = types.InlineKeyboardButton(text="🇺🇸 Доллар ",callback_data = 'dollars')
        btn_inline_2_step_2 = types.InlineKeyboardButton(text="🇪🇺 Евро",callback_data = 'euro')
        btn_inline_3_step_2 = types.InlineKeyboardButton(text="🇵🇱 PL",callback_data = 'pln')
        markup_inline_step_2.add(btn_inline_1_step_2,btn_inline_2_step_2,btn_inline_3_step_2)
        msg = bot.send_message(call.message.chat.id," Выберете на клавиатуре что вас интересует  ",reply_markup = markup_inline_step_2)
    
    # Вывод dollars Шаг 3 
    elif call.data =='dollars':
        bot.send_message(call.message.chat.id,"🇺🇸 Покупка|Продажа \n \n ✅  {0}  |  {1} \n \n 🏞  Курс на след день {2} \n \n Время обновление информации {3} ".format(USD_BUY,USD_SELL,USD_NEXT_DAY,actual_time ))

    # Вывод euro Шаг 3 
    elif call.data =='euro':
        bot.send_message(call.message.chat.id,"🇪🇺 Покупка|Продажа \n \n ✅  {0}  |  {1} \n \n 🏞  Курс на след день {2} \n \n Время обновление информации {3} ".format(EURO_BUY,EURO_SELL,EURO_NEXT_DAY,actual_time ))


    # Вывод злоты Шаг 3 
    elif call.data =='pln':
        bot.send_message(call.message.chat.id,"🇵🇱 Покупка|Продажа \n \n ✅  {0}  |  {1} \n \n 🏞  Курс на след день {2} \n \n Время обновление информации {3} ".format(PL_BUY,PL_SELL,PL_NEXT_DAY,actual_time ))

    # Что то другое Шаг 3
    else:
        bot.send_message(call.message.chat.id,"Пожалуйста выберете  раздел на клавиатуре ")
    


bot.polling(none_stop=True)