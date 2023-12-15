import random
import string
import telebot

bot = telebot.TeleBot('6671933355:AAHDjP8ZIHh2e4sA7geU0tN4XUsEO-dLR_o')

passwords = {}
@bot.message_handler(commands=['start'])
def start(message):
    password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    passwords[message.chat.id] = password

    bot.send_message(message.chat.id, f"Ваш пароль для входа в игру: {password}")

@bot.message_handler(func=lambda message: True)
def check_password(message):
    if message.text == passwords.get(message.chat.id):
        bot.send_message(message.chat.id, "Вы успешно вошли в игру!")
    else:
        bot.send_message(message.chat.id, "Неверный пароль!")

bot.polling()
