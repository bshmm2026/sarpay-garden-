import asyncio
from pyrogram import Client, filters
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- သင့်ရဲ့ အချက်အလက်အမှန်များကို ထည့်သွင်းပေးထားပြီးပါပြီ ---
API_ID = 30099748               
API_HASH = "F22d0becf71e71a6f03743ab437076fb" 
BOT_TOKEN = "8923375079:AAEtYo-o9mhxjQz9OL8yStEVV9euaxOZr50"       
CHANNEL_ID = -1001289196901     
# --------------------------------------------------------

app = Client("my_book_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(f"👋 မင်္ဂလာပါ {message.from_user.mention} ရေ...\n\n📚 စာအုပ်နာမည် ရိုက်ပြီး အမြန်နှုန်းနဲ့ ရှာဖွေနိုင်ပါတယ်ခင်ဗျာ။")

@app.on_message(filters.text & filters.private)
async def search_book(client, message):
    query = message.text
    searching_msg = await message.reply_text("🔍 စာအုပ်ကို အမြန်နှုန်းဖြင့် ရှာဖွေနေပါတယ်...")
    results = []
    
    # Telegram Database ကနေ တိုက်ရိုက်ဆွဲထုတ်လို့ ပိုမိုမြန်ဆန်သွားစေပါတယ်
    async for msg in client.search_messages(CHANNEL_ID, query=query):
        if msg.document or msg.text:
            clean_id = str(CHANNEL_ID).replace("-100", "")
            post_link = f"https://t.me/c/{clean_id}/{msg.id}"
            
            if msg.document:
                title = msg.document.file_name
            elif msg.text:
                title = msg.text.split("\n")[0][:30] + "..."
            else:
                title = "စာအုပ်အညွှန်း"
                
            results.append(f"📘 **{title}**\n🔗 [စာအုပ်ရယူရန် နှိပ်ပါ]({post_link})\n")
            
        if len(results) >= 20:
            break
            
    if results:
        response_text = f"📚 **ရှာတွေ့ရရှိသော စာအုပ်များ ({len(results)} အုပ်) -**\n\n" + "\n".join(results)
        await searching_msg.edit_text(response_text, disable_web_page_preview=True)
    else:
        await searching_msg.edit_text("❌ ရှာမတွေ့ပါဘူးခင်ဗျာ။ အမည်ကို မှန်ကန်အောင် ပြန်ရိုက်ကြည့်ပေးပါ။")

class FaceServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is Running Alive!")

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), FaceServer)
    server.serve_forever()

async def main():
    threading.Thread(target=run_web_server, daemon=True).start()
    print("⚡ Bot Started Successfully with High Speed Search...")
    async with app:
        await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
