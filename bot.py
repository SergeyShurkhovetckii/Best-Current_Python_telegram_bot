import config #Конфинурация для Telegram Bot
import requests # Модуль для обработки URL
from bs4 import BeautifulSoup  as BS # Модуль для работы с HTML
import time # Модуль для остановки программы
import telebot
import emoji #Смайлики 
from telebot import types

# Парсер 
Main = "https://kaliningrad.bankiros.ru/currency"
MAin_CB = "https://bankiros.ru/currency/cbrf"
Main_Moex ="https://bankiros.ru/currency/moex/usdrub-tod"
Main_Moex_euro = "https://bankiros.ru/currency/moex/eurrub-tod"
    # Заголовки для передачи вместе с URL
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
#######
# Ищем доллар покупка 
current_alls = requests.get(Main ,headers=headers)
current_CB = requests.get(MAin_CB,headers=headers)
current_moex_USD = requests.get(Main_Moex,headers=headers) 
current_moex_EURO = requests.get(Main_Moex_euro,headers=headers) 
####################
soup_current_all = BS(current_alls.content,'html.parser')
soup_current_CB = BS(current_CB.content,'html.parser')
soup_current_moex_usd = BS(current_moex_USD.content,'html.parser')
soup_current_moex_euro = BS(current_moex_EURO.content,'html.parser')
# Финальный Парсинг 
conver_soup_dollars = soup_current_all.find_all("span",{"class":"conv-val triger-usd"})
conver_soup_euro = soup_current_all.find_all("span",{"class":"conv-val triger-eur"})
conver_soup_pl = soup_current_all.find_all("span",{"class":"conv-val triger-pln"})
conver_soup_time = soup_current_all.find_all("div",{"class":"actual-currency"})
conver_soup_moex_usd = soup_current_moex_usd.find_all("span",{"class":"xxx-font-size-30 xxx-text-bold"})
conver_soup_moex_usd_time = soup_current_moex_usd.find_all("span",{"class":"xxx-trading-preview__date xxx-font-size-14 xxx-text-color-darck-gray"})
conver_soup_moex_euro = soup_current_moex_euro.find_all("span",{"class":"xxx-font-size-30 xxx-text-bold"})
conver_soup_moex_euro_time = soup_current_moex_euro.find_all("span",{"class":"xxx-trading-preview__date xxx-font-size-14 xxx-text-color-darck-gray"})
# bank_name = soup_current_all.find("td",{"class":"currency-value"})

# for i in bank_name.find_all('a'):
#     print(i.text)

bank_name = soup_current_all.find("table",{"class":"non-standard"})
def action ():
    list = []
    for i in bank_name.find_all('a'):
        # list = i
        # print(i.text)
        list.append(i)
        print(list[0].text)


action()


# Переменный доллар 
USD_BUY = conver_soup_dollars[0].text
USD_SELL = conver_soup_dollars[1].text
USD_CB = conver_soup_dollars[2].text
USD_TR = conver_soup_moex_usd[0].text
USD_TR_time = conver_soup_moex_usd_time[0].text
# Переменные Евро 
EURO_BUY = conver_soup_euro[0].text
EURO_SELL = conver_soup_euro[1].text
EURO_CB = conver_soup_euro[2].text
EURO_TR = conver_soup_moex_euro[0].text
EURO_TR_time = conver_soup_moex_euro_time[0].text
# Переменные PLN
PL_BUY = conver_soup_pl[0].text
PL_SELL = conver_soup_pl[1].text
# Прочее
actual_time = conver_soup_time[0].text
#########################################

    # Начало 
bot = telebot.TeleBot(config.token)
@bot.message_handler(commands=['start'])
def get_user_info(message):
    # Вывод клавиатуры Шаг 1 
    markup_inline =types.InlineKeyboardMarkup(row_width=1)
    btn_inline_1 = types.InlineKeyboardButton(text=" Начать ",callback_data = 'current')
    markup_inline.add(btn_inline_1)
    bot.send_message(message.chat.id, "Привет👋🏻" + message.from_user.first_name + " я бот \n \n Моя задача  показывать лучший курс валюты в Калининграде. \n \n Курс валюты по Центральному банку \n \n  Курс валюты  Московской биржы  \n \n \n  Для повторного запуска используете комманду /start или напишите в чат /start " ,reply_markup = markup_inline)

@bot.callback_query_handler(func=lambda call:True)
def answer(call):
    if call.data== 'current':
    # Вывод клавиатуры Шаг 1
        markup_inline_step_2 =types.InlineKeyboardMarkup(row_width=3)
        btn_inline_6_step_2 = types.InlineKeyboardButton(text="Обмена",callback_data = 'BB')
        btn_inline_4_step_2 = types.InlineKeyboardButton(text="Курс ЦБ",callback_data = 'cb')
        btn_inline_5_step_2 = types.InlineKeyboardButton(text="Курс Биржы",callback_data = 'tr')
        markup_inline_step_2.add(btn_inline_4_step_2,btn_inline_5_step_2,btn_inline_6_step_2)
        msg = bot.send_message(call.message.chat.id,"✅Пожалуйста выберете раздел",reply_markup = markup_inline_step_2)
    # Вывод клавиатуры Шаг 2
    if call.data== 'BB':
        markup_inline_step_21 =types.InlineKeyboardMarkup(row_width=2)
        btn_inline_1_step_21 = types.InlineKeyboardButton(text="🇺🇸 Доллар ",callback_data = 'dollars')
        btn_inline_2_step_21 = types.InlineKeyboardButton(text="🇪🇺 Евро",callback_data = 'euro')
        btn_inline_3_step_21 = types.InlineKeyboardButton(text="🇵🇱 PL",callback_data = 'pln')
        markup_inline_step_21.add(btn_inline_1_step_21,btn_inline_2_step_21,btn_inline_3_step_21)
        bot.send_message(call.message.chat.id," \n \n ✅Узнать самый выгодный курс в пунтках обмена",reply_markup = markup_inline_step_21)
    # Вывод dollars Шаг 3 
    elif call.data =='dollars':
        bot.send_message(call.message.chat.id,"🇺🇸 Покупка|Продажа \n  \n☑️  {0}  |  {1} \n \n \n Время обновления {2} ".format(USD_BUY,USD_SELL,actual_time ))

    # Вывод euro Шаг 3 
    elif call.data =='euro':
        bot.send_message(call.message.chat.id,"🇪🇺 Покупка|Продажа \n  \n ☑️  {0}  |  {1} \n \n \n Время обновления  {2} ".format(EURO_BUY,EURO_SELL,actual_time ))


    # Вывод злоты Шаг 3 
    elif call.data =='pln':
        bot.send_message(call.message.chat.id,"🇵🇱 Покупка|Продажа \n  \n ☑️  {0}  |  {1} \n \n \n Время обновления  {2} ".format(PL_BUY,PL_SELL,actual_time ))

    # Что то другое Шаг 4 
    if call.data =='cb':
        markup_inline_step_3 =types.InlineKeyboardMarkup(row_width=2)
        btn_inline_1_step_3 = types.InlineKeyboardButton(text="🇺🇸 Доллар ",callback_data = 'dollars_cb')
        btn_inline_2_step_3 = types.InlineKeyboardButton(text="🇪🇺 Евро",callback_data = 'euro_cb')
        markup_inline_step_3.add(btn_inline_1_step_3,btn_inline_2_step_3)
        bot.send_message(call.message.chat.id," \n \n ✅ Узнать курс  по Центральному Банку ",reply_markup = markup_inline_step_3)
    # Вывод dollars Шаг 4.1
    elif call.data =='dollars_cb':
        bot.send_message(call.message.chat.id,'\n \n'"🇺🇸 {} ".format(USD_CB))
    # Вывод euro Шаг 4.2    
    elif call.data == 'euro_cb':
        bot.send_message(call.message.chat.id,'\n \n'"🇪🇺 {} ".format(EURO_CB))
    
    # Что то другое Шаг 5
    if call.data =='tr':
        markup_inline_step_4 =types.InlineKeyboardMarkup(row_width=2)
        btn_inline_1_step_4 = types.InlineKeyboardButton(text="🇺🇸 Доллар ",callback_data = 'dollars_tr')
        btn_inline_2_step_4 = types.InlineKeyboardButton(text="🇪🇺 Евро",callback_data = 'euro_tr')
        markup_inline_step_4.add(btn_inline_1_step_4,btn_inline_2_step_4)
        bot.send_message(call.message.chat.id,"\n \n ✅ Узнать курс  Московской Биржы ",reply_markup = markup_inline_step_4)
    # Вывод dollars Шаг 5.1  
    elif call.data =='dollars_tr':
        bot.send_message(call.message.chat.id,'\n \n'"🇺🇸 {0} \n \n Обновлено {1} ".format(USD_TR,USD_TR_time))
    # Вывод euro Шаг 5.2   
    elif call.data == 'euro_tr':
        bot.send_message(call.message.chat.id,'\n \n'"🇪🇺 {0} \n \n Обновлено {1} ".format(EURO_TR,EURO_TR_time))


@bot.message_handler(commands=['help'])
def get_user_help(message):
    bot.send_message(message.chat.id, "Привет👋🏻" + message.from_user.first_name + " мой создатель @S19S93 , вся информация была взята https://kaliningrad.bankiros.ru/ ")



bot.polling(none_stop=True)