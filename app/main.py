import os

import time
import schedule
from threading import Thread

import werkzeug
from flask import Flask, render_template, send_from_directory

from art import create_art

source_art_dir = "media"
generated_art_dir = "art"


def new_art():
    print("creating new ART")
    file = generated_art_dir + "/" + str(int(time.time())) + ".jpg"
    create_art(source_art_dir, file)
    global current_art
    current_art = file
    print("ART completed", file)

    return file


def last_art():
    generated_art = os.listdir(generated_art_dir)
    generated_art.sort()
    if len(generated_art) == 0:
        return new_art()
    return generated_art[len(generated_art)-1]


current_art = last_art()
print(current_art)


def art_thread():
    print("Started ART thread")

    schedule.every().hour.do(new_art)

    while True:
        schedule.run_pending()
        time.sleep(1)


thread = Thread(target=art_thread)
thread.daemon = True

if not werkzeug.serving.is_running_from_reloader():
    thread.start()

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('art.html', image=current_art)


@app.route('/art/<path:path>')
def send_art(path):
    return send_from_directory(generated_art_dir, path)


@app.route('/frame.png')
def send_frame():
    return send_from_directory(".", "frame.png")


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=8123)
