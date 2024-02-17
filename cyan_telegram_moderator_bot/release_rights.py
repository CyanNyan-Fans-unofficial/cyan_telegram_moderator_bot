import logging
from telegram import ChatPermissions
from .permissions import RELEASED_PERMISSIONS
from telegram.constants import (
    ChatMemberStatus,
    )

async def release_rights(bot, chat_id, user_id):
    """When the user is qualified(see is_qualified), enable other user permissions

    The enabled permissions include:
     'Send Media',
     'Send Stickers & GIFs',
     'Send Polls',
     'Embed Links',
     'Add Users'

    """
    logging.info("Releasing rights")
    # 异步获取chat_member信息
    chat_member = await bot.get_chat_member(chat_id, user_id)
    if chat_member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
        logging.info('Skip creator or administrator!')
        return

    # 创建一个ChatPermissions对象，其中包含你想要授予的权限
    permissions = ChatPermissions(
                                    can_send_messages=True, 
                                    can_send_audios=True,
                                    can_send_documents=True,
                                    can_send_videos=True,
                                    can_send_video_notes=True,
                                    can_send_polls=True, 
                                    can_send_other_messages=True, 
                                    can_add_web_page_previews=True,
                                    can_invite_users=True)

    # 使用这个permissions对象调用restrict_chat_member
    await bot.restrict_chat_member(chat_id, user_id, permissions=permissions)
    logging.info("Rights should be released")