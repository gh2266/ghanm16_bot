import os
import telebot
from flask import Flask, request

API_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

def is_user_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    if is_user_subscribed(message.from_user.id):
        bot.reply_to(message, "أهلاً بك! أنت مشترك في القناة.")
    else:
        bot.reply_to(message, f"يرجى الاشتراك في القناة أولاً: https://t.me/{CHANNEL_USERNAME.lstrip('@')}")

@app.route(f'/{API_TOKEN}', methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route('/')
def index():
    return 'البوت شغّال!', 200

if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL") + '/' + API_TOKEN)
