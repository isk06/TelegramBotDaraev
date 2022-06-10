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
    start_buttons = ["Последние новости", "Картинка", "Анонсы"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Приветствую тебя на моем канале! Нажми на одну из кнопок ниже", reply_markup=keyboard)

# функция получения последних новостей с сайта https://eec.eaeunion.org/news/
@dp.message_handler(Text(equals="Последние новости"))
async def get_all_news(message: types.Message):
    with open("news_dict.json") as file: # используем наш словарь с новостями из json-файла
        news_dict = json.load(file)

    for k, v in news_dict.items(): # передаем новости в телеграм
        news = f"{v['article_date_timestamp']}\n" \
               f"{v['article_title']}\n" \
               f"{v['article_desc']}\n" \
               f"{v['article_url']}"

        await message.answer(news)

# отправка картинки

@dp.message_handler(Text(equals="Картинка"))
async def get_photo(message: types.Message):
    await bot.send_photo(chat_id=chat_id, photo='https://telegram.org/img/t_logo.png')


# сообщение об анонсах

@dp.message_handler(Text(equals="Анонсы"))
async def get_fresh_news(message: types.Message):
    fresh_news = check_news_update()
    await message.answer("Анонсов пока нет...")

if __name__ == '__main__':
    executor.start_polling(dp)
