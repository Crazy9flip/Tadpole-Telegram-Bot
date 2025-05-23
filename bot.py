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

user_state = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	markup.add(
		types.KeyboardButton('🔁 Convert'), 
		types.KeyboardButton('💰 Donate')
		)
	bot.send_message(message.chat.id, random.choice(responses['greetings']), reply_markup=markup)


"""@bot.message_handler(content_types=['sticker'])
def handle_sticker(message):
    print(message.sticker.file_id)"""


@bot.message_handler(func=lambda m: m.text in ['🔁 Convert', '💰 Donate'])
def handle_markup(message):
	if message.text == '🔁 Convert':
		bot.send_message(message.chat.id, random.choice(responses['link']['entry']))
		user_state[message.from_user.id] = 'convert'

	if message.text == '💰 Donate':
		bot.send_message(message.chat.id, random.choice(responses['donation']['entry']))
		user_state[message.from_user.id] = 'donate'


@bot.message_handler(func=lambda m: m.text and user_state.get(m.from_user.id) == 'donate')
def handle_donation(message):
	bot.send_message(message.chat.id, 'Alas, the coffers be sealed for now. Donations shan\'t be taken at this hour.')
	"""bot.send_invoice(
		message.chat.id,
		title='Donation',
		description='Toss a coin, kind soul!',
		provider_token='381764678:TEST:6a1d84dc-cd7c-4a19-9d2a-xxxxxx',
		currency='USD',
		prices=[types.LabeledPrice(label='If thy heart be kind', amount=100)],
		start_parameter='donation',
		invoice_payload='donation'
	)"""
	user_state[message.from_user.id] = None


"""@bot.pre_checkout_query_handler(func=lambda q: True)
def handle_checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def send_payment_success(message):
    bot.send_message(message.chat.id, random.choice(responses['donation']['success']))"""


@bot.message_handler(content_types=['text'])
def handle_link(message):
	if user_state.get(message.from_user.id) == 'convert':
		temp_message = bot.send_message(message.chat.id, random.choice(responses['link']['waiting']))

		with YoutubeDL(ydl_config) as ydl:
			try:
				ydl_info = ydl.extract_info(message.text, download=True)
			except Exception:
				bot.send_message(message.chat.id, random.choice(responses['link']['error']['link']))
				return

		"""ydl_dur = ydl_info['duration']
		HH, mm, ss = ydl_dur//3600, (ydl_dur%3600)//60, ydl_dur%60
		HHmmss_arr = [HH, mm, ss] if HH else [mm,ss]
		ydl_output = ydl_info['title'] + ' (' + ':'.join(str(i).zfill(2) for i in HHmmss_arr) + ')'
		bot.delete_message(message.chat.id, temp_message.message_id)
		bot.send_message(message.chat.id, ydl_output)"""

		ydl_path = os.path.join('temp', [i for i in os.listdir('temp') if not i.startswith('.')][0])
		with open(ydl_path, 'rb') as f:
			bot.send_audio(message.chat.id, f)
		bot.delete_message(message.chat.id, temp_message.message_id)
		os.remove(ydl_path)

		bot.send_message(message.chat.id, random.choice(responses['link']['success']))

	else:
		bot.send_message(message.chat.id, random.choice(responses['link']['error']['mode']))


bot.infinity_polling()