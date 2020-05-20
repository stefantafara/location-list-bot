import telebot, os, redis, logging

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

# set logger
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

# Redis
r = redis.from_url(os.environ.get("REDIS_URL"))


@bot.message_handler(commands=['ping'])
def handle_message(message):
    # receiving message
    print(f'message received: {message.text}')
    # reply
    print(f'sending reply...')
    bot.send_message(chat_id=message.chat.id, text='Hi!')
    bot.send_message(chat_id=message.chat.id, text=f'Your text was: {message.text}')
    print(f'reply sent')


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am Location List Bot.
PLease use these commands:
/help - for help
/add - to add new location
/list - to watch list of 10 last locations
/reset - to reset all locations
""")


@bot.message_handler(commands=['add'])
def command_add(message):
    print('requesting location...')
    bot.send_message(chat_id=message.chat.id, text='Please input location')
    bot.register_next_step_handler(message, add_location)


def add_location(message):
    print('pushing location to Redis...')
    r.lpush(message.chat.id, message.text)
    print('pushed successfully')
    bot.send_message(chat_id=message.chat.id, text='Thank you! Location was successfully added.')


@bot.message_handler(commands=['list'])
def list_locations(message):
    bot.send_message(chat_id=message.chat.id, text='Please input location')
    for location in r.lrange(message.chat.id, 0, 9):
        print(f'location: {location}')
        bot.send_message(chat_id=message.chat.id, text=location)


@bot.message_handler(commands=['reset'])
def send_welcome(message):
    print(f'deleting all locations with ID: {message.chat.id}')
    r.delete(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text='All locations were deleted')


if __name__ == '__main__':
    bot.polling()
