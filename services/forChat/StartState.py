import markups
from services.forChat.UserState import UserState
from services.forChat.Response import Response
import config_controller
import db.database as db

class StartState(UserState):
    async def start_msg(self):
        if not db.is_in_users_by_chat_id(self.user_id):
            db.create_user(self.user_name, self.user_id)
        return Response(text=config_controller.START_TEXT, buttons=markups.generate_links_for_user(), is_end=True)