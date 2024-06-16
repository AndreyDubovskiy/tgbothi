from db.models.BaseModel import BaseModel
from db.models.imports import *

class GroupModel(BaseModel):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    chat_id: Mapped[str] = mapped_column(String(255))
    link: Mapped[str] = mapped_column(String(255))


    def __init__(self, name: str, link: str):
        self.name = name
        self.chat_id = "None"
        self.link = link
