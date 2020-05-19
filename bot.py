import telebot
import config

# reading token from config...
print(f'reading token from config...')
token = config.token
print(f'token: {token}')
# starting bot...
print('starting bot...')
bot = telebot.TeleBot(token)
print('bot started.')


@bot.message_handler()
def handle_message(message):
    # receiving message
    print(f'message received: {message.text}')
    # reply
    print(f'sending reply...')
    bot.send_message(chat_id=message.chat_id, text='Hi there')
    print(f'reply sent')

if __name__ == '__main__':
  bot.polling()
