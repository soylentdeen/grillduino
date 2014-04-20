import scipy
import numpy
import matplotlib.pyplot as pyplot
import serial
import tweetHandler
import guiHandler
import Tkinter

print("Welcome to Grillduino!  Connected grilling for the masses!")

"""
Using the voltages dropped across the different resisters, calculate the 
resistance of each resistor.  R3 is the one in the heat.  Using a pre-stored
calibration, convert the resistance of R3 to temperature.  Plot.  Upload plot
to website.  If temperature is outside of limits for too long, send a tweet.
Allow twitter users to send directed tweets to the twitter account requesting
a status update on the grill.
"""


root = Tkinter.Tk()
GuiClient = guiHandler.ThreadedClient(root)
root.mainloop()

print 'asdf'

Bird = tweetHandler.Tweety(GuiClient)

print 'fdsa'

Bird.checkFeed()

#Bird.startGrilling()

#Bird.stopGrilling()
