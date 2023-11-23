# GPG Sender and Receiver
Send and receive files with a single command using Telegram Bot and API.
This application is mainly meant to facilitate the exchange of encrypted
files between two fixed users, but it can be easily changed to ask the
sender which recipient should be getting the encrypted message.

## What you need to obtain
- A Telegram Bot API Key
- Its User ID (try forwarding one of your bot's messages to @userinfobot on Telegram)
- Your personal API ID and API Hash : [Here](https://my.telegram.org/apps)

## What you need to configure
- receiver/.env (use the provided .env.example as a template)
- sender/.env (use the provided .env.example as a template)
- The path to your receiver .env in receiver/gpgbot.py
- The path to your sender .env in sender/sender.py
- The recipient's name or email in send-enc-files.sh (GPG)
