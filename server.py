#!/usr/bin/env python3.7

from flask import Flask, render_template, redirect, url_for
import datetime
import json
import threading
from subprocess import call
from SoundControl import SoundControl
from settings import volumeIncrement, apiEndpoint, apiEndpointForWeb

app = Flask(__name__)

lullablock = SoundControl()
print ("lullablock status: ", lullablock)

def timerInMinutes():
    return round(lullablock.getTimer()/60,1)

@app.route('/')
def index():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")

    templateData = {
        'volume' : lullablock.getVolume(),
        'timer_in_minutes' : timerInMinutes(),
        'time': timeString,
        'tracks': lullablock.getTracks(),
        'track': lullablock.getTrack(),
        'remaining': lullablock.timerRemaining(),
        'timerDurations': lullablock.timerDurations,
        'timerLength': lullablock.getTimer(),
        'apiEndpoint': apiEndpointForWeb
    }

    return render_template('page-svg.html', **templateData)


@app.route('/timer/bop')
def timerBop():
    t = lullablock.setTimer()
    return redirect(url_for('index'))

@app.route('/api/timer')
def api_timerBop():
    msg = False
    msg = lullablock.setTimer()
    return f"{msg}"

@app.route('/start')
def start():
    lullablock.startTrack()
    return redirect(url_for('index'))

@app.route('/stop')
def stop():
    lullablock.stopTrack()
    return redirect(url_for('index'))

@app.route('/volume/<direction>')
def volume(direction):
    if direction.lower() == "up":
        v = lullablock.setVolume("+"+str(volumeIncrement))
    elif direction.lower() == "down":
        v = lullablock.setVolume("-"+str(volumeIncrement))
    else:
        v = lullablock.setVolume(int(direction))
    return redirect(url_for('index'))

@app.route('/api/volume/<direction>')
def api_volume(direction):
    msg = False

    if direction[0] == "+":
        v = lullablock.setVolume(f"+{volumeIncrement}")
        msg = True
    elif direction[0] == "-":
        v = lullablock.setVolume(f"-{volumeIncrement}")
        msg = True
    else:
        v = lullablock.setVolume(int(direction))
        msg = True

    v = lullablock.getVolume()

    return f"{v}"

@app.route('/tracks')
def tracks():
    return redirect(url_for('index'))

@app.route('/tracks/play/<filename>')
def playTrack(filename):
    lullablock.setTrack(filename)
    return redirect(url_for('index'))

@app.route('/api/ready')
def api_ready():
    msg = False
    lullablock.ready()
    msg = True
    return f"{msg}"

def initListener():
    print("Starting up the device listener.")
    call(["python3.7", "/home/pi/lullablock/rotaryEncoderListener.py"])

if __name__ == '__main__':
    debugMode = False
    print ("The __main__ function is running.")

    if debugMode:
        print("\u001b[31m Don't forget to start rotaryEncoderListener.py ! \u001b[0m")
    else:
        # Start a new thread for hardware listener
        print("\u001b[31m Starting the device listener ! \u001b[0m")
        processThread = threading.Thread(target=initListener)
        processThread.start()

    app.run(debug=debugMode, host='0.0.0.0')
