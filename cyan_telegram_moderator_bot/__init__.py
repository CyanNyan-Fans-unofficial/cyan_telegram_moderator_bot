from telegram import Update
from telegram.constants import (
    ChatMemberStatus,
    )
from telegram.ext import (
    ContextTypes,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    InlineQueryHandler,
)
import logging
from random import randint
from .update_db import try_release,updatedb
from .db import collection_group
from .ban_rights import banrights

# 设定 cyan 群组变量
# 加载变量
import env
TOKEN=env.TELEGRAM_TOKEN
MESSAGE_COUNT = env.CYANBOT_MESSAGE_COUNT

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("echo detected")
    group_collection = await collection_group()
    group_info = await group_collection.find_one({'chat_id': update.effective_chat.id})
    if group_info:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=group_info['echo'])

async def meow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("meow detected")
    group_collection = await collection_group()
    group_info = await group_collection.find_one({'chat_id': update.effective_chat.id})
    if group_info:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=group_info['meow'])

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("roll detected")
    limit = 100
    if context.args:
        try:
            limit = int(context.args[0])
        except ValueError:
            logging.info('User gave an invalid number')
    if limit >= 1:
        result = randint(1, limit)
        await update.effective_chat.send_message(text=str(result))

async def release(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info("Manually release rights")
    if not (update.message and update.message.reply_to_message):
        return
    target = update.message.reply_to_message.from_user
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    target_id = target.id
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    if chat_member.status not in {ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR}:
        logging.info('no permission to release rights!')
        return
    if await try_release(context.bot, chat_id, target_id, force=True):
        await update.effective_chat.send_message('Manually released rights!')


set_types = {
    'welcome': 'welcome_message',
    'echo': 'echo',
    'meow': 'meow',
    'message_count': 'message_count'
}

async def set_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info('set message detected!')
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    if chat_member.status not in {ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR}:
        logging.info('no permission to set message!')
        return
    # 使用 await 等待 collection_group() 完成，获取集合对象
    group_collection = await collection_group()

    group_info = await group_collection.find_one({'chat_id': chat_id})
    if group_info and len(context.args) >= 2:
        set_type = context.args[0]
        set_content = ' '.join(context.args[1:])
        if set_type in set_types:
            # 使用 await 等待 collection_group() 完成，获取集合对象
            group_collection = await collection_group()
            await group_collection.update_one({'chat_id': chat_id}, {'$set': {set_types[set_type]: set_content}})
            await context.bot.send_message(
                chat_id=chat_id,
                text=f'Message updated for {set_type}.')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logging.info("echo")
logging.info("meow")

def main():
    # 创建 bot 应用实例
    application = (
        ApplicationBuilder().token(env.TELEGRAM_TOKEN).concurrent_updates(True).build()
    )
    application.add_handler(MessageHandler(filters.TEXT & filters.REPLY, release), group=3)
    # 测试代码
    application.add_handler(CommandHandler('echo', echo, filters=filters.ChatType.SUPERGROUP))
    application.add_handler(CommandHandler('meow', meow, filters=filters.ChatType.SUPERGROUP))
    application.add_handler(CommandHandler('set', set_message, filters=filters.ChatType.SUPERGROUP))
    application.add_handler(MessageHandler(filters.ChatType.SUPERGROUP & filters.StatusUpdate.NEW_CHAT_MEMBERS, banrights),group=4)
    application.add_handler(MessageHandler(filters.ChatType.SUPERGROUP & filters.TEXT, updatedb), group=5)
    application.run_polling()

if __name__ == "__main__":
    main()