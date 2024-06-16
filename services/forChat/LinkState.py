import markups
from services.forChat.UserState import UserState
from services.forChat.Response import Response
import config_controller
import db.database as db

class LinkState(UserState):
    async def start_msg(self):
        self.current_page = 0
        self.max_on_page = 20
        self.state = "links"
        self.current_group = None
        return Response(text="Список посилань: ", buttons=markups.generate_link_menu(self.current_page, self.max_on_page))

    async def next_msg(self, message: str):
        if self.state == "add_name":
            self.name = message
            self.state = "add_link"
            return Response(text="Введіть наступним повідомленням саме посилання:",
                            buttons=markups.generate_cancel())
        elif self.state == "add_link":
            self.link = message
            self.state = None
            db.create_group(self.name, self.link)
            return Response(text="Додано!", redirect="/links")

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            if self.current_group != None:
                return Response(redirect="/links")
            return Response(redirect="/menu")
        elif data_btn == "/add":
            self.state = "add_name"
            return Response(text="Введіть наступним повідомленням назву для посилання:", buttons=markups.generate_cancel())
        elif self.state == "links":
            group = db.get_group_by_name(data_btn)[0]
            self.current_group = group
            return Response(text="Назва посилання: "+group.name+"\nПосилання: " +group.link, buttons=markups.generate_link_semimenu())
        elif data_btn == "/delete":
            db.delete_group_by_name(self.current_group.name)
            return Response(text="Видалено!", redirect="/links")
