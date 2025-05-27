import os
import json
import random

import telebot
from telebot import types

from yt_dlp import YoutubeDL

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


DONATION_LINK = 'https://google.com' # Paste your remote payment link here

MAX_SIZE_MB = 50

MAX_DURATION_SEC = 1800


bot = telebot.TeleBot(os.getenv('TOKEN'))

ydl_config = {
    'format': 'bestaudio',
    'outtmpl': 'temp/%(title)s.%(ext)s',
    'noplaylist': True,
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }]
}

with open('responses.json', 'r') as f:
	responses = json.load(f)


@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(types.KeyboardButton('💰 Donate'))
	bot.send_message(message.chat.id, random.choice(responses['greetings']), reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help(message):
	bot.send_message(message.chat.id, random.choice(responses['link']['entry']))


@bot.message_handler(func=lambda m: m.text in ['💰 Donate', '/donate'])
def handle_markup(message):
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton('Donation page', url=DONATION_LINK))
	bot.send_message(message.chat.id, random.choice(responses['donation']['entry']), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_link(message):
	temp_message = bot.send_message(message.chat.id, random.choice(responses['link']['waiting']))
	with YoutubeDL(ydl_config) as ydl:
		try:
			ydl_info = ydl.extract_info(message.text, download=False)

			ydl_audio_filesize = ydl_info.get('filesize') or ydl_info.get('filesize_approx')
			if ydl_audio_filesize and ydl_audio_filesize > MAX_SIZE_MB * 1024 * 1024:
				bot.delete_message(message.chat.id, temp_message.message_id)
				bot.send_message(message.chat.id, random.choice(responses['link']['error']['filesize']))
				return

			ydl_duration = ydl_info.get('duration', 0)
			if ydl_duration > MAX_DURATION_SEC:
				bot.delete_message(message.chat.id, temp_message.message_id)
				bot.send_message(message.chat.id, random.choice(responses['link']['error']['duration']))
				return

			ydl_info = ydl.extract_info(message.text, download=True)

		except Exception:
			bot.delete_message(message.chat.id, temp_message.message_id)
			bot.send_message(message.chat.id, random.choice(responses['link']['error']['link']))
			return

	ydl_path = os.path.join('temp', f'{ydl_info['title']}.mp3')
	with open(ydl_path, 'rb') as f:
		bot.send_audio(message.chat.id, f)
	bot.delete_message(message.chat.id, temp_message.message_id)
	os.remove(ydl_path)
	bot.send_message(message.chat.id, random.choice(responses['link']['success']))


bot.infinity_polling()