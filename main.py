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

def convert(sticker_file: BytesIO) -> BytesIO:
    sticker = Image.open(sticker_file)
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
async def convert_msg(message: types.Message):
    sticker = message.sticker
    if sticker.is_animated or sticker.is_video:
        await message.answer("ayo bruhv only static stickers please")
        return
    sticker_file = BytesIO()
    sticker_path = await sticker.download(sticker_file)
    emoji_file = convert(sticker_file)
    await message.answer_document(InputFile(emoji_file), caption=sticker_path)
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)