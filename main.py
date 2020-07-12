from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

class User():
	def __init__(self, chat_id, name):
		self.id = chat_id
		self.name = name

status = {}
user = {}

def start(update, context):
	global status
	chat_id = update.effective_chat.id
	status[chat_id] = get_name
	context.bot.send_message(chat_id=chat_id, text="Assalomu alaykum!\nAvval Ismingizni yuboring.")

def error_message(update, context):
	chat_id = update.effective_chat.id
	context.bot.send_message(chat_id, text="Bot sizdan hech narsani kutmayapti!")

def echo(update, context):
	global status
	chat_id = update.effective_chat.id
	status.get(chat_id, error_message)(update, context)

def get_name(update, context):
	global user, status
	chat_id = update.effective_chat.id
	name = update.message.text
	user[chat_id] = User(chat_id, name)
	status[chat_id] = get_age
	context.bot.send_message(chat_id=chat_id, text="Endi yoshingizni yuboring.\n\n(Yoshingiz shunchaki blank to`lg`izishchun kere. Lekin blank to`lmasa anketa yuborilmidi.)")

def get_age(update, context):
	global user, status
	chat_id = update.effective_chat.id
	try:
		age = int(update.message.text)
	except ValueError:
		context.bot.send_message(chat_id=chat_id, text='Yoshingizni boshqattan sonlar orqali yuboring.')
	else:
		user[chat_id].age = age
		status[chat_id] = get_info
		context.bot.send_message(chat_id, text='Endi Python dasturlash tili bo`yicha nimalarni bilishingizni yuboring.')

def get_info(update, context):
	global user, status
	chat_id = update.effective_chat.id
	info = update.message.text
	user[chat_id].info = info
	user[chat_id].username = update.effective_chat.username
	send_user_to_me(context, user[chat_id])
	context.bot.send_message(chat_id, text="Anketa yuborildi. Bizdan aloqa kuting.")

def send_user_to_me(context, user):
	text = f'Bittasi kutvotti: @{user.username}\nIsmi: {user.name}\nYoshi: {user.age}\nAbout: {user.info}'
	context.bot.send_message(496583471, text=text)

updater = Updater(token='1049614575:AAHmS6ol7OiA0c0h9hiTaYG_bn9QO3OjV0M', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

start_handler = CommandHandler('start', start)
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(echo_handler)
updater.start_polling()
updater.idle()