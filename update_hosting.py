import ngrok
import time
import os
import socket
import logging
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import traceback

logging.basicConfig()

if not firebase_admin._apps:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cookie-netflix-48899-firebase-adminsdk-6bxuo-c48d262735.json"
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://cookie-netflix-48899-default-rtdb.firebaseio.com/'})


def get_credential():
    path = f"/credentials/ngrok/SETUP_TOKEN_{socket.gethostname().upper()}"
    data = db.reference(path).get()
    default_return = "", 80
    if data is None:
        return default_return
    if "TOKEN" not in data or "PORT" not in data:
        return default_return
    return data["TOKEN"], data["PORT"]


def update_public_url():
    db.reference(f"/public_urls/{socket.gethostname()}").set({PORT: listener.url()})
    logging.info(f"Update public url: {listener.url()}")


def main():
    while True:
        try:
            update_public_url()
            time.sleep(update_interval)
        except:
            logging.error(traceback.TracebackException.msg)


TOKEN, PORT = get_credential()
logging.info(f"Found TOKEN: {TOKEN} and PORT: {PORT}")
logging.info(f"Running with hostname: {socket.gethostname()}")
listener = ngrok.forward(PORT, authtoken=TOKEN)
update_interval = 15 * 60
main()
