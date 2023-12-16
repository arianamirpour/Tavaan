import os
from openai import OpenAI
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv


bot = Bot(token='6695135667:AAF93rJDAp7Hdoig_gIQnYJK5sREx5jcMlU')
dp = Dispatcher()

load_dotenv()

client = OpenAI(
 api_key=os.environ.get("OPENAI_API_KEY"),
)


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: types.Message):
    await message.reply('سلام. خیلی خوش اومدی به ربات \n هر سوالی داری میتونی بپرسی!')


@dp.message_handler()
async def gpt(message: types.Message):
    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": message.text,
        }
    ],
    model="gpt-3.5-turbo",
    )
    await message.reply(chat_completion.choices[0].text)


if __name__ == '__main__':
    dp.start_polling(dp)