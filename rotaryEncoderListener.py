import evdev
import select
import json
import os.path
import requests
from settings import volumeIncrement, apiEndpoint

# set this up for the live listener
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
devices = {dev.fd: dev for dev in devices}

try:
    r = requests.get(f"{apiEndpoint}ready")
    if (r.text != "True"): print("An error occured while notifying the server that we're monitoring the rotary encoder.")
except:
    print("Failed to connect to the webserver. Maybe it's not running?")

# And kick off our infinite loop
def main():
    done = False
    while not done:
        r, w, x = select.select(devices, [], [])
        for fd in r:
            for event in devices[fd].read():
                event = evdev.util.categorize(event)
                if isinstance(event, evdev.events.RelEvent):
                    if (event.event.value > 0):
                        try:
                            r = requests.get(f"{apiEndpoint}volume/+{str(event.event.value * volumeIncrement)}")
                            if (r.text != "True"): print("An error occured setting the volume")
                        except:
                            print("Failed to connect to the webserver. Maybe it's not running?")
                    else:
                        try:
                            r = requests.get(f"{apiEndpoint}volume/{str(event.event.value * volumeIncrement)}")
                            if (r.text != "True"): print("An error occured setting the volume")
                        except:
                            print("Failed to connect to the webserver. Maybe it's not running?")

                elif isinstance(event, evdev.events.KeyEvent):
                    if event.keycode == "KEY_ENTER" and event.keystate == event.key_up:
                        try:
                            r = requests.get(f"{apiEndpoint}timer")
                            if (int(r.text) < 0): print("An error occured setting the volume")
                        except:
                            print("Failed to connect to the webserver. Maybe it's not running?")

if __name__ == '__main__':
    main()
