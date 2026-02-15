from aiogram import Bot, Dispatcher
from aiogram.types import Message # , InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command

import os
from dotenv import load_dotenv
load_dotenv()

ADMINS = list(map(int, os.getenv("ADMINS").split(",")))

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: Message):
  await message.answer(text="Welcome to Mystery Bot! Type your anonymous message:")

@dp.message()
async def get_any_message(message: Message):
  # print(f"@{message.from_user.username} - {message.from_user.first_name} - {message.from_user.id}")
  for admin in ADMINS:
    try:
      await message.forward(chat_id=admin)
      await asyncio.sleep(0.05)
    except Exception as e:
      print(f"Failed to forward to {admin}: {e}")

async def main():
  await dp.start_polling(bot)

if __name__ == "__main__":
  try:
    import asyncio
    asyncio.run(main())
  except KeyboardInterrupt:
    pass

