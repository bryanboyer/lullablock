# Lullablock

A pink noise maker for Horatio.

# Hardware BOM
Lullablock is built on top of a Raspberry Pi Zero WH.

- [Raspberry Pi Zero WH (Zero W with Headers)](https://www.adafruit.com/product/3708)
- [Adafruit I2S 3W Stereo Speaker Bonnet for Raspberry Pi - Mini Kit](https://www.adafruit.com/product/3346)
- [Stereo Enclosed Speaker Set - 3W 4 Ohm](https://www.adafruit.com/product/1669)
- [ky040 Rotary Encoder, from Cylewet](https://www.amazon.com/Cylewet-Encoder-15%C3%9716-5-Arduino-CYT1062/dp/B06XQTHDRR)
- Power supply
- Terminal blocks and wire as needed

# Hardware setup
GPIO connections made via the prototyping area on the Speaker Bonnet:
- CLK -> GPIO Pin 12
- DT -> GPIO Pin 13
- SW -> GPIO Pin 16
- Plus Sign -> 5V 
- GND -> Ground

# Software setup
- Device tree to capture input from GPIO pins [as seen here](https://blog.ploetzli.ch/2018/ky-040-rotary-encoder-linux-raspberry-pi/).
- Python 3.7
- [Pygame](https://www.pygame.org/) provides audio control
- [Flask](https://flask.palletsprojects.com/) provides the webserver

Edit `/etc/rc.local`, which will run on boot, to include:
```
sudo -i -u pi python3.7 /home/pi/lullablock/server.py &
```
This runs the server as user `pi` so that the dependencies are ok. There's probably a better way to install Python modules so that this is not a problem but ugh.
