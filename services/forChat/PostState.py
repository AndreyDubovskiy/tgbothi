import datetime

from services.forChat.UserState import UserState
from services.forChat.Response import Response
from telebot.async_telebot import AsyncTeleBot
from telebot import types
import markups
import config_controller
import db.database as db

class PostState(UserState):
    def __init__(self, user_id: str, user_chat_id: str, bot: AsyncTeleBot, user_name: str):
        super().__init__(user_id, user_chat_id, bot, user_name)
        self.current_page = 0
        self.max_on_page = 5
        self.edit = None
        self.current_name = None
        self.newname = None
        self.newurls = None
        self.newphotos = None
        self.newvideos = None
        self.newtext = None
    async def start_msg(self):
        if self.user_id in config_controller.list_is_loggin_admins:
            return Response(text="Список постів", buttons=markups.generate_post_menu(self.current_page, self.max_on_page))
        else:
            return Response(text="У вас недостатньо прав!", is_end=True)

    async def next_msg(self, message: str):
        if not (self.user_id in config_controller.list_is_loggin_admins):
            return Response(text="У вас недостатньо прав!", is_end=True)
        if self.edit == "addname":
            self.newname = message
            self.edit = "addpost"
            return Response(text="Відправте пост одним повідомленням (можна з фото або відео, та текстом, але одним повідомленням):")
        elif self.edit == "addpost":
            self.newtext = message
            self.edit = "addurls"
            return Response(
                text="Напишіть посилання, які потрібно додати до поста (якщо не одне посилання, то кожне посилання з нового рядка. Але одним повідомленням):", buttons=markups.generate_cancel())
        elif self.edit == "addurls":
            self.newurls = message.split("\n")
            self.edit = None
            if config_controller.add_or_edit_post(self.newname, text=self.newtext, urls=self.newurls, photos=self.newphotos, videos=self.newvideos):
                return Response(text="Успішно додано!", is_end=True, redirect="/postlist")
            else:
                return Response(text="Помилка!", is_end=True, redirect="/postlist")

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            if self.current_name == None:
                return Response(is_end=True, redirect="/menu")
            else:
                return Response(is_end=True, redirect="/postlist")
        elif data_btn == "/next":
            if len(config_controller.LIST_POSTS)-((self.current_page+1)*self.max_on_page) > 0:
                self.current_page+=1
            return Response(text="Список постів", buttons=markups.generate_post_menu(self.current_page*self.max_on_page, self.max_on_page))
        elif data_btn =="/prev":
            if self.current_page > 0:
                self.current_page-=1
            return Response(text="Список постів", buttons=markups.generate_post_menu(self.current_page*self.max_on_page, self.max_on_page))
        elif data_btn in config_controller.LIST_POSTS:
            self.current_name = data_btn
            print(config_controller.LIST_POSTS[self.current_name])
            text = ""
            if config_controller.LIST_POSTS[self.current_name]['photos'] != None:
                text+= "\nКількість прикріплених фото: " + str(len(config_controller.LIST_POSTS[self.current_name]['photos'])) + "\n"
            if config_controller.LIST_POSTS[self.current_name]['videos'] != None:
                text+= "\nКількість прикріплених відео: " + str(len(config_controller.LIST_POSTS[self.current_name]['videos'])) + "\n"
            if config_controller.LIST_POSTS[self.current_name]['text'] != None:
                text+="\nТекст поста:\n" + config_controller.LIST_POSTS[self.current_name]['text']
            return Response(text="Назва поста: " + self.current_name + text, buttons=markups.generate_post_semimenu())
        elif data_btn == "/add":
            self.edit = "addname"
            return Response(text="Напишіть назву поста наступним повідомленням (для себе, користувачам не надсилається):", buttons=markups.generate_cancel())
        elif data_btn == "/delete":
            if config_controller.del_post(self.current_name):
                return Response(text="Успішно видалено!", is_end=True, redirect="/postlist")
            else:
                return Response(text="Помилка!", is_end=True, redirect="/postlist")
        elif data_btn == "/sendme":
            try:
                chat_id = self.user_chat_id
                text_post = config_controller.LIST_POSTS[self.current_name]['text']
                list_photos = config_controller.LIST_POSTS[self.current_name]['photos']
                list_videos = config_controller.LIST_POSTS[self.current_name]['videos']
                list_urls = config_controller.LIST_POSTS[self.current_name]['urls']
                markup_tpm = types.InlineKeyboardMarkup(row_width=2)
                for i in list_urls:
                    markup_tpm.add(types.InlineKeyboardButton(text="Перейти за посиланням", url=i))
                if list_photos and len(list_photos) == 1 and text_post:
                    with open(list_photos[0], 'rb') as photo_file:
                        await self.bot.send_photo(chat_id=chat_id, photo=photo_file, caption=text_post,
                                                  reply_markup=markup_tpm)
                elif list_photos and len(list_photos) == 1:
                    with open(list_photos[0], 'rb') as photo_file:
                        await self.bot.send_photo(chat_id=chat_id, photo=photo_file, reply_markup=markup_tpm)
                elif list_photos and len(list_photos) > 1 and text_post:
                    media = []
                    for i in list_photos:
                        with open(i, 'rb') as photo_file:
                            media.append(types.InputMediaPhoto(media=photo_file))
                    await self.bot.send_media_group(chat_id=chat_id, media=media)
                    await self.bot.send_message(chat_id=chat_id, text=text_post, reply_markup=markup_tpm)
                elif list_videos and len(list_videos) == 1 and text_post:
                    with open(list_videos[0], 'rb') as video_file:
                        await self.bot.send_video(chat_id=chat_id, video=video_file, caption=text_post,
                                                  reply_markup=markup_tpm)
                elif list_videos and len(list_videos) == 1:
                    with open(list_videos[0], 'rb') as video_file:
                        await self.bot.send_video(chat_id=chat_id, video=video_file, reply_markup=markup_tpm)
                elif text_post:
                    await self.bot.send_message(chat_id=chat_id, text=text_post, reply_markup=markup_tpm)
            except Exception as ex:
                return Response(text="Щось пішло не так!", redirect="/menu")
            return Response(redirect="/postlist")
        elif data_btn == "/send":
            list_users = db.get_all_users()
            count = 0
            error = 0
            await self.bot.send_message(chat_id=self.user_id, text="Розсилка розпочата, очікуйте повідомлення про закінчення")
            for user in list_users:
                try:
                    chat_id = user.chat_id
                    text_post = config_controller.LIST_POSTS[self.current_name]['text']
                    list_photos = config_controller.LIST_POSTS[self.current_name]['photos']
                    list_videos = config_controller.LIST_POSTS[self.current_name]['videos']
                    list_urls = config_controller.LIST_POSTS[self.current_name]['urls']
                    markup_tpm = types.InlineKeyboardMarkup(row_width=2)
                    for i in list_urls:
                        markup_tpm.add(types.InlineKeyboardButton(text="Перейти за посиланням", url=i))
                    if list_photos and len(list_photos) == 1 and text_post:
                        with open(list_photos[0], 'rb') as photo_file:
                            await self.bot.send_photo(chat_id=chat_id, photo=photo_file, caption=text_post, reply_markup=markup_tpm)
                    elif list_photos and len(list_photos) == 1:
                        with open(list_photos[0], 'rb') as photo_file:
                            await self.bot.send_photo(chat_id=chat_id, photo=photo_file, reply_markup=markup_tpm)
                    elif list_photos and len(list_photos) > 1 and text_post:
                        media = []
                        for i in list_photos:
                            with open(i, 'rb') as photo_file:
                                media.append(types.InputMediaPhoto(media=photo_file))
                        await self.bot.send_media_group(chat_id=chat_id, media=media)
                        await self.bot.send_message(chat_id=chat_id, text=text_post, reply_markup=markup_tpm)
                    elif list_videos and len(list_videos) == 1 and text_post:
                        with open(list_videos[0], 'rb') as video_file:
                            await self.bot.send_video(chat_id=chat_id, video=video_file, caption=text_post, reply_markup=markup_tpm)
                    elif list_videos and len(list_videos) == 1:
                        with open(list_videos[0], 'rb') as video_file:
                            await self.bot.send_video(chat_id=chat_id, video=video_file, reply_markup=markup_tpm)
                    elif text_post:
                        await self.bot.send_message(chat_id=chat_id, text=text_post, reply_markup=markup_tpm)
                    count+=1
                except Exception as ex:
                    error+=1
            return Response(text="Розсилка закінчена!\nРозіслано людям: "+str(count)+"\nПомилок: "+str(error), is_end=True, redirect="/postlist")






    async def next_msg_photo_and_video(self, message: types.Message):
        if self.edit == "addpost":
            self.newtext = message.caption
            if message.photo:
                self.newphotos = []
                i = message.photo[-1]
                file_info = await self.bot.get_file(i.file_id)
                file_path = file_info.file_path
                bytess = await self.bot.download_file(file_path)
                with open(f'post_tmp/{str(config_controller.get_id_post())}_{i.file_id}.jpg', 'wb') as file:
                    file.write(bytess)
                self.newphotos.append(f'post_tmp/{str(config_controller.get_id_post())}_{i.file_id}.jpg')
            if message.video:
                self.newvideos = []
                i = message.video
                file_info = await self.bot.get_file(i.file_id)
                file_path = file_info.file_path
                bytess = await self.bot.download_file(file_path)
                with open(f'post_tmp/{str(config_controller.get_id_post())}_{i.file_id}.mp4', 'wb') as file:
                    file.write(bytess)
                self.newvideos.append(f'post_tmp/{str(config_controller.get_id_post())}_{i.file_id}.mp4')
            self.edit = "addurls"
            return Response(text="Напишіть посилання, які потрібно додати до поста (якщо не одне посилання, то кожне посилання з нового рядка. Але одним повідомленням):", buttons=markups.generate_cancel())