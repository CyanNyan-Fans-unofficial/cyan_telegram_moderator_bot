from telegram import ChatPermissions

RESTRICTED_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    # 在新版本机器人中，该权限已经失效
    # can_send_media_messages=False,
    can_send_audios=False,
    can_send_documents=False,
    can_send_videos=False,
    can_send_video_notes=False,
    can_send_polls=False,
    can_send_other_messages=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False,
    can_pin_messages=False)

RELEASED_PERMISSIONS = ChatPermissions(
    can_send_messages=True,
    # 在新版本机器人中，该权限已经失效
    # can_send_media_messages=True,
    can_send_audios=True,
    can_send_documents=True,
    can_send_videos=True,
    can_send_video_notes=True,
    can_send_polls=True,
    can_send_other_messages=True,
    can_add_web_page_previews=True,
    can_change_info=False,
    can_invite_users=True,
    can_pin_messages=False)
