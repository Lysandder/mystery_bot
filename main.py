from aiogram import Bot, Dispatcher
from aiogram.types import Message # , InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters.command import Command

import asyncio
from aiohttp import web

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

# --- Tiny web server for Render ---
async def health(request):
    return web.Response(text="ok")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_get("/healthz", health)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", "10000"))
    site = web.TCPSite(runner, host="0.0.0.0", port=port)
    await site.start()

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
