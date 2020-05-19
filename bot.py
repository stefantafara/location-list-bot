import telebot, os

# there is no need in config file. use Heroku config
# import config

# reading token from config...
print(f'reading token from config...')
token = os.environ['TOKEN']
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
