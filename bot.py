import telebot, os, redis, logging
from telebot import types

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

button_names = ['help', 'add', 'list', 'reset']

# creating keyboard
def create_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    buttons = [types.InlineKeyboardButton(text=button, callback_data=button) for button in button_names]
    keyboard.add(*buttons)
    return keyboard

# button handler
@bot.callback_query_handler(func=lambda x: True)
def handle_button_callback(callbackquery):
    message = callbackquery.message
    text = callbackquery.data
    print(f'text: {text}')
    if text == 'add':
        command_add(message)
    elif text == 'list':
        list_locations(message)
    elif text == 'reset':
        reset(message)
    elif text == 'help':
        help(message)


# ping command handler
@bot.message_handler(commands=['ping'])
def handle_message(message):
    # receiving message
    print(f'message received: {message.text}')
    # reply
    print(f'sending reply...')
    bot.send_message(chat_id=message.chat.id, text='Hi!')
    bot.send_message(chat_id=message.chat.id, text=f'Your text was: {message.text}', reply_markup=create_keyboard())
    print(f'reply sent')


# help/start command handler
@bot.message_handler(commands=['help', 'start'])
def help(message):
    bot.send_message(chat_id=message.chat.id, text="""
Hi there, I am Location List Bot.
PLease use these commands:
/help - for help
/add - to add new location
/list - to watch list of 10 last locations
/reset - to reset all locations
""", reply_markup=create_keyboard())


# add command handler: step 1
@bot.message_handler(commands=['add'])
def command_add(message):
    print('requesting location...')
    bot.send_message(chat_id=message.chat.id, text='Please input address')
    bot.register_next_step_handler(message, add_location)


# add command handler: step 2
def add_location(message):
    print('pushing location to Redis...')
    r.lpush(message.chat.id, message.text)
    print('pushed successfully')
    bot.send_message(chat_id=message.chat.id, text='Thank you! Location was successfully added.',
                     reply_markup=create_keyboard())


# list command handler
@bot.message_handler(commands=['list'])
def list_locations(message):
    locations = r.lrange(message.chat.id, 0, 9)
    if len(locations) == 0:
        bot.send_message(chat_id=message.chat.id, text='Sorry your locations list is empty')
    else:
        for location in locations:
            print(f'location: {location}')
            bot.send_message(chat_id=message.chat.id, text=location)
    bot.send_message(chat_id=message.chat.id, text="Please press the button", reply_markup=create_keyboard())


# reset command handler: step 1
@bot.message_handler(commands=['reset'])
def reset(message):
    print(f'deleting all locations with ID: {message.chat.id}')
    r.delete(message.chat.id)
    bot.send_message(chat_id=message.chat.id, text='All locations were deleted', reply_markup=create_keyboard())


if __name__ == '__main__':
    bot.polling()
