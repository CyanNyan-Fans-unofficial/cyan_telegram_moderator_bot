from telegram import Update
from telegram.constants import (
    ChatMemberStatus,
    )
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from . import (
    release,
    echo,
    meow,
    set_message,
)
from .update_db import updatedb
from .ban_rights import banrights

# 设定 cyan 群组变量
# 加载变量
from dotenv import load_dotenv
import os
load_dotenv() 

TOKEN= os.getenv("TELEGRAM_TOKEN")
MESSAGE_COUNT= os.getenv("CYANBOT_MESSAGE_COUNT","60")

def main():
    # 创建 bot 应用实例
    application = (
        ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()
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