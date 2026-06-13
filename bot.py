import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import TOKEN
from db import Database

bot = telebot.TeleBot(TOKEN)
db = Database()

otvety = {
    'Как оформить заказ?': 'Для оформления заказа, пожалуйста, выберите интересующий вас товар и нажмите кнопку "Добавить в корзину", затем перейдите в корзину и следуйте инструкциям для завершения покупки.',
    'Как узнать статус моего заказа?': 'Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем сайте и перейдя в раздел "Мои заказы". Там будет указан текущий статус вашего заказа.',
    'Как отменить заказ?': 'Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержки как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки.',
    'Что делать, если товар пришел поврежденным?': 'При получении поврежденного товара, пожалуйста, сразу свяжитесь с нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара.',
    'Как связаться с вашей технической поддержкой?': 'Вы можете связаться с нашей технической поддержкой через телефон на нашем сайте или написать нам в чат-бота.',
    'Как узнать информацию о доставке?': 'Информацию о доставке вы можете найти на странице оформления заказа на нашем сайте. Там указаны доступные способы доставки и сроки.'
}

def main_menu_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('Как оформить заказ?'))
    keyboard.add(KeyboardButton('Как узнать статус моего заказа?'))
    keyboard.add(KeyboardButton('Как отменить заказ?'))
    keyboard.add(KeyboardButton('Что делать, если товар пришел поврежденным?'))
    keyboard.add(KeyboardButton('Как связаться с вашей технической поддержкой?'))
    keyboard.add(KeyboardButton('Как узнать информацию о доставке?'))
    keyboard.add(KeyboardButton('Связаться со специалистом'))
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в поддержку "Продаем все на свете"!\n\nВыберите интересующий вас вопрос из меню ниже:', reply_markup=main_menu_keyboard())

@bot.message_handler(func=lambda message: message.text in otvety)
def handle_questions(message):
    bot.send_message(message.chat.id, otvety[message.text])

@bot.message_handler(func=lambda message: message.text == 'Связаться со специалистом')
def ask_specialist(message):
    msg = bot.send_message(message.chat.id, 'Опишите вашу проблему:')
    bot.register_next_step_handler(msg, save_request, message.chat.id, message.from_user.username)

def save_request(message, user_id, username):
    if not message.text:
        bot.send_message(user_id, 'Пожалуйста, отправьте текстовое сообщение.')
        return
    
    db.add_request(user_id, username, message.text)
    bot.send_message(user_id, 'Заявка передана специалисту. Мы свяжемся с вами.')

if __name__ == '__main__':
    bot.infinity_polling()