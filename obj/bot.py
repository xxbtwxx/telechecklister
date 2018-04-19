from obj.dal import Dal
from static import cfg
from obj.listController import ListController
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, User, ParseMode, Chat, ChatMember
import telegram.error
import telegram.utils.helpers
import logging

class Bot:
    token = cfg.key

    updater = ''
    dispatcher = ''
    is_running = False

    def __init__(self):
        self.updater = Updater(token = self.token)
        self.dispatcher = self.updater.dispatcher

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

        self.dispatcher.workers = 4
        self.add_handlers()

    def start(self):
        self.updater.start_polling(timeout=9999, read_latency=10)
        self.is_running = True

    def stop(self):
        self.updater.stop()
        self.is_running = False

    def bot_running(self):
        return self.is_running

    def add_handlers(self):
        function_to_handler = {
            self.command_show_all_lists: 'all_lists',
            self.command_create_list: 'create_list',
            self.command_delete_list: 'delete_list',
            self.command_show_list: 'list',
            self.command_add_to_list: 'add_item',
            self.command_delete_from_list: 'delete_item',
            self.command_check_item: 'check_item',
            self.command_uncheck_item: 'uncheck_item',
            self.command_help: 'help'
        }

        for function, handler in function_to_handler.items():
            self.dispatcher.add_handler(CommandHandler(handler, function))


    def command_show_all_lists(self, bot, update):

        chat_id = update.message.chat.id
        list_controller = ListController(chat_id)

        all_lists = list_controller.get_list_names()
        if len(all_lists) == 0:
            update.message.reply_text('There are no active lists')
            return False


        out = '\n'.join(list(map(lambda x: x[0] + '\n' 
                                                + list_controller.list_completeness(x[0]) 
                                                + ' checked items\n------------', 
                                                all_lists)))
        update.message.reply_text('Active lists:\n------------\n'+out)
        return True

    def format_brackets_input(self, input_text):
        input_text = input_text.replace('”', '"')
        input_text = input_text.replace('“', '"')
        return input_text

    def command_create_list(self, bot, update):

        input_text = self.format_brackets_input(update.message.text)
        input_text = input_text.split('"')

        if len(input_text) != 3:
            cmd = '''Please specify list name\nCommand usage /create_list "list name"'''
            update.message.reply_text(cmd)
            return False

        list_name = input_text[1]
        chat_id = update.message.chat.id

        list_controller = ListController(chat_id)

        if list_name != '':
            status = list_controller.create_list(list_name)
        else:
            update.message.reply_text('Sorry, the list name can\'t be blank')
            return False

        if status == False:
            update.message.reply_text('List already exist')
            return False

        update.message.reply_text('List created')
        return True

    def command_delete_list(self, bot, update):

        input_text = self.format_brackets_input(update.message.text)
        input_text = input_text.split('"')

        if len(input_text) != 3:
            update.message.reply_text('''Please specify list name\nCommand usage /delete_list "list name"''')
            return False

        list_name = input_text[1]

        chat_id = update.message.chat.id

        list_controller = ListController(chat_id)
        if list_name != '':
            status = list_controller.delete_list(list_name)
        else:
            update.message.reply_text('Sorry, the list name can\'t be blank')
            return False

        if status == False:
            update.message.reply_text('No such list exist')
            return False

        update.message.reply_text('List deleted')
        return True

    def command_show_list(self, bot, update):
        input_text = self.format_brackets_input(update.message.text)
        input_text = input_text.split('"')

        if len(input_text) != 3:
            update.message.reply_text('''Please specify list name\nCommand usage /show_list "list name"''')
            return False

        list_name = input_text[1]  
        chat_id = update.message.chat.id

        list_controller = ListController(chat_id)

        if list_name != '':
            status = list_controller.list_exist(list_name)
        else:
            update.message.reply_text('Sorry, the list name can\'t be blank')
            return False

        if status == False:
            update.message.reply_text('No such list exist')
            return False

        items = list_controller.get_list_items(list_name)

        if len(items) == 0:
            update.message.reply_text('List is empty')
            return True

        checked = ['❌', '✅']
        out = '\n'.join(list(map(lambda x: x[0] + ' ' + checked[int(x[1])] + '\n------------', items)))
        update.message.reply_text('List ' + list_name 
                                  + '\n' + '------------' + '\n' + out)

        return True

    def command_add_to_list(self, bot, update):
        input_text = self.format_brackets_input(update.message.text)
        input_text = input_text.split('"')

        if len(input_text) != 5:
            update.message.reply_text('''Please specify list name\nCommand usage /add_item "list name" "item_name"''')
            return False

        list_name = input_text[1]  
        item_name = input_text[3]
        chat_id = update.message.chat.id

        list_controller = ListController(chat_id)

        if list_name != '':
            status = list_controller.list_exist(list_name)
        else:
            update.message.reply_text('Sorry, the list name can\'t be blank')
            return False

        if status == False:
            update.message.reply_text('No such list exist')
            return False

        if item_name != '':
            status = list_controller.item_in_list(list_name, item_name)
        else:
            update.message.reply_text('Sorry, the item name can\'t be blank')
            return False

        if status == True:
            update.message.reply_text('Sorry, this item is already in the list')
            return False

        list_controller.add_to_list(list_name, item_name)

        update.message.reply_text('Added to list')

    def command_delete_from_list(self, bot, update):
        input_text = self.format_brackets_input(update.message.text)
        input_text = input_text.split('"')

        if len(input_text) != 5:
            update.message.reply_text('''Please specify list name\nCommand usage /delete_item "list name" "item_name"''')
            return False

        list_name = input_text[1]  
        item_name = input_text[3]
        chat_id = update.message.chat.id

        list_controller = ListController(chat_id)

        if list_name != '':
            status = list_controller.list_exist(list_name)
        else:
            update.message.reply_text('Sorry, the list name can\'t be blank')
            return False

        if status == False:
            update.message.reply_text('No such list exist')
            return False

        if item_name != '':
            status = list_controller.item_in_list(list_name, item_name)
        else:
            update.message.reply_text('Sorry, the item name can\'t be blank')
            return False

        if status == False:
            update.message.reply_text('Sorry, this item is not in the list')
            return False

        list_controller.delete_from_list(list_name, item_name)

        update.message.reply_text('Deleted from list')

    def command_check_item(self, bot, update):
        input_text = self.format_brackets_input(update.message.text)
        input_text = input_text.split('"')

        if len(input_text) != 5:
            update.message.reply_text('''Please specify list name\nCommand usage /check_item "list name" "item_name"''')
            return False

        list_name = input_text[1]  
        item_name = input_text[3]
        chat_id = update.message.chat.id

        list_controller = ListController(chat_id)

        if list_name != '':
            status = list_controller.list_exist(list_name)
        else:
            update.message.reply_text('Sorry, the list name can\'t be blank')
            return False

        if status == False:
            update.message.reply_text('No such list exist')
            return False

        if item_name != '':
            status = list_controller.item_in_list(list_name, item_name)
        else:
            update.message.reply_text('Sorry, the item name can\'t be blank')
            return False

        if status == False:
            update.message.reply_text('Sorry, this item is not in the list')
            return False

        list_controller.check_item(list_name, item_name)
        update.message.reply_text('Item checked')
        return True

    def command_uncheck_item(self, bot, update):
        input_text = self.format_brackets_input(update.message.text)
        input_text = input_text.split('"')

        if len(input_text) != 5:
            update.message.reply_text('''Please specify list name\nCommand usage /check_item "list name" "item_name"''')
            return False

        list_name = input_text[1]  
        item_name = input_text[3]
        chat_id = update.message.chat.id

        list_controller = ListController(chat_id)

        if list_name != '':
            status = list_controller.list_exist(list_name)
        else:
            update.message.reply_text('Sorry, the list name can\'t be blank')
            return False

        if status == False:
            update.message.reply_text('No such list exist')
            return False

        if item_name != '':
            status = list_controller.item_in_list(list_name, item_name)
        else:
            update.message.reply_text('Sorry, the item name can\'t be blank')
            return False

        if status == False:
            update.message.reply_text('Sorry, this item is not in the list')
            return False

        list_controller.uncheck_item(list_name, item_name)
        update.message.reply_text('Item unchecked')
        return True

    def command_help(self, bot, update):
        update.message.reply_text('Possible commands: /all_lists, /create_list, /delete_list, /list, /add_item, /delete_item, /check_item, /uncheck_item')