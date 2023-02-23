from aiogram.types.input_file import InputFile

from PIL import Image
import os

import logging
from io import BytesIO
from PIL import Image
from aiogram import Bot, Dispatcher, executor, types


TOKEN = ""


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# https://note.nkmk.me/en/python-pillow-add-margin-expand-canvas/
def expand2square(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result

def convert(sticker_file: BytesIO) -> BytesIO:
    sticker = Image.open(sticker_file)
    max_dim = max(sticker.width, sticker.height)
    new_dim = (int((sticker.width/max_dim)*100), int((sticker.height/max_dim)*100))
    sticker.resize(new_dim)
    emoji_img = expand2square(sticker, background_color=(255, 0, 0, 0))
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
    sticker_path = await sticker.download(destination_file=sticker_file)
    emoji_file = convert(sticker_file)
    await message.answer_document(InputFile(emoji_file), caption=sticker_path)
    

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
