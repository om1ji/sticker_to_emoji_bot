from bot_token import TOKEN
from aiogram.types.input_file import InputFile

from PIL import Image
import os

import logging
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Send sticker and a properly resized image for emoji will be returned")

@dp.message_handler(content_types=["sticker"])
async def echo(message: types.Message):
    sticker_path = await message.sticker.download()

    image = Image.open(sticker_path.name)

    # Waiting for Artemetra
    
    await message.answer_document(InputFile(sticker_path))
    os.remove(sticker_path)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)