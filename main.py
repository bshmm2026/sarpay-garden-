import asyncio
from pyrogram import Client, filters, enums
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# --- သင့်ရဲ့ အချက်အလက်အမှန်များ ဖြစ်ပါတယ် ---
API_ID = 30099748               
API_HASH = "F22d0becf71e71a6f03743ab437076fb" 
BOT_TOKEN = "8923375079:AAEtYo-o9mhxjQz9OL8yStEVV9euaxOZr50"       
CHANNEL_ID = -1001289196901     
# --------------------------------------------------------

# ဤနေရာတွင် စောစောက ချိတ်ဆက်မှု လွဲချော်ခြင်းကို သေချာစွာ ပြင်ဆင်ထားပါသည်
app = Client(
    "my_book_bot", 
    api_id=API_ID, 
    api_hash=API_HASH, 
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text(f"👋 မင်္ဂလာပါ {message.from_user.mention} ရေ...\n\n📚 စာအုပ်နာမည် ရိုက်ပြီး စက္ကန့်ပိုင်းအတွင်း အမြန်ရှာဖွေနိုင်ပါပြီ ခင်ဗျာ။")

@app.on_message(filters.text & filters.private)
async def search_book(client, message):
    query = message.text.strip()
    searching_msg = await message.reply_text("🔍 စာအုပ်ကို အမြန်နှုန်းဖြင့် ရှာဖွေနေပါတယ်...")
    
    results = []
    
    try:
        # ချန်နယ်ထဲက Document (ဖိုင်) တွေကိုပဲ ကွက်တိ အမြန်နှုန်းနဲ့ ရှာခိုင်းပါတယ်
        async for msg in client.search_messages(CHANNEL_ID, query=query, filter=enums.MessagesFilter.DOCUMENT):
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
                
            # စာအုပ် ၅ အုပ်ပြည့်တာနဲ့ ရှာဖွေမှုကို ချက်ချင်းရပ်ခိုင်းလိုက်တဲ့အတွက် လျှပ်စီးလို မြန်သွားပါတယ်
            if len(results) >= 5:
                break
    except Exception:
        # အပေါ်ကစနစ် အဆင်မပြေပါက အရံအနေဖြင့် Limit ၅ အုပ်ဖြင့် အမြန်ပတ်ခြင်း
        async for msg in client.search_messages(CHANNEL_ID, query=query, limit=30):
            if msg.document or msg.text:
                clean_id = str(CHANNEL_ID).replace("-100", "")
                post_link = f"https://t.me/c/{clean_id}/{msg.id}"
                title = msg.document.file_name if msg.document else (msg.text[:30] + "...")
                results.append(f"📘 **{title}**\n🔗 [စာအုပ်ရယူရန် နှိပ်ပါ]({post_link})\n")
            if len(results) >= 5:
                break
                
    if results:
        response_text = f"📚 **%E1%80%9A%E1%80%BE%E1%80%AC%E1%80%B1%E1%80%90%E1%80%Bcode_%E1%80%B7%E1%80%Bcode_%E1%80%9B%E1%80%Bcode_%E1%80%Bcode_%E1%80%BE%E1%80%AD%E1%80%Bcode_%E1%80%Bcode_%E1%80%B1%E1%80%Bcode_%E1%80%Bcode_%E1%80%Bcode_%E1%80%Bcode_%E1%80%Bcode_%E1%80%A1%E1%80%AF%E1%80%Bcode_%E1%80%Bcode_%E1%80%Bcode_%E1%80%Bcode_%E1%80%Bcode_** ({len(results)} အုပ်) -\n\n" + "\n".join(results)
        await searching_msg.edit_text(response_text, disable_web_page_preview=True)
    else:
        await searching_msg.edit_text("❌ ရှာမတွေ့ပါဘူးခင်ဗျာ။ စာလုံးပေါင်း မှန်ကန်အောင် ပြန်ရိုက်ကြည့်ပေးပါ။")

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
    print("⚡ High Speed Engine Started with 5 Books Limit...")
    async with app:
        await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
