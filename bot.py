import os
import json
import random

import telebot
from telebot import types

from yt_dlp import YoutubeDL

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())


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


MARKUP_DONATION = '💰 Donate'


@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(types.KeyboardButton(MARKUP_DONATION))
	bot.send_message(message.chat.id, random.choice(responses['greetings']), reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help(message):
	bot.send_message(message.chat.id, random.choice(responses['link']['entry']))


@bot.message_handler(func=lambda m: m.text in [MARKUP_DONATION, '/donate'])
def handle_markup(message):
	markup = types.InlineKeyboardMarkup()
	markup.add(types.InlineKeyboardButton('Donation page', url=os.getenv('DONATION_LINK')))
	bot.send_message(message.chat.id, random.choice(responses['donation']['entry']), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def handle_link(message):
	temp_message = bot.send_message(message.chat.id, random.choice(responses['link']['waiting']))
	with YoutubeDL(ydl_config) as ydl:
		try:
			ydl_info = ydl.extract_info(message.text, download=True)
		except Exception:
			bot.delete_message(message.chat.id, temp_message.message_id)
			bot.send_message(message.chat.id, random.choice(responses['link']['error']))
			return
	"""ydl_dur = ydl_info['duration']
	HH, mm, ss = ydl_dur//3600, (ydl_dur%3600)//60, ydl_dur%60
	HHmmss_arr = [HH, mm, ss] if HH else [mm,ss]
	ydl_output = ydl_info['title'] + ' (' + ':'.join(str(i).zfill(2) for i in HHmmss_arr) + ')'
	bot.delete_message(message.chat.id, temp_message.message_id)
	bot.send_message(message.chat.id, ydl_output)"""
	ydl_path = os.path.join('temp', [i for i in os.listdir('temp') if i != '.gitkeep'][0])
	with open(ydl_path, 'rb') as f:
		bot.send_audio(message.chat.id, f)
	bot.delete_message(message.chat.id, temp_message.message_id)
	os.remove(ydl_path)
	bot.send_message(message.chat.id, random.choice(responses['link']['success']))


bot.infinity_polling()