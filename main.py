import asyncio
from pyrogram import Client, filters

# --- မိမိ အချက်အလက်များ ---
API_ID = 26733221               
API_HASH = "812542a197b09c5d263301a91e5e01df" 
BOT_TOKEN = "8923375079:AAEtYo-o9mhxjQz9OL8yStEVV9euaxOZr50"       
CHANNEL_ID = -1001289196901     
# -------------------------------------------

app = Client("my_book_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(f"👋 မင်္ဂလာပါ {message.from_user.mention} ရေ...\n\n📚 စာအုပ်နာမည် ရိုက်ပြီး ရှာဖွေနိုင်ပါတယ်ခင်ဗျာ။")

@app.on_message(filters.text & filters.private)
async def search_book(client, message):
    query = message.text
    searching_msg = await message.reply_text("🔍 စာအုပ်ရှာဖွေနေပါတယ်...")
    results = []
    async for msg in client.search_messages(CHANNEL_ID, query=query, limit=10):
        if msg.document or msg.text:
            clean_id = str(CHANNEL_ID).replace("-100", "")
            post_link = f"https://t.me/c/{clean_id}/{msg.id}"
            title = msg.document.file_name if msg.document else (msg.text[:30] + "...")
            results.append(f"📘 **{title}**\n🔗 [စာအုပ်ရယူရန် နှိပ်ပါ]({post_link})\n")
    if results:
        response_text = "📚 **ရှာတွေ့ရရှိသော စာအုပ်များ -**\n\n" + "\n".join(results)
        await searching_msg.edit_text(response_text, disable_web_page_preview=True)
    else:
        await searching_msg.edit_text("❌ ရှာမတွေ့ပါဘူးခင်ဗျာ။")

print("⚡ Bot Running with Async Loop...")

# Event Loop Error ကို ကျော်ရန် ဤနေရာကို ပြင်ဆင်ထားပါသည်
async def main():
    async with app:
        await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
