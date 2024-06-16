from db.models.BaseModel import BaseModel
from db.models.imports import *

class UserModel(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_name: Mapped[str] = mapped_column(String(255))
    chat_id: Mapped[str] = mapped_column(String(255))


    def __init__(self, tg_name: str, chat_id: str):
        self.tg_name = tg_name
        self.chat_id = chat_id
