import asyncio
import datetime
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from pip._internal import commands
from config import token
from main import check_news_update
import telebot
import telegram
import surrogates


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Last news", "Picture", "Announcements"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Welcome to my channel! Click on one of the buttons below", reply_markup=keyboard)

# function for receiving the latest news from the site https://eec.eaeunion.org/news/
@dp.message_handler(Text(equals="Last news"))
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file: # use our dictionary with news from json-file
        news_dict = json.load(file)

    for k, v in news_dict.items(): # send news to Telegram
        news = f"{v['article_date_timestamp']}\n" \
               f"{v['article_title']}\n" \
               f"{v['article_desc']}\n" \
               f"{v['article_url']}"

        await message.answer(news)

# Sending a picture

@dp.message_handler(Text(equals="Picture"))
async def get_photo(message: types.Message):
    await bot.send_photo(chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')


# Announcement message

@dp.message_handler(Text(equals="Announcements"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()
    await message.answer("No announcements yet...")

if __name__ == '__main__':
    executor.start_polling(dp)
