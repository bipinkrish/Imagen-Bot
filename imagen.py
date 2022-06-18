from pyrogram import Client
from pyrogram import filters
import threading
import os

'''bot_token = os.environ.get("TOKEN", "") 
api_hash = os.environ.get("HASH", "") 
api_id = os.environ.get("ID", "")''' 

api_id = 11223922
api_hash = "ac6664c07855e0455095d970a98a082d"
bot_token = "5358186417:AAGKQt1Xf2ps2gU0_CCkquAZRDofY7MKte8"

app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)

@app.on_message(filters.command(['start']))
def echo(client, message):
    app.send_message(message.chat.id,"send prompt with /imagen")

def get_filepaths(directory):
    file_paths = []

    for root, directories, files in os.walk(directory):
        for filename in sorted(files):
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths

def generate(iprompt,message):
    os.mkdir(f"{message.id}")
    cmd = f'cd {message.id} && imagine "{iprompt}" --image_width=256'
    os.system(cmd)
    files = get_filepaths(f"{message.id}")
    print(files)
    for ele in files:
        app.send_document(message.chat.id,document=ele)
        os.remove(ele)
    os.rmdir(f"{message.id}")

@app.on_message(filters.command(['imagen']))
def echo(client, message):
    iprompt = message.text.split("imagen ")[1]
    imag = threading.Thread(target=lambda:generate(iprompt,message),daemon=True)
    imag.start()

app.run()