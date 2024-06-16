import os
import pickle

PASSWORD_ADMIN = "admin"

START_TEXT = "Привіт! Тут повинен буди привітальний текст, але його не задали 😢"


LIST_POSTS = {}
# {"name":{"text": str,
#          "urls": [str],
#          "photos": [str],
#           "videos": [str]
#          }}


list_is_loggin_admins = []

def preload_config():
    if os.path.exists("config.bin"):
        read_ini()
    else:
        write_ini()
def write_ini():
    config = {}
    config["PASSWORD_ADMIN"] = PASSWORD_ADMIN
    config["LIST_POSTS"] = LIST_POSTS
    config["START_TEXT"] = START_TEXT
    with open('config.bin', 'wb') as configfile:
        pickle.dump(config, configfile)


def change_start_text(text:str):
    global START_TEXT
    START_TEXT = text
    write_ini()


def read_ini():
    global PASSWORD_ADMIN, LIST_POSTS, START_TEXT
    with open('config.bin', 'rb') as configfile:
        config = pickle.load(configfile)
        PASSWORD_ADMIN = str(config["PASSWORD_ADMIN"])
        LIST_POSTS = config.get("LIST_POSTS", LIST_POSTS)
        START_TEXT = config.get("START_TEXT", START_TEXT)


def del_post(key):
    global LIST_POSTS
    if LIST_POSTS.get(key, None) != None:
        if LIST_POSTS[key]['photos'] != None:
            for i in LIST_POSTS[key]['photos']:
                try:
                    os.remove(i)
                except Exception as ex:
                    pass
        if LIST_POSTS[key]['videos'] != None:
            for i in LIST_POSTS[key]['videos']:
                try:
                    os.remove(i)
                except Exception as ex:
                    pass
        LIST_POSTS.__delitem__(key)
        write_ini()
        return True
    else:
        return False

def is_id_post(id:int):
    for i in LIST_POSTS:
        if LIST_POSTS[i]['id'] == id:
            return False
    return True

def get_id_post():
    id = 0
    while(not is_id_post(id)):
        id+=1
    return id


def add_or_edit_post(key: str, text: str = None, urls: list = None, photos: list = None, videos: list = None):
    global LIST_POSTS
    try:
        v_key = key
        v_text = text
        v_urls = urls
        v_photos = photos
        v_videos = videos
        id = get_id_post()
        LIST_POSTS[v_key] = {'text': v_text,
                                 'urls': v_urls,
                             'photos': v_photos,
                             'videos': v_videos,
                             'id': id}
        write_ini()
        return True
    except Exception as ex:
        print(ex)
        return False

def log(chat_id, password):
    global list_is_loggin_admins
    if password == PASSWORD_ADMIN and (not chat_id in list_is_loggin_admins):
        list_is_loggin_admins.append(chat_id)
        return True
    elif chat_id in list_is_loggin_admins:
        return True
    return False

def change_password_admin(chat_id, password):
    global PASSWORD_ADMIN, list_is_loggin_admins
    if chat_id in list_is_loggin_admins:
        PASSWORD_ADMIN = password
        write_ini()
        list_is_loggin_admins = []
        return True
    else:
        return False