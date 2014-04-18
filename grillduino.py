import scipy
import numpy
import matplotlib.pyplot as pyplot
import serial

print("Welcome to Grillduino!  Connected grilling for the masses!")

"""
Using the voltages dropped across the different resisters, calculate the 
resistance of each resistor.  R3 is the one in the heat.  Using a pre-stored
calibration, conver the resistance of R3 to temperature.  Plot.  Upload plot
to website.
"""
