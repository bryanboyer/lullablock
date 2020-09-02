import datetime
import json
import os.path
import asyncio
import pygame
from threading import Timer
import time
import sys
from settings import timerDurations, configFolder, audioFolder, blipFile, readyFile, audioFeedbackVolume

mixer = pygame.mixer.init()
print("Mixer status: ", mixer)

# Makes sure Volume is within appropriate levels
def clampVolume(n, min_value, max_value):
    return max(min_value,min(int(n),max_value))

# Returns the closest number from a list
def closest(list, k):
    return list[min(range(len(list)), key = lambda i: abs(list[i]-k))]

class FancyTimer(Timer):
    started_at = None
    def start(self):
        self.started_at = time.time()
        Timer.start(self)
    def elapsed(self):
        return time.time() - self.started_at
    def remaining(self):
        return max(self.interval - self.elapsed(),0)

class SoundControl:
    def getVolume(self):
        with open(os.path.join(configFolder, "volume.json")) as f:
            volume = json.load(f)
            return volume['level']

    def setVolume(self,new_volume):
        with open(os.path.join(configFolder, "volume.json"),'r+') as f:
            read_volume = json.load(f)
            if str(new_volume)[0] == "+":
                new_volume = clampVolume(read_volume['level'] + int(str(new_volume)[1:]),self.min_volume,self.max_volume)
            elif str(new_volume)[0] == "-":
                new_volume = clampVolume(read_volume['level'] - int(str(new_volume)[1:]),self.min_volume,self.max_volume)
            else:
                new_volume = clampVolume(new_volume,self.min_volume,self.max_volume)

            # change the volume!
            pygame.mixer.music.set_volume(new_volume/100)

            # write to the file
            print("Volume was {0} and is now {1}. (JSON: {2})".format(read_volume['level'],new_volume,read_volume))
            read_volume['level'] = new_volume
            self.writeVolume(new_volume,f)

            return new_volume

    def writeVolume(self,new_volume:int,file=False):
        if file:
            try:
                file.truncate(0)
                file.seek(0)
                json.dump({"level":new_volume},file)
            except:
                print("Could not write the Volume to disk.")
        else:
            print("writeVolume requires a file")


    def getTracks(self):
        with open(os.path.join(configFolder, "tracks.json")) as f:
            file = json.load(f)
            return file['tracks']

    def getTrack(self):
        with open(os.path.join(configFolder, "track.json")) as f:
            track = json.load(f)
            return track['filename']

    def setTrack(self, new_track):
        with open(os.path.join(configFolder, "track.json"),'r+') as f:
            read_track = json.load(f)
            read_track['filename'] = new_track
            f.seek(0)
            f.write(json.dumps(read_track))
            f.truncate()

            # check to see if something is playing,
            # if so, check the timer, change the track, then start playing again
            print("Now we will change the soundz")
            if pygame.mixer.music.get_busy() == True:
                pygame.mixer.music.stop()
                pygame.mixer.music.load(os.path.join(audioFolder,new_track))
                pygame.mixer.music.play(loops=-1) #-1 loops = infinite

                r = self.countdown.remaining()
                self.countdown.cancel()
                self.countdown = FancyTimer(r, self.stopTrack)
                self.countdown.start()

            return new_track

    def startTrack(self):
        track_filename = self.getTrack()
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.load(os.path.join(audioFolder,track_filename))
            pygame.mixer.music.play(loops=-1) #-1 loops = infinite

    def stopTrack(self):
        pygame.mixer.music.stop()
        # Cannot use pygame.mixer.music.fadeout(5000) to fadeout because
        # it is blocking. So you will need to write a custom fadeout function
        if self.countdown != False: self.countdown.cancel()
        self.writeTimer(0)
        self.blip()

    def getTimer(self):
        with open(os.path.join(configFolder, "timer.json")) as f:
            timer = json.load(f)
            return timer['duration']

    # does not take argument because we merely bop through the available timer settings
    def setTimer(self):
        with open(os.path.join(configFolder, "timer.json"),'r+') as f:
            read_timer = json.load(f)

            c = closest(self.timerDurations,read_timer['duration'])
            c = self.timerDurations.index(c)+1
            new_timer = self.timerDurations[c] if c < len(self.timerDurations) else self.timerDurations[0]

            print("Timer was {0} and is now {1}.".format(read_timer['duration'],new_timer))
            read_timer['duration'] = new_timer

            # now write the new timer
            self.writeTimer(new_timer,f)

            if (new_timer > 0):
                self.startTrack()
                if self.countdown != False: self.countdown.cancel()
                self.countdown = FancyTimer(new_timer, self.stopTrack)
                self.countdown.start()
            else:
                self.stopTrack()

            return new_timer

    def writeTimer(self,new_time:int,file=False):
        if file:
            try:
                file.truncate(0)
                file.seek(0)
                json.dump({"duration":new_time},file)
            except:
                print("Could not write the Timer to disk.")
        else:
            try:
                with open(os.path.join(configFolder, "timer.json"),'w') as f:
                    json.dump({"duration":0},f)
            except:
                print("Could not write the Timer to disk.")

    def timerRemaining(self):
        if self.countdown is False:
            return 0
        else:
            return self.countdown.remaining()

    def blip(self):
        self.audioFeedback(blipFile)

    def ready(self):
        self.audioFeedback(readyFile)

    def audioFeedback(self,audioFile):
        beforeVolume = self.getVolume()
        self.setVolume(audioFeedbackVolume)
        pygame.mixer.music.load(audioFile)
        pygame.mixer.music.play(1) #-1 loops = infinite
        self.setVolume(beforeVolume)

    def __init__(self, volume:int=50, timer:int=60, track="pianoloop.mp3"):
        self.min_volume = 0
        self.max_volume = 100
        self.volume = self.getVolume()
        self.track = self.getTrack()
        self.timerDurations = timerDurations
        self.timer = self.getTimer()
        self.countdown = False
        # set the timer up so it's begins at the right place since
        # we're turning on for the first time
        self.writeTimer(self,0)
