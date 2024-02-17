from motor.motor_asyncio import AsyncIOMotorClient
from os import environ

import env
# 加载变量
DATABASE_URL=env.CYANBOT_DATABASE_URL
DATABASE_NAME = env.CYANBOT_DATABASE_NAME

async def connect_mongo():
    client = AsyncIOMotorClient(DATABASE_URL)
    db = client[DATABASE_NAME]
    return db

async def collection_user():
    db = await connect_mongo()
    return db['collection']

async def collection_counts():
    db = await connect_mongo()
    return db['message_counts']

async def collection_group():
    db = await connect_mongo()
    return db['groups']

async def init_user(userid, username, first_name, last_name):
    post = {
        'user_id': userid,
        'user_name': username,
        'first_name': first_name,
        'last_name': last_name,
        'count': 0,
        'is_qualified': False
    }
    await (await collection_user()).insert_one(post)

async def init_counts(chat_id, user_id, init_count=0, is_qualified=False):
    count = {
        'chat_id': chat_id,
        'user_id': user_id,
        'is_qualified': is_qualified,
        'count': init_count
    }
    await (await collection_counts()).insert_one(count)

async def init_group(chat_id, title=None):
    group = {
        'chat_id': chat_id,
        'title': title,
        'message_count': '60',
        'welcome_message': 'Hello, {first_name}. Welcome to the group! Please stay active so you can send sticker and media later XD',
        'echo': 'Cyan is cute!',
        'meow': '喵喵喵？'
    }
    await (await collection_group()).insert_one(group)
    