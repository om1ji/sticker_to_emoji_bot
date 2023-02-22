from bot_token import TOKEN

import logging
from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Send sticker and properly resized image for emoji will be returned")

@dp.message_handler(content_types=["sticker"])
async def echo(message: types.Message):
    """Downloads sticker as an image to /sticker folder"""
    await message.sticker.download()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)