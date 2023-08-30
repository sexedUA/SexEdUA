import asyncio
from main_bot import dp
from admin_bot import dp as dp_admin
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading


class DummyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Replace with an appropriate message
        self.wfile.write("Bot is running!")
        return


def run_dummy_server():
    server_address = ('', 10000)  # Choose a port that's not used by your bot
    httpd = HTTPServer(server_address, DummyRequestHandler)
    print('Dummy server is running...')
    httpd.serve_forever()


async def run_bots():
    tasks = [
        asyncio.create_task(dp.start_polling()),
        asyncio.create_task(dp_admin.start_polling())
    ]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    dummy_thread = threading.Thread(target=run_dummy_server)
    dummy_thread.start()
    asyncio.run(run_bots())
