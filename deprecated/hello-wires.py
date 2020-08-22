import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)

sleeptime = 0.1

fired = False

count = 0

try:
 while True:
    clicker_state = GPIO.input(23)
    if clicker_state == False:
        print('Clicker Button Pressed')
        fired = True

    ccw_state = GPIO.input(24)
    if ccw_state == False:
        print('Counter-Clockwise')
        fired = True

    cw_state = GPIO.input(25)
    if cw_state == False:
        print('Clockwise')
        fired = True

    if fired == True:
        count = count + 1
        print("count",count,"state",clicker_state,ccw_state,cw_state)
        fired = False

        time.sleep(sleeptime)
except:
 print('\n\nExiting with cleanup')
 GPIO.cleanup() # use this instead
