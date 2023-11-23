import asyncio
import logging
import sys

from aiotdlib import Client

from dotenv import load_dotenv
from os import getenv

if not load_dotenv("/full/path/to/sender/.env"):
    print("sender: Error loading .env, quitting")
    raise SystemExit

try:
    API_ID = int(getenv("API_ID"))
    API_HASH = getenv("API_HASH")
    PHONE_NUMBER = getenv("PHONE_NUMBER")
    RECEIVER_BOT_USER_ID = int(getenv("RECEIVER_BOT_USER_ID"))
except Exception as e:
    print("sender: Error parsing environment variables", e)
    raise SystemExit


async def send_file(client, file_path):
    content = {
        "@type": "inputMessageDocument",
        "document": {"@type": "inputFileLocal", "path": file_path},
        "@extra": 1, # Is this needed?
    }

    resp = await client.api.send_message(
        chat_id=RECEIVER_BOT_USER_ID,
        input_message_content=content,
        skip_validation=True,
    )
    # Validation seems to always fail, but if we skip it, the message sends successfully
    # print(resp)
    # return resp


async def main(files):
    client = Client(api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

    async with client:
        for f in files:
            await send_file(client, f)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: sender.py FILE [FILE ...]")
        raise SystemExit
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main(sys.argv[1:]))
