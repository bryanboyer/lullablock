# 🤫🔊 Lullablock

### Pink noise machine for baby Fred and other humans

Plays an audio file on loop until a timer runs out and that's all it does. Package includes 3dprint for the case and code to run everything on a Raspberry Pi Zero W. Controls are via a single large dial/button or via web app. This could (should?) have been done on an Arduino, but Fred can't tell the difference. Shhhhh.

![alt text](https://github.com/bryanboyer/lullablock/blob/master/3dprint/lullablock_build.jpg?raw=true)

# 🔧 Build Instructions

Directions below may have gaps. If so, oops! Good luck.

## 🛒 Hardware BOM
Lullablock is built on top of a Raspberry Pi Zero WH.

- [Raspberry Pi Zero WH (Zero W with Headers)](https://www.adafruit.com/product/3708)
- [Adafruit I2S 3W Stereo Speaker Bonnet for Raspberry Pi - Mini Kit](https://www.adafruit.com/product/3346)
- [Stereo Enclosed Speaker Set - 3W 4 Ohm](https://www.adafruit.com/product/1669)
- [ky040 Rotary Encoder, from Cylewet](https://www.amazon.com/Cylewet-Encoder-15%C3%9716-5-Arduino-CYT1062/dp/B06XQTHDRR)
- Power supply
- Terminal blocks and/or wire as needed
- Case using [supplied 3D print files](https://github.com/bryanboyer/lullablock/tree/master/3dprint) or your own design
- Handful of nylon M2.5 screws and hex nuts
- Handful of nylon 6-32 thumbscrews and hex nuts

## 🧰 Hardware setup
Start by assembling the Speaker Bonnet and attaching it to your RPI Zero. you will also need to build a case, or use the 3d printing files provided in this package to print one.

Then you're ready to:
1. Base: screw the RPI to the base using M2.5 screws and nuts.
2. Body: attach rotary encoder to the top of the body using the nut and washer that it comes with. Attach speakers to the sides using M2.5 screws and nuts.
3. Attach all wires between the rotary encoder and the RPI, as well as between the speakers and the speaker bonnet. I used [jumpers](https://www.adafruit.com/product/1953?gclid=CjwKCAiA25v_BRBNEiwAZb4-ZRbKXj26y8MHqaMjv3Fv1vKvwB_-EpQndhkhp318n3Iuip4fMkSVdhoChYwQAvD_BwE) and soldered terminals but you can also solder wires directly. The Speaker Bonnet includes a prototyping area, so you will be connecting to that with the following:
  - ROTARY ENCODER CLK -> GPIO Pin 12
  - ROTARY ENCODER DT -> GPIO Pin 13
  - ROTARY ENCODER SW -> GPIO Pin 16
  - ROTARY ENCODER Plus Sign -> 5V 
  - ROTARY ENCODER GND -> Ground
4. Connect power cable to RPI.
5. Glue [6-32 nylon hex nuts](https://www.mcmaster.com/catalog/126/3382) into the receptacles on the bottom of the Body.
6. Assemble body and base! Use [6-32 Nylon Thumb Screws, 1/4" Long](https://www.mcmaster.com/catalog/126/3265), to secure it closed.
7. Infill: rotary knobs have slight variarions, so depending on which one you use you may need to devise your own infill piece that connects the 3d printed dial cover (knob) to the metal stem of the rotary encoder. The infill piece fits over the metal stem, which then slots into the hole on the bottom of the dial. Friction should hold everything in place but you can glue it as well if you like.

## 👾 Software setup, install the following:
- [Raspbian Buster Lite](https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2020-12-04/2020-12-02-raspios-buster-armhf-lite.zip)
- Python 3.7
- [I2S DAC per Adafruit](https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi/raspberry-pi-usage)
- [Pygame](https://www.pygame.org/) provides audio control
- [Flask](https://flask.palletsprojects.com/) provides the web app framework
- [NGINX](https://www.nginx.com/) provides the webserver
- [Gunicorn3](https://gunicorn.org/)  

## 🌳 Edit the Device Tree
Add the following to `/boot/config.txt` based on [these instructions](https://blog.ploetzli.ch/2018/ky-040-rotary-encoder-linux-raspberry-pi/):
```
# enable rotary encoder
dtoverlay=rotary-encoder,pin_a=12,pin_b=13,relative_axis=1
dtoverlay=gpio-key,gpio=16,keycode=28,label="ENTER"
dtoverlay=hifiberry-dac
dtoverlay=i2s-mmap
```

## ⚡️ Set up system services
Copy `rotarylistener.service.example` to `/etc/systemd/system/rotarylistener.service`. From there you can:
- Start with `sudo systemctl start rotarylistener.service`
- Stop with `sudo systemctl stop rotarylistener.service`
- Check with `systemctl status rotarylistener.service`
- Tail logs for the service by using: `journalctl -f -u rotarylistener.service`

Enable NGINX by copying `lullablock.service.example` to `/etc/nginx/sites-available/` and then symlink that file to `/etc/nginx/sites-available/lullablock` with `sudo ln -s /etc/nginx/sites-available/lullablock /etc/nginx/sites-enabled/lullablock`
- Test config file with `sudo nginx -t`
- Restart the server `sudo systemctl restart nginx`

Set up the worker by copying `lullablock.service.example` to `/etc/systemd/system/lullablock.service`
- Start with `sudo systemctl start lullablock`

## 🔐 Security Notice
Fair warning: no effort has been made to secure this device, so make sure your RPI has a good password. Lullablock does not need to connect to the outside world for anything, so you can also wall it off from the open internet without impeding functionality.

-----------------------------

# 👉 How to use Lullablock

Lullablock plays an audio file on loop until a timer runs out. Physical and digital interfaces are provided to change the timer duration and volume. Setting a new audio track will require connecting via the app/web interface.

## 🎚 Physical Interface

Lullablock has a set of timer durations, by default 90, 45, 15, and 0 minutes (these can be changed in `settings.py`). Pressing the big dial will advance through these timers. For instance, if Lullablock is off, pressing the dial will turn on the sound and begin counting down to 90 minutes. At the end of the timer it will shut off. Tap a second time and the timer will be reduced to 45 minutes, again and it will be 15 miniutes, one more time and Lullablock will tiurn off.

Turning the dial will decrease or increase the volume based on the direction of rotation. Technically, this happens by sending API calls for each increment of rotation so you will find that there's a small delay between spinning the dial and hearing the change. This is a bad way to implement the dial controls but... I couldn't figure out a better way to do it and maintain state. Ooops.

## 📱 Digital Interface

Find your device on the network and load that in a browser, such as the one on your phone. For instance, my Lullablock uses the [hostname](https://www.howtogeek.com/167195/how-to-change-your-raspberry-pi-or-other-linux-devices-hostname/) lullablock.local and can be found at http://lullablock.local. Once the page loads you will have the ability to turn volume up and down by tapping the - and + icons. The |‾|\_|‾|\_|‾|\_| graphic is a representation of the countdown to silence. Click it to start the timer.

## 🎶 Customizing Lullablock

To change the audio that plays on loop, upload new audio files to `static/audio`. The files must be WAV or MP3 format. In the app you can change the track by clicking on the trackname in the upper left corner of the screen and then clicking on the track you would like to play. For instance, you might edit together your own loop of [cafe chatter from the BBC](https://sound-effects.bbcrewind.co.uk/search?q=cafe) or crickets or something. 🦗
