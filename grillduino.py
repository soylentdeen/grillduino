import scipy
import numpy
import matplotlib.pyplot as pyplot
import serial
import twitter

def getTweetCreds():
    df = open('./twitter/login.dat', 'r')
    creds = {}
    for line in df:
        l = line.split()
        creds[l[0]] = l[1]
    return creds

print("Welcome to Grillduino!  Connected grilling for the masses!")

"""
Using the voltages dropped across the different resisters, calculate the 
resistance of each resistor.  R3 is the one in the heat.  Using a pre-stored
calibration, convert the resistance of R3 to temperature.  Plot.  Upload plot
to website.  If temperature is outside of limits for too long, send a tweet.
Allow twitter users to send directed tweets to the twitter account requesting
a status update on the grill.
"""

creds = getTweetCreds()

twit = twitter.Api(consumer_key=creds["ckey"],
        consumer_secret=creds["csecret"],
        access_token_key=creds["atkey"],
        access_token_secret=creds["atsecret"])

print twit.VerifyCredentials()

status = twit.PostUpdate("It's time to grill meat and chew bubble gum.  And I'm
all out of Bazooka Joe.")
#print status.text
