import telebot
import config


bot = telebot.TeleBot(config.bot_token)

users = config.fake_database['users']

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)

    btn1 = telebot.types.KeyboardButton('Кошелёк')
    btn2 = telebot.types.KeyboardButton('Перевести')
    btn3 = telebot.types.KeyboardButton('История')

    markup.add(btn1, btn2, btn3)

    text = f'Привет {message.from_user.full_name}, я твой бот-криптокошелек, \n' \
           'у меня ты можешь хранить и отправлять биткоины'

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='Кошелёк')
def wallet(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                               resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    markup.add(btn1)
    balance = 0
    text = f'Ваш баланс: {balance}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='Перевести')
def transaction(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                               resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    markup.add(btn1)
    text = 'Введите адрес кошелька, куда хотите перевести: '
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='История')
def history(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                               resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    markup.add(btn1)
    transactions = []
    text = f'Ваши транзакции: {transactions}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='Меню')
def menu(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                               resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Кошелёк')
    btn2 = telebot.types.KeyboardButton('Перевести')
    btn3 = telebot.types.KeyboardButton('История')
    markup.add(btn1, btn2, btn3)

    text = 'Главное меню'

    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(regexp='Я в консоли')
def print_me(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                               resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    markup.add(btn1)
    print(message.from_user.to_dict())
    text = f'Ты: {message.from_user.to_dict()}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.from_user.id == config.tg_admin_id and message.text == 'Админка')
def admin_panel(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2,
                                               resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Общий баланс')
    btn2 = telebot.types.KeyboardButton('Все пользователи')
    btn3 = telebot.types.KeyboardButton('Данные по пользователю')
    btn4 = telebot.types.KeyboardButton('Удалить пользователя')
    markup.add(btn1, btn2, btn3, btn4)
    text = 'Админ-панель'
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(func=lambda message: message.from_user.id == config.tg_admin_id and message.text == 'Все пользователи')
def all_users(message):
    text = 'Пользователи: '
    inline_markup = telebot.types.InlineKeyboardMarkup()
    for user in users:
        inline_markup.add(telebot.types.InlineKeyboardButton
            (
            text=f'Пользователь: {user["name"]}',
            callback_data=f'user_{user["id"]}'
            ))
    bot.send_message(message.chat.id, text, reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    query_type = call.data.split('_')[0]
    if query_type == 'user':
        user_id = call.data.split('_')[1]
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            if str(user['id']) == user_id:
                inline_markup.add(
                    telebot.types.InlineKeyboardButton(
                        text="Назад",
                        callback_data="users"
                    ),
                    telebot.types.InlineKeyboardButton(
                        text="Удалить пользователя",
                        callback_data=f"delete_user_{user_id}"
                    )
                )

        bot.edit_message_text(text=f"""Данные по пользователю:
                                    ID: {user["id"]}
                                    Имя: {user["name"]}
                                    Ник: {user["nick"]}
                                    Баланс: {user["balance"]}""",
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup
                              )
        print(f'Запрошен {user}')

    if query_type == 'users':
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            inline_markup.add(telebot.types.InlineKeyboardButton(
                text=f'Пользователь: {user["name"]}',
                callback_data=f'user_{user["id"]}'
            ))
        bot.edit_message_text(text='Пользователи: ',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup
                              )

    if query_type == 'delete' and call.data.split('_')[1] == 'user':
        user_id = int(call.data.split('_')[2])
        for i, user in enumerate(users):
            print(user['name'])
            if user['id'] == user_id:
                print(f'Удалён пользователь: {users[i]}')
                users.pop(i)
        inline_markup = telebot.types.InlineKeyboardMarkup()
        for user in users:
            inline_markup.add(telebot.types.InlineKeyboardButton(
                text=f'Пользователь: {user["name"]}',
                callback_data=f'user_{user["id"]}'
            ))
        bot.edit_message_text(text='Пользователи',
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=inline_markup
                              )

@bot.message_handler(func=lambda message: message.from_user.id == config.tg_admin_id and message.text == "Общий баланс")
def total_balance(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('Меню')
    btn2 = telebot.types.KeyboardButton('Админка')
    markup.add(btn1, btn2)
    balance = 0
    for user in users:
        balance += user['balance']
    text = f'Общий баланс: {balance}'
    bot.send_message(message.chat.id, text, reply_markup=markup)


bot.infinity_polling()
