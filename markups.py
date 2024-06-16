from telebot import types
import db.database as db
import config_controller


def generate_yes_no():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="✅Так✅", callback_data="/yes"))
    markup.add(types.InlineKeyboardButton(text="❌Відмінити❌", callback_data="/cancel"))
    return markup

def generate_ready_exit():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="✅Готово✅", callback_data="/yes_ready"))
    markup.add(types.InlineKeyboardButton(text="❌Відмінити❌", callback_data="/cancel"))
    return markup

def generate_post_menu(offset: int=0, max:int = 5):
    if offset > len(config_controller.LIST_POSTS):
        offset = 0
    current_elem = 0
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in config_controller.LIST_POSTS:
        current_elem+=1
        if current_elem > offset and current_elem-offset <= max:
            markup.add(types.InlineKeyboardButton(text=i, callback_data=i))
        else:
            pass
    if len(config_controller.LIST_POSTS) >= max:
        markup.add(types.InlineKeyboardButton(text="-->", callback_data="/next"))
        markup.add(types.InlineKeyboardButton(text="<--", callback_data="/prev"))
    markup.add(types.InlineKeyboardButton(text="Додати", callback_data="/add"))
    markup.add(types.InlineKeyboardButton(text="❌Відмінити❌", callback_data="/cancel"))
    return markup

def generate_link_menu(offset: int=0, max:int = 5):
    list_link = db.get_all_groups()
    if offset > len(list_link):
        offset = 0
    current_elem = 0
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in list_link:
        current_elem+=1
        if current_elem > offset and current_elem-offset <= max:
            markup.add(types.InlineKeyboardButton(text=i.name, callback_data=i.name))
        else:
            pass
    if len(list_link) >= max:
        markup.add(types.InlineKeyboardButton(text="-->", callback_data="/next"))
        markup.add(types.InlineKeyboardButton(text="<--", callback_data="/prev"))
    markup.add(types.InlineKeyboardButton(text="Додати", callback_data="/add"))
    markup.add(types.InlineKeyboardButton(text="❌Відмінити❌", callback_data="/cancel"))
    return markup

def generate_links_for_user():
    list_link = db.get_all_groups()
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i in list_link:
        markup.add(types.InlineKeyboardButton(text=i.name, url=i.link))
    return markup

def generate_link_semimenu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="Видалити", callback_data="/delete"))
    markup.add(types.InlineKeyboardButton(text="❌Відмінити❌", callback_data="/cancel"))
    return markup

def generate_post_semimenu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="Видалити", callback_data="/delete"))
    markup.add(types.InlineKeyboardButton(text="Розіслати", callback_data="/send"))
    markup.add(types.InlineKeyboardButton(text="Тест (Відправити мені)", callback_data="/sendme"))
    markup.add(types.InlineKeyboardButton(text="❌Відмінити❌", callback_data="/cancel"))
    return markup


def generate_cancel():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="❌Відмінити❌", callback_data="/cancel"))
    return markup

def generate_markup_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text="Список постів", callback_data="/postlist"))
    markup.add(types.InlineKeyboardButton(text="Змінити вітальний текст", callback_data="/change_start_text"))
    markup.add(types.InlineKeyboardButton(text="Список початкових посилань", callback_data="/links"))

    markup.add(types.InlineKeyboardButton(text="Змінити пароль адміна", callback_data="/passwordadmin"))

    return markup