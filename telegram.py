import telebot
import get_html_news
import os
import speedtest
from datetime import datetime

TOKEN = '6219533363:AAHKMeXcVIZlUvNWdyG1LCYpW-HEagB-Zfw'
bot = telebot.TeleBot(TOKEN)

exist_search = False

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Hi, how are you doing?")

@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, "Press '/' to see list of commands")

@bot.message_handler(commands=['news_file'])
def get_news_file(message):
	global exist_search
	if exist_search:
		bot.reply_to(message, "All servers are busy? please try later")
	else:
		exist_search = True
		dt = message.text.split(' ')[1:]
		try:
			datetime.strptime(dt[0], '%Y/%m/%d')
			if datetime.strptime(dt[0], '%Y/%m/%d') > datetime.now():
				bot.reply_to(message, "Enter date less now")
			else:
				bot.reply_to(message, "Start get news")
				news = get_html_news.AUTO_NEWS()
				news_list = news.get_news(dt[0])
				bot.send_message(message.chat.id, f'Find {news.cnt} on {dt[0]}')
				if os.path.exists(os.path.join(news.dir, 'news_file.txt')):
					with open(os.path.join(news.dir, 'news_file.txt'), 'r', encoding='utf-8') as f:
						bot.send_document(message.chat.id, f)
				else:
					bot.send_message(message.chat.id, "Something gone wrong")
		except:
			bot.reply_to(message, f'"Date in wrong format, try again" {dt}')
	exist_search = False

@bot.message_handler(commands=['news'])
def get_news(message):
	global exist_search
	if exist_search:
		bot.reply_to(message, "All servers are busy? please try later")
	else:
		exist_search = True
		dt = message.text.split(' ')[1:]
		try:
			datetime.strptime(dt[0], '%Y/%m/%d')
			if datetime.strptime(dt[0], '%Y/%m/%d') > datetime.now():
				bot.reply_to(message, "Enter date less now")
			else:
				bot.reply_to(message, "Start get news")
				news = get_html_news.AUTO_NEWS()
				news_list = news.get_news(dt[0])
				bot.send_message(message.chat.id, f'Find {news.cnt} on {dt[0]}')
				for i in range(news.cnt):
					bot.send_message(message.chat.id,
									 f'{i + 1}. {news_list[i]["news_text"]} (link: {news_list[i]["news_link"]})')
		except:
			bot.reply_to(message, f'"Date in wrong format, try again" {dt}')
	exist_search = False

@bot.message_handler(commands=['speedtest'])
def get_speedtest(message):
	inet = speedtest.Speedtest()
	download = float(str(inet.download())[0:2] + "."
					 + str(round(inet.download(), 2))[1]) * 0.125
	uploads = float(str(inet.upload())[0:2] + "."
					+ str(round(inet.download(), 2))[1]) * 0.125
	bot.reply_to(message, f'Dowload speed {download}, Upload speed {uploads}')

@bot.message_handler(content_types=['sticker'])
def reply_sticker(message):
	text = message.sticker.emoji
	bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def reply_text(message):
	text = message.text[::-1]
	bot.reply_to(message, text)



bot.polling()