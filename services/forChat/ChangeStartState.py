import markups
from services.forChat.UserState import UserState
from services.forChat.Response import Response
import config_controller

class ChangeStartState(UserState):
    async def start_msg(self):
        return Response(text="Введіть наступним повідомленням початковий текст: ", buttons=markups.generate_cancel())

    async def next_msg(self, message: str):
        config_controller.change_start_text(message)
        return Response(text="Текст змінено!", redirect="/menu")

    async def next_btn_clk(self, data_btn: str):
        if data_btn == "/cancel":
            return Response(redirect="/menu")