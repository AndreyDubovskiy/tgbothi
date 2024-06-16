import datetime

from sqlalchemy import create_engine
from db.models.BaseModel import BaseModel
from db.models.UserModel import UserModel
from db.models.GroupModel import GroupModel


from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy import select
from typing import List

engine = create_engine("sqlite:///mainbase.db", echo=False)

BaseModel.metadata.create_all(engine)


def get_all_groups():
    with Session(engine) as session:
        query = select(GroupModel)
        res: List[GroupModel] = session.scalars(query).all()
    return res

def get_group_by_name(name:str):
    with Session(engine) as session:
        query = select(GroupModel).where(GroupModel.name == name)
        res: List[GroupModel] = session.scalars(query).all()
    return res

def get_group_by_chat_id(chat_id:str):
    with Session(engine) as session:
        query = select(GroupModel).where(GroupModel.chat_id == chat_id)
        res: List[GroupModel] = session.scalars(query).all()
    return res

def get_group_by_link(link:str):
    with Session(engine) as session:
        query = select(GroupModel).where(GroupModel.link == link)
        res: List[GroupModel] = session.scalars(query).all()
    return res

def is_in_groups_by_name(name:str):
    tmp = get_group_by_name(name)
    return len(tmp) != 0

def create_group(name:str, link:str):

    if is_in_groups_by_name(name):
        return

    with Session(engine) as session:
        group = GroupModel(name, link)
        session.add(group)
        session.commit()
    return

def delete_group_by_name(name: str):
    if not is_in_groups_by_name(name):
        return False
    with Session(engine) as session:
        query = select(GroupModel).where(GroupModel.name == name)
        group: GroupModel = session.scalars(query).first()
        session.delete(group)
        session.commit()
    return True




def get_all_users():
    with Session(engine) as session:
        query = select(UserModel)
        res: List[UserModel] = session.scalars(query).all()
    return res


def session_commit(obj):
    with Session(engine) as session:
        session.add(obj)
        session.commit()
    return

def get_user_by_tg_name(tg_name:str):
    with Session(engine) as session:
        query = select(UserModel).where(UserModel.tg_name == tg_name)
        res: List[UserModel] = session.scalars(query).all()
    return res

def get_user_by_chat_id(chat_id:str):
    with Session(engine) as session:
        query = select(UserModel).where(UserModel.chat_id == chat_id)
        res: List[UserModel] = session.scalars(query).all()
    return res

def is_in_users_by_chat_id(chat_id:str):
    tmp = get_user_by_chat_id(chat_id)
    return len(tmp) != 0

def create_user(tg_name:str, chat_id:str):

    if is_in_users_by_chat_id(chat_id):
        return

    with Session(engine) as session:
        user = UserModel(tg_name, chat_id)
        session.add(user)
        session.commit()
    return

def delete_user_by_chat_id(chat_id: str):
    if not is_in_users_by_chat_id(chat_id):
        return False
    with Session(engine) as session:
        query = select(UserModel).where(UserModel.chat_id == chat_id)
        user: UserModel = session.scalars(query).first()
        session.delete(user)
        session.commit()
    return True