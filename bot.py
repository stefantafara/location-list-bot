import telebot
import config

token = config.token

bot = telebot.TeleBot()

@bot.message_handler()
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id=message.chat_id, text='Hi there')

bot.polling(none_stop=True, timeout=123)