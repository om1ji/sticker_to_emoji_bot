from bot_token import TOKEN
from aiogram.types.input_file import InputFile

from PIL import Image
import os

import logging
from io import BytesIO
from PIL import Image
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

def convert(image_data: BytesIO) -> BytesIO:
    sticker = Image.open(image_data)
    max_dim = max(sticker.width, sticker.height)
    new_dim = (int((sticker.width/max_dim)*100), int((sticker.height/max_dim)*100))
    sticker.resize(new_dim)
    emoji_img = Image.new(sticker.mode, (100,100), (255, 0, 0, 0))
    emoji_img.paste(sticker, (max_dim//2))
    emoji_file = BytesIO()
    emoji_img.save(emoji_file, 'png')
    return emoji_file

@dp.message_handler(commands=['start', 'help'])
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