import logging
import os
from .release_rights import release_rights
from .db import collection_group, collection_counts, collection_user, init_counts, init_group, init_user

async def is_qualified(chat_id, user_id):
    group_info = await (await collection_group()).find_one({'chat_id': chat_id})
    if group_info:
        min_message_count = int(group_info.get('message_count'))
    else:
        min_message_count = int(os.environ['MESSAGE_COUNT'])
    if await (await collection_counts()).count_documents({
        'chat_id': chat_id,
        'user_id': user_id,
        'count': {"$gte": min_message_count}
    }, limit=1):
        return True

async def updatedb(update, context):
    user_id = update.effective_user.id
    user_name = update.effective_user.username
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    chat_id = update.effective_chat.id
    title = update.effective_chat.title

    logging.info(
        "New messsage: group {}, username {}, id {} ".format(
            chat_id, user_name, user_id))

    groups = await collection_group()
    if await groups.count_documents({'chat_id': chat_id}, limit=1) == 0:
        await init_group(chat_id, title)
        logging.info(
            "New group: title {}, id {}".format(title, chat_id))

    collection = await collection_user()
    if await collection.count_documents({'user_id': user_id}, limit=1) == 0:
        await init_user(user_id, user_name, first_name, last_name)
        logging.info(
            "First message: group {}, username {}, id {}".format(
                chat_id, user_name, user_id))

    counts = await collection_counts()
    if await counts.count_documents({'chat_id': chat_id, 'user_id': user_id}, limit=1) == 0:
        await init_counts(chat_id, user_id, 1)
    else:
        await counts.update_one(
            {'chat_id': chat_id, 'user_id': user_id}, {'$inc': {'count': 1}})
        message_count = (await counts.find_one(
            {'chat_id': chat_id, 'user_id': user_id}))['count']
        logging.info(
            'Increment message count: group {}, by {}, id {}, current message count is {}'.format(
                chat_id,
                user_name,
                user_id,
                message_count))
    if await try_release(context.bot, chat_id, user_id):
        logging.info(
            "Lock released: group {} username {}, id {}".format(
                chat_id, user_name, user_id))


async def try_release(bot, chat_id, user_id, force=False):
    logging.info("update_db_try_release")
    counts = await collection_counts()
    qualified = await is_qualified(chat_id, user_id)
    user_data = await counts.find_one({'chat_id': chat_id, 'user_id': user_id})

    if force or (qualified and not user_data['is_qualified']):
        # 假设 release_rights 本身是异步的，如果不是，你可能需要修改它或以其他方式处理
        await release_rights(bot, chat_id, user_id)
        await counts.update_one({'chat_id': chat_id, 'user_id': user_id},
                                {"$set": {'is_qualified': True}})
        return True
    return False
