import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv

from openai import OpenAI
import os

# Bot token can be obtained via https://t.me/BotFather
TOKEN ="6695135667:AAF93rJDAp7Hdoig_gIQnYJK5sREx5jcMlU"

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()
load_dotenv()



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    await message.answer(f"سلام, {hbold(message.from_user.full_name)} خوش اومدی به ربات \n هر سوالی داشتی میتونی ازم بپرسی!")


client = OpenAI(
 api_key=os.environ.get("OPENAI_API_KEY"),
)

def callGPT(message):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": message.text,
        }
    ],
    model="gpt-3.5-turbo",
    )
    # print(chat_completion)
    return (chat_completion.choices[0].message.content)

    # return "salam"

@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """

    await message.answer(callGPT(message))

async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())