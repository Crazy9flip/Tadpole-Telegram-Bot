import telebot
from config import TOKEN

from yt_dlp import YoutubeDL
import os
import json
import random

bot = telebot.TeleBot(TOKEN)

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

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	#bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAANiaAzpviI4qhcGeoos2biR_25WNK0AAicDAAK1cdoGD_Tez6DF3ew2BA')
	bot.send_message(message.chat.id, random.choice(responses['greetings']))

"""@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    print(message.sticker.file_id)"""

@bot.message_handler(content_types=['text'])
def handle_link(message):        
	with YoutubeDL(ydl_config) as ydl:
		try:
			ydl_info = ydl.extract_info(message.text, download=True)
		except Exception:
			bot.send_message(message.chat.id, random.choice(responses['link']['error']))
			return
		
	ydl_dur = ydl_info['duration']
	HH, mm, ss = ydl_dur//3600, (ydl_dur%3600)//60, ydl_dur%60
	HHmmss_arr = [HH, mm, ss] if HH else [mm,ss]
	ydl_output = ydl_info['title'] + ' (' + ':'.join(str(i).zfill(2) for i in HHmmss_arr) + ')'
	bot.send_message(message.chat.id, ydl_output)

	ydl_path = os.path.join('temp', [i for i in os.listdir('temp') if not i.startswith('.')][0])
	with open(ydl_path, 'rb') as f:
		bot.send_audio(message.chat.id, f)
	os.remove(ydl_path)

bot.infinity_polling()