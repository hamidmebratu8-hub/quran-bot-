import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
import yt_dlp

API_ID = int(os.getenv("API_ID", "123456")) 
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")

app = Client("MyQuranBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

@app.on_message(filters.command("play") & (filters.group | filters.channel))
async def play_audio(client, message: Message):
    if len(message.command) < 2:
        await message.reply("⚠️ እባክዎ የሱራውን ወይም የಖሪውን ስም ይጻፉ!\nምሳሌ፦ `/play አል በቃራ`")
        return

    query = " ".join(message.command[1:]) + " Quran recitation"
    status_msg = await message.reply(f"🔍 '{query}' በመፈለግ ላይ ይገኛል...")

    ydl_opts = {'format': 'bestaudio', 'default_search': 'ytsearch1:', 'noplaylist':True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(query, download=False)
            audio_url = info['entries'][0]['url']
            title = info['entries'][0]['title']

        chat_id = message.chat.id
        await call_py.join_group_call(chat_id, AudioPiped(audio_url))
        await status_msg.edit(f"🎧 **በመጫወት ላይ:**\n📌 {title}")
    except Exception as e:
        await status_msg.edit(f"❌ ስህተት አጋጥሟል: `{str(e)}`")

@app.on_message(filters.command("stop") & (filters.group | filters.channel))
async def stop_audio(client, message: Message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply("⏹ የድምፅ ስርጭቱ ቆሟል።")
    except Exception as e:
        await message.reply(f"ስታቆም ስህተት ተፈጥሯል: `{e}`")

async def main():
    await app.start()
    await call_py.start()
    print("ቦቱ በተሳካ ሁኔታ ተጀምሯል!")
    await asyncio.gather(app.idle(), call_py.idle())

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
