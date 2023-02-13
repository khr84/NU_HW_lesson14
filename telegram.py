import telebot
import get_html_news
import os
from datetime import datetime

TOKEN = '6219533363:AAHKMeXcVIZlUvNWdyG1LCYpW-HEagB-Zfw'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Hi, how are you doing?")

@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, "Press '/' to see list of commands")

@bot.message_handler(commands=['news_file'])
def get_news_file(message):
	dt = message.text.split(' ')[1:]
	try:
		datetime.strptime(dt[0], '%Y/%m/%d')
		bot.reply_to(message, "Start get news")
	except:
		bot.reply_to(message, f'"Date in wrong format, try again" {dt}')
	news = get_html_news.AUTO_NEWS()
	news_list = news.get_news(dt[0])
	bot.send_message(message.chat.id, f'Find {news.cnt} on {dt[0]}')
	if os.path.exists(os.path.join(news.dir,'news_file.txt')):
		with open(os.path.join(news.dir,'news_file.txt'), 'r', encoding='utf-8') as f:
			bot.send_document(message.chat.id, f)
	else:
		bot.send_message(message.chat.id, "Something gone wrong")


bot.polling()