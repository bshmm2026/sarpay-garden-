import asyncio
from pyrogram import Client, filters, enums
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

BOT_TOKEN = "8923375079:AAEtYo-o9mhxjQz9OL8yStEVV9euaxOZr50"       
CHANNEL_ID = -1001289196901     

app = Client(
    "my_book_bot", 
    api_id=6, 
    api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e", 
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start_cmd(client, message):
    await message.reply_text("👋 Hello! Type book name to search.")

@app.on_message(filters.text & filters.private)
async def search_book(client, message):
    query = message.text.strip()
    searching_msg = await message.reply_text("🔍 Searching...")
    
    results = []
    
    try:
        async for msg in client.search_messages(CHANNEL_ID, query=query, filter=enums.MessagesFilter.DOCUMENT):
            if msg.document:
                clean_id = str(CHANNEL_ID).replace("-100", "")
                post_link = f"https://t.me/c/{clean_id}/{msg.id}"
                title = msg.document.file_name
                results.append(f"📘 **{title}**\n🔗 [Download]({post_link})\n")
                
            if len(results) >= 5:
                break
    except Exception as e:
        print(f"Error: {e}")
        async range_search in client.search_messages(CHANNEL_ID, query=query, limit=20):
            if msg.document or msg.text:
                clean_id = str(CHANNEL_ID).replace("-100", "")
                post_link = f"https://t.me/c/{clean_id}/{msg.id}"
                title = msg.document.file_name if msg.document else (msg.text[:30] + "...")
                results.append(f"📘 **{title}**\n🔗 [Download]({post_link})\n")
            if len(results) >= 5:
                break
                
    if results:
        response_text = f"📚 **Found ({len(results)} books) -**\n\n" + "\n".join(results)
        await searching_msg.edit_text(response_text, disable_web_page_preview=True)
    else:
        await searching_msg.edit_text("❌ Not Found! Try again.")

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
    print("⚡ Engine Started...")
    async with app:
        await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
