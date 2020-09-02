#!/usr/bin/env python3

# audio_test.py - simple pygame audio test
# Author Michael Ludvig

import pygame

# PyGame initialisation
pygame.init()
pygame.mixer.init()

# Audio file from Scratch
audio = '/home/pi/lullablock/static/audio/chop.wav'

# Play the audio and wait for completion
pygame.mixer.music.load(audio)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
