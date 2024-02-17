import logging
from .update_db import is_qualified  # 确保is_qualified也支持异步，如果需要的话
from .db import collection_group
from .permissions import RESTRICTED_PERMISSIONS, RELEASED_PERMISSIONS

# 将函数定义为异步
async def ban_rights(update, context):
    """Ban all rights except send text when first enter group"""
    # 确保collection_group().find_one也被修改为支持异步
    group_collection = await collection_group()
    group_info = await group_collection.find_one({'chat_id': update.effective_chat.id})

    for new_member in update.message.new_chat_members:
        # 使用await等待is_qualified，如果它是异步的
        if await is_qualified(update.effective_chat.id, new_member.id):
            logging.info('{} is already qualified!'.format(new_member.first_name))
            # 确保restrict_chat_member是异步的或者找到适当的异步替代方法
            await context.bot.restrict_chat_member(
                update.message.chat_id, new_member.id, RELEASED_PERMISSIONS)
        else:
            logging.info('{} is restricted!'.format(new_member.first_name))
            # 同上，确保使用异步方法
            await context.bot.restrict_chat_member(
                update.message.chat_id, new_member.id, RESTRICTED_PERMISSIONS)

        if group_info:
            welcome_text = group_info['welcome_message']
            # 如果reply_text不支持异步，考虑使用异步的等价方法
            await update.message.reply_text(welcome_text.format(
                first_name=new_member.first_name,
                last_name=new_member.last_name
            ))
