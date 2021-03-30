import telebot
from telebot import *
from settings import *

bot = telebot.TeleBot(Token, skip_pending=True)
yasaklılar=[]
whitelist = [777000]
@bot.message_handler(content_types=["text"])
def kontrol(message):
    global yasaklılar
    if message.from_user.id in whitelist:
        pass
    else:
        markup = InlineKeyboardMarkup(row_width = 1)
        katildim = InlineKeyboardButton("Katıldım", callback_data="katildim")
        markup.add(katildim)
        user_id = message.from_user.id
        admin = bot.get_chat_member(message.chat.id, user_id)
        if admin.status == "creator" or admin.status == "administrator":
            pass
        else:
            for kanal in Channels:
                user = bot.get_chat_member(kanal, user_id)
                if user.status == "left":
                    bot.restrict_chat_member(message.chat.id, user_id)
                    mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
                    bot.reply_to(message, f"{mention} Lütfen @orgutresmikanal'ına katılın", reply_markup=markup, parse_mode="markdown")
                    yasaklılar.append(user_id)
                    bot.send_message(message.chat.id, f"{yasaklılar}")

@bot.callback_query_handler(func=lambda call: call.data == "katildim")
def katildim(call):
    global yasaklılar
    user_id = call.from_user.id
    if user_id in yasaklılar:
        for kanal in Channels:
            user = bot.get_chat_member(kanal, user_id)
            if user.status == "left":
                pass
            else:
                bot.restrict_chat_member(call.message.chat.id, user_id, can_send_messages=True)
                yasaklılar.remove(user_id)
                bot.send_message(call.message.chat.id, f"{yasaklılar}")


print("bot aktif")
if __name__=="__main__":
    bot.polling(none_stop=True)
