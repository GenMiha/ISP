import logging
import threading
import time

import schedule

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CallbackQueryHandler, MessageHandler, Filters, CommandHandler

from app import database, app
from config import TOKEN
from models import User, Link
from text_constants import START_MESSAGE
from vid_utils import Video, BadLink

class MessageReact(object):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)
    user_password = ""
    user_name = ""
    mychat_id = 0
    user_id = 0
    ready_to_reference = False
    ready_to_password = False
    ready_to_reg = False
    password_default = "aaa"
    update = ""
    bot = ""

    def __init__(self, bottoken):
        self.updater = Updater(token=bottoken, use_context=False)
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.download_chosen_format))

    def bot_load(self):
        handler = MessageHandler(Filters.text | Filters.command, self.handle_message)
        self.updater.dispatcher.add_handler(handler)
        self.updater.start_polling()
        self.bot = self.updater.bot

    def bot_starts(self, bot, update):
        bot.sendMessage(chat_id=update.message.chat_id, text=START_MESSAGE)
        self.update = update

    def handle_message(self, bot, update):
        self.mychat_id = update.message.chat_id
        if self.ready_to_reference == False:
            if update.message.text == "/start":
                self.bot_starts(bot, update)
                user_par = self.find_user_in_database(update.message.chat.username)
                if user_par:
                    self.user_id = user_par[0]
                    self.user_password = user_par[1]
                self.ready_to_password = True
            else:
                if update.message.text == "/reg":
                    bot.sendMessage(chat_id=self.mychat_id, text="Please, enter your new password.")
                    self.ready_to_reg = True
                    self.ready_to_password = False
                    self.ready_to_reference = False
                else:
                    if self.ready_to_reg == True:
                        user_par = self.find_user_in_database(update.message.chat.username)
                        if user_par[0] == 0:
                            self.add_user_to_database(update.message.chat.username, update.message.text)
                            self.ready_to_reg = False
                            # bot.sendMessage(chat_id=self.mychat_id, text="Enter '/start' now.")
                        else:
                            bot.sendMessage(chat_id=self.mychat_id,
                                            text="You are in base already. Enter '/start' please!")
                if self.ready_to_password == True:
                    if update.message.text == self.user_password:
                        bot.sendMessage(chat_id=self.mychat_id,
                                        text=f"Nice to see you, {update.message.chat.username}! Please, input the reference.")
                        self.ready_to_reference = True
                        if update.message.chat.username == "Cherrduck":
                            self.update = update
                            self.admin_detected(update)
                    else:
                        bot.sendMessage(chat_id=self.mychat_id, text="Bad password. Enter '/start' again!")
                        self.user_id = ""
                        self.user_password = ""
                        self.ready_to_reference = False
                        self.ready_to_password = False
                else:
                    if self.ready_to_reg == False:
                        bot.sendMessage(chat_id=self.mychat_id, text="Please, enter '/start'")
        else:
            self.get_format(bot, update)

    def get_format(self, bot, update):
        self.logger.info("from {}: {}".format(update.message.chat_id, update.message.text))

        try:
            video = Video(update.message.text, init_keyboard=True)
            self.find_link_in_database(update.message.text, self.user_id)
        except BadLink:
            update.message.reply_text("Bad link")
        else:
            reply_markup = InlineKeyboardMarkup(video.keyboard)
            update.message.reply_text('Choose format:', reply_markup=reply_markup)

    def download_chosen_format(self, bot, update):
        query = update.callback_query
        resolution_code, link = query.data.split(' ', 1)
        if resolution_code != "id":
            bot.edit_message_text(text="Downloading...",
                                  chat_id=query.message.chat_id,
                                  message_id=query.message.message_id)
            video = Video(link)
            video.download(resolution_code)
            with video.send() as files:
                for f in files:
                    bot.send_document(chat_id=query.message.chat_id, document=open(f, 'rb'))
        else:
            self.delete_user_from_db(link, self.update)

    def add_user_to_database(self, username, password):
        user = User(username, password)
        database.session.add(user)
        database.session.commit()
        user_id = user.id
        return user_id

    def find_user_in_database(self, username):
        user = database.session.query(User).filter(User.username == f'{username}').all()
        if user:
            user_id = user[0].id
            user_password = user[0].password
        else:
            user_id = 0
            user_password = ""
        return [user_id, user_password]

    def delete_user_from_db(self, userid, update):
        database.session.query(User).filter(User.id == f'{userid}').delete()
        database.session.commit()
        self.admin_detected(update)

    def add_link_to_database(self, name, user_id):
        link = Link(name, user_id)
        database.session.add(link)
        database.session.commit()

    def find_link_in_database(self, name, user_id):
        # link = database.session.query(Link).filter(Link.name == f'{name}', Link.user_id == f'{user_id}').all()
        # if not link:
        self.add_link_to_database(name, user_id)

    def admin_detected(self, update):
        user = User.query.all()
        if user:
            kb = []
            for us in user:
                kb.append([InlineKeyboardButton("{0}".format(us.username),
                                                callback_data="{} {}".format("id", us.id))])
            reply_markup = InlineKeyboardMarkup(kb)
            update.message.reply_text('\nAdmin panel.\nChoose user for delete:', reply_markup=reply_markup)
        return kb

    def notification_sending(self):
        self.bot.sendMessage(chat_id=self.update.message.chat_id,
                                   text="Visit us more often!\nWe will be glad to see you!")

    def scheduleOn(self):
        schedule.every().day.at("22:19").do(self.notification_sending)
        while True:
            schedule.run_pending()
            time.sleep(60)


if __name__ == '__main__':
    message_react = MessageReact(TOKEN)
    message_react.bot_load()
    thread = threading.Thread(target=message_react.scheduleOn)
    thread.start()