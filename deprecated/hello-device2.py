import evdev
import select
import json
import os.path
import alsaaudio
#import pygame
from SoundControl import SoundControl
from settings import *

###############################################################################
###############################################################################
##
##  LET'S SLEEP THIS BABY !
##
###############################################################################
###############################################################################

# set this up for the live listener
devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
devices = {dev.fd: dev for dev in devices}

print("We're set up and listening to the rotary encoder.")

#pygame.mixer.init()


# And kick off our infinite loop
done = False
countdown = 0

lullablock = SoundControl(volume_increment=2)

def main():
    while not done:
        r, w, x = select.select(devices, [], [])
        for fd in r:
            for event in devices[fd].read():
                event = evdev.util.categorize(event)

                if isinstance(event, evdev.events.RelEvent):
                    # read the current volume, adjust it, and then write back to the file
                    new_volume = lullablock.getVolume() + (event.event.value * lullablock.volume_increment)
                    v = lullablock.setVolume(new_volume) # this returns a clamped value

                elif isinstance(event, evdev.events.KeyEvent):
                    if event.keycode == "KEY_ENTER" and event.keystate == event.key_up:
                        # read the current volume, adjust it, and then write back to the file
                        new_timer = lullablock.setTimer()

                        if new_timer != 0:
                            # if pygame.mixer.music.get_busy() == False:
                            #     pygame.mixer.music.load(os.path.join(audioFolder,"pianoloop.mp3"))
                            #     pygame.mixer.music.play(loops=-1) #-1 loops = infinite
                        else:
                            # pygame.mixer.music.stop()

                        #done = True
                        #break

if __name__ == '__main__':
    main()
