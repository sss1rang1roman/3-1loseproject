import telebot
from M1L3.config import token

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message:
        chat_id = message.chat.id
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id)
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'Новый пользователь')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)


@bot.message_handler(func=lambda message: True)
def check_links(message):
    if message.text and ('http://' in message.text.lower() or 'https://' in message.text.lower() or 't.me/' in message.text.lower()):
        chat_id = message.chat.id
        user_id = message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status
        
        if user_status not in ['administrator', 'creator']:
            try:
                bot.ban_chat_member(chat_id, user_id)
                bot.delete_message(chat_id, message.message_id)
                bot.send_message(chat_id, f"Пользователь @{message.from_user.username} был забанен за отправку ссылки.")
            except Exception as e:
                print(f"Ошибка при бане пользователя: {e}")


@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
   
    for new_user in message.new_chat_members:
        welcome_text = f" Добро пожаловать, {new_user.first_name}!\nРады видеть тебя в нашем чате!"
        bot.send_message(message.chat.id, welcome_text)
        bot.approve_chat_join_request(message.chat.id, new_user.id)

@bot.message_handler(commands=['check_admin'])
def check_admin_rights(message):
    chat_id = message.chat.id
    bot_user = bot.get_me()
    try:
        member = bot.get_chat_member(chat_id, bot_user.id)
        if member.status == 'administrator':
            bot.reply_to(message, "✅ Я имею права администратора!")
        else:
            bot.reply_to(message, "❌ У меня нет прав администратора!")
    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")
        
bot.infinity_polling(none_stop=True)