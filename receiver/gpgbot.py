import asyncio
import logging
import sys
import hashlib
from os import getenv, path, makedirs
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ContentType
from aiogram.utils.markdown import hbold

from notify import notification

if not load_dotenv("/full/path/to/receiver/.env"):
    print("gpgbot: Error loading .env, quitting")
    raise SystemExit

try:
    TOKEN = getenv("BOT_TOKEN")
    FILES_FOLDER = path.expanduser(getenv("FILES_FOLDER"))
except Exception as e:
    print("gpgbot: Error parsing environment variables", e)
    raise SystemExit

if not path.exists(FILES_FOLDER):
    makedirs(FILES_FOLDER)
    print(f"gpgbot: Created folder {FILES_FOLDER}")
elif not path.isdir(FILES_FOLDER):
    print(f"gpgbot: {FILES_FOLDER} exists but is not a directory, quitting...")
    raise SystemExit

dp = Dispatcher()

bot = None


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def handler(message: types.Message) -> None:
    try:
        m_ct = message.content_type
        if m_ct != ContentType.DOCUMENT:
            print(f"gpgbot: Received ContentType '{m_ct}', ignoring")
            await message.answer("Content type not supported, ignoring.")
            return

        invalid_chars = '<>:"/\|?* '
        filename = message.document.file_name
        for c in invalid_chars:
            filename.replace(c, "")
        destination = f"{FILES_FOLDER}/{filename}"

        await bot.download(message.document, destination)

        filehash = hashlib.sha256(open(destination, "rb").read()).hexdigest()

        notif_filename = filename if len(filename <= 10) else filename[:10] + "..."

        notification(
            "Encrypted message received",
            app_name="GPGTelegramBot",
            timeout=5000,
            message=f"Message from {message.from_user.full_name}: {notif_filename} - {filehash[:5]}...",
        )

        await message.answer(f"Received! File SHA256: {filehash}")
    except Exception as e:
        print("gpgbot: There was an error.", e)
        await message.answer("Error!")
    finally:
        await message.delete()  # Should we delete the file after downloading it?


async def main() -> None:
    global bot
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
