import asyncio
import aiofiles
import os

from BotClass import UserBot
from pyrogram import compose
from concurrent.futures import ThreadPoolExecutor

# Установите chat_id чата, на который вы хотите реагировать
chat_id = 0

# Установите api_id и api_hash вашего аккаунта Telegram
api_id = 0
api_hash = ""


async def ainput(prompt: str = "") -> str:
    with ThreadPoolExecutor(1, "AsyncInput") as executor:
        return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)


async def start_bots():
    global bot
    user_bots = []
    with open("codes.txt") as file:
        text = file.read()
        data = text.split(", ")
        file.close()
    bot = UserBot(name="1", target=chat_id, card_begin=data, api_id=api_id, api_hash=api_hash)
    user_bots.append(await bot.starts())
    await compose(user_bots, sequential=True)


async def console_reading():
    global bot
    await asyncio.sleep(40)
    while True:
        command = await ainput("> ")
        if command == "help":
            print("Available commands:\n"
                  "cards: look at which cards have a filter\n"
                  "n_cards: append new codes into codes.txt\n"
                  "r_cards: reset all codes in codes.txt\n"
                  "stop: stop bot")
        elif command == "tasks_info":
            tasks = asyncio.all_tasks()
        elif command == "cards":
            if os.stat("codes.txt").st_size:
                card_numbers = ", ".join([i for i in open("codes.txt")])
            else:
                card_numbers = "No card codes"
            print(card_numbers)
        elif command == "n_cards":
            new_cards = await ainput("> ")
            async with aiofiles.open("codes.txt", "a") as file:
                if os.stat("codes.txt").st_size:
                    await file.write(f", {new_cards}")
                else:
                    await file.write(f"{new_cards}")
                await file.close()
            await bot.update_codes()
        elif command == "r_cards":
            new_cards = await ainput("> ")
            with open("codes.txt", "w") as file:
                file.write(f"{new_cards}")
                file.close()
            await bot.update_codes()
        elif command == "stop":
            tasks = asyncio.all_tasks()
            for task in tasks:
                task.cancel()
            break


async def main():
    polling_task = asyncio.create_task(start_bots())
    console = asyncio.create_task(console_reading())

    await asyncio.gather(polling_task, console)


if __name__ == "__main__":
    asyncio.run(main())
