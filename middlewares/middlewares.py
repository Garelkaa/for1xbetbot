
from typing import *
from aiogram import BaseMiddleware
from aiogram.types import Message
from signature import db
from keyboard.chat_kb import chat_by_kb


class CheckDb(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        
        if not db.user_exists(user_id):
            db.add_user(user_id)
            if event.chat.type == 'private':
                chat_member = await event.bot.get_chat_member(chat_id=-1002242167058, user_id=event.from_user.id)
                if chat_member.status == 'left':
                    await event.answer(
                        f"Для продолжения пользования этим ботом - подпишитесь на наш канал!", reply_markup=chat_by_kb()
                    )
                else:
                    return await handler(event, data)
            else:
                return await handler(event, data)
        else:
            if event.chat.type == 'private':
                chat_member = await event.bot.get_chat_member(chat_id=-1002242167058, user_id=event.from_user.id)
                if chat_member.status == 'left':
                    await event.answer(
                        f"Для продолжения пользования этим ботом - подпишитесь на наш канал!", reply_markup=chat_by_kb()
                    )
                else:
                    return await handler(event, data)
            else:
                return await handler(event, data)
        