import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP) # click
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP) # CW
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP) # CCW

clk = 24
dt = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

clkLastState = GPIO.input(clk)

def my_callback(channel):
    global clkLastState
    global counter
    try:
            clkState = GPIO.input(clk)
            dtState = GPIO.input(dt)
            # print(clkState, dtState)
            # 00 cw
            # 01 ccw

            if clkState == False and dtState == False:
                counter += 1
            elif clkState == False and dtState == True:
                counter -= 1

            #
            # if clkState != clkLastState:
            #     if dtState != clkState:
            #         counter += 1
            #     else:
            #         counter -= 1
            #
            #     print(counter)
            #     clkLastState = clkState
            #     #sleep(0.01)
    finally:
        print(counter)
        # print("Ending")


counter = 0
clkLastState = GPIO.input(clk)
GPIO.add_event_detect(24, GPIO.FALLING  , callback=my_callback, bouncetime=300)
input("Enter anything")
GPIO.cleanup()
