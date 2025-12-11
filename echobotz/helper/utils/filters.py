from pyrogram.enums import ChatType
from pyrogram.errors import PeerIdInvalid, ChannelInvalid
from pyrogram.filters import create

from config import Config
from ... import LOGGER, user_data, auth_chats, sudo_users
from ...core.EchoClient import EchoBot


async def _chat_info(chat_id):
    chat_id = str(chat_id).strip()
    if chat_id.startswith("-100"):
        chat_id = int(chat_id)
    elif chat_id.startswith("@"):
        chat_id = chat_id.replace("@", "")
    else:
        return None
    try:
        return await EchoBot.get_chat(chat_id)
    except (PeerIdInvalid, ChannelInvalid) as e:
        LOGGER.error(f"{type(e).__name__}: {chat_id}")
        return None


async def _owner_filter(_, client, update):
    user = (getattr(update, "from_user", None)
            or getattr(update, "sender_chat", None))
    return bool(user and user.id == Config.OWNER_ID)


async def _sudo_user_filter(_, client, update):
    user = (getattr(update, "from_user", None)
            or getattr(update, "sender_chat", None))
    if not user:
        return False
    uid = user.id
    return bool(
        uid == Config.OWNER_ID
        or uid in sudo_users
        or (
            uid in user_data
            and user_data[uid].get("SUDO")
        )
    )


async def _authorized_user_filter(_, client, update):
    if Config.PUBLIC_MODE:
        return True

    user = (getattr(update, "from_user", None)
            or getattr(update, "sender_chat", None))
    if not user:
        return False
    uid = user.id

    msg = getattr(update, "message", None) or update
    chat = getattr(msg, "chat", None)
    if not chat:
        return False

    chat_id = chat.id
    thread_id = (
        msg.message_thread_id
        if getattr(msg, "is_topic_message", False)
        else None
    )

    if uid == Config.OWNER_ID:
        return True
    if uid in sudo_users:
        return True
    if uid in user_data and (
        user_data[uid].get("AUTH", False)
        or user_data[uid].get("SUDO", False)
    ):
        return True
    if chat_id in user_data and user_data[chat_id].get("AUTH", False):
        thread_ids = user_data[chat_id].get("thread_ids", [])
        if thread_id is None or thread_id in thread_ids:
            return True
    if chat_id in auth_chats:
        return True
    if uid in auth_chats:
        return True
    return False


class CustomFilters:
    owner = create(_owner_filter)
    sudo = create(_sudo_user_filter)
    authorized = create(_authorized_user_filter)
