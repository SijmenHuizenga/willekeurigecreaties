import os

import time
from flask import render_template, send_from_directory, Flask
from uwsgidecorators import timer

from art import create_art

# Because uWSGI will run in multiple threads, some of which are spoolers, some might run in another working directory.
# So we need to ensure all th reads are looking at the same directory. Abosulte paths are the way to go.
source_art_dir = os.path.abspath("media")
generated_art_dir = os.path.abspath("art")

app = Flask(__name__)


# Run every hour
@timer(3600, target='mule')
def new_art(signum):
    print("creating new ART")
    file = str(int(time.time())) + ".jpg"
    create_art(source_art_dir, generated_art_dir + "/" + file)
    print("ART completed", file)

    return file


def last_art():
    generated_art = os.listdir(generated_art_dir)
    generated_art.sort()
    if len(generated_art) == 0:
        return new_art()
    return generated_art[len(generated_art) - 1]


@app.route('/')
def hello():
    return render_template('art.html', image=last_art())


@app.route('/art/<path:path>')
def send_art(path):
    return send_from_directory(generated_art_dir, path)


@app.route('/frame.webp')
def send_frame():
    return send_from_directory(".", "frame.webp")

