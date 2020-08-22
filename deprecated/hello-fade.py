import alsaaudio
import time
import pygame
import os.path
from settings import *

m = alsaaudio.Mixer('PCM')
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(configFolder, "../static/audio","pianoloop.mp3"))
pygame.mixer.music.play(loops=-1) #-1 loops = infinite
time.sleep(100)

# m = alsaaudio.Mixer('PCM')
# current_volume = m.getvolume() # returns a percentage
# print(current_volume)
#
# sleep_time = 0.2
#
# while current_volume[0] > 0:
#     current_volume = m.getvolume()
#     m.setvolume(max(0,current_volume[0]-1))
#     print(current_volume[0])
#     time.sleep(sleep_time)
