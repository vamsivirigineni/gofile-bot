from pyrogram import Client, filters
import requests
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "gofile-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.document | filters.video)
async def upload_file(client, message):
    msg = await message.reply("Downloading file...")

    file_path = await message.download()

    await msg.edit("Uploading to Gofile...")

    server = requests.get("https://api.gofile.io/getServer").json()["data"]["server"]

    with open(file_path, "rb") as f:
        response = requests.post(
            f"https://{server}.gofile.io/uploadFile",
            files={"file": f}
        ).json()

    link = response["data"]["downloadPage"]

    os.remove(file_path)

    await msg.edit(f"Gofile Link:\n{link}")

print("Bot Started")

app.run()
