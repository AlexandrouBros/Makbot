import  discord
from    discord.ext import commands
import  asyncio

"""
The following file contains an implementation for a music queue.
It should be imported into "music.py", so that the Queue's methods
can be called on receiving a discord command.

"""

class Queue():

    # Initialisation and queue information
    def __init__(self):
        self.queue = []
        print('Queue_init')

    def __str__(self):
        return str(self.queue)


    def test(self):
        print('Queue_test')


    def skip(self, ctx):
        if self.queue != []:
          vc = ctx.voice_client
          vc.stop()
          song = self.getNext()
          return song


    def length(self):       # Return length of queue not including currently playing song 
        return len(self.queue) - 1


    def returnSong(self, pos):
        return self.queue[pos]


    def isEmpty(self):         # Check if there are any songs waiting to be played
        if len(self.queue) in (0,1):
            return True
        else: return False


    def positionOfSong(self, song):
        try:
            index = self.queue.index(song)
            return index
        except ValueError:
            return None


    # Adding to the queue
    def add(self, song):
        self.queue.append(song)
   

    # Remove last song from queue and return the next song
    def getNext(self):
        if self.isEmpty():
            return None
        else:
            self.queue = self.queue[1:]
            nextSong = self.queue[0]
            return nextSong
    

    def curSong(self):
        return self.queue[0]


    def clear(self):
        if self.queue != []:
            self.queue = self.queue[:1]
    

    def clearall(self):
        self.queue = []


    def removeAtPosition(self, position):
        try:
            index = int(position)
        except ValueError:
            print("Non-int supplied to addAtPosition, ignoring...")
            return None

        try:
            self.queue = self.queue[:position] + self.queue[position + 1:]
        except IndexError:
            print("Supplied position was out of range, ignoring")
            return None


    def addAtPosition(self, song, position): 
        try:
            index = int(position)
        except ValueError:
            print("Non-int supplied to addAtPosition, ignoring...")
            return None

        try:
            self.queue = self.queue[:position] + list(song) + self.queue[position:]
        except IndexError:
            if index <= 0:
                self.queue = list(song) + self.queue
            else:
                self.queue = self.queue + list(song)


    # Skipping
    def skipTo(self, position):
        if self.isEmpty():
            print("No songs in queue.")
            return None

        try:
            index = int(position)
        except ValueError:
            print("Non-int supplied to skip, ignoring...")
            return None

        try:
            self.queue = self.queue[index:]
        except IndexError:
            print("Supplied position was out of range, ignoring...")
            return None
