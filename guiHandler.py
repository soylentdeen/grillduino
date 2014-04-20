import numpy
import Tkinter
import time
import threading
import serial
import random
import Queue
import matplotlib.pyplot as pyplot
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tweetHandler

class GuiPart:
    def __init__(self, master, queue, endCommand):
        self.queue = queue
        out = open('calibration.dat', 'w')
        out.close()
        self.startTime = time.time()
        # Set up the GUI

        DoneButton = Tkinter.Button(master, text='Done', command=endCommand)
        DoneButton.pack()

        RefreshButton = Tkinter.Button(master, text='Refresh',
            command=self.refresh)
        RefreshButton.pack()

        self.TempEntry = Tkinter.Entry(master)
        self.TempEntry.bind('<Return>', self.addTemp)
        self.TempEntry.pack()

        self.R1 = 1000.0
        self.R2 = 1000.0

        self.V1 = numpy.array([])
        self.V2 = numpy.array([])
        self.V3 = numpy.array([])
        self.R3 = numpy.array([])
        self.T3 = numpy.array([])
        self.Vtime = numpy.array([])
        self.meattemp = [numpy.array([]), numpy.array([])]

        figure = pyplot.figure(figsize=(5, 4), dpi=100)
        axis = figure.add_axes([0.1, 0.1, 0.8, 0.8])

        self.V1line, = axis.plot(self.Vtime, self.V1, marker='o')
        self.V2line, = axis.plot(self.Vtime, self.V2, marker='o')
        self.V3line, = axis.plot(self.Vtime, self.V3, marker='o')
        self.meatline, = axis.plot(self.meattemp[0], self.meattemp[1])
        self.canvas = FigureCanvasTkAgg(figure, master)
        self.canvas.show()
        self.canvas._tkcanvas.pack(side=Tkinter.TOP,fill=Tkinter.BOTH, expand=1)
        # Add more GUI stuff here

    def calculateTemp(self):
        #I = numpy.mean((self.V1[-1]-self.V2[-1])/self.R1, 
        #        (self.V2[-1]-self.V3[-1])/self.R2)
        print self.V2[-1], self.V3[-1], self.R2
        I = (self.V2[-1]-self.V3[-1])/self.R2
        print I, self.V3[-1], self.V3[-1]/I
        self.R3 = numpy.append(self.R3, self.V3[-1]/I)
        #self.T3.append(self.R3*self.slope + self.yint)

    def refresh(self):
        self.V1line.set_data(self.Vtime, self.V1)
        self.V2line.set_data(self.Vtime, self.V2)
        self.V3line.set_data(self.Vtime, self.V3)
        self.calculateTemp()
        out = open('calibration.dat', 'a')
        out.write(str(self.Vtime[-1])+" "+str(self.R3[-1])+'\n')
        out.close()
        self.meatline.set_data(self.meattemp[0], self.meattemp[1])
        ax = self.canvas.figure.axes[0]
        print 'update: ', self.R3[-1]
        try:
           ax.set_xlim(min(self.Vtime), max(self.Vtime)+1.0)
           ax.set_ylim(0.0, 5.5)
        except:
           pass
        self.canvas.draw()

    def addTemp(self, event):
        try:
            temp = float(self.TempEntry.get())
            t = time.time()-self.startTime
            self.temp[0] = numpy.append(self.temp[0], t)
            self.temp[1] = numpy.append(self.temp[1], temp)
        except:
            print "Error!"
	

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # As a test, we simply print it
                #print msg
                self.V1 = numpy.append(self.V1, msg[0])
                self.V2 = numpy.append(self.V2, msg[1])
                self.V3 = numpy.append(self.V3, msg[2])
                self.Vtime = numpy.append(self.Vtime, msg[3]-self.startTime)
                self.refresh()
            except Queue.Empty:
                pass

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        self.Bird = tweetHandler.Tweety()

        # Create the queue
        self.queue = Queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
    	self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()
        self.thread2 = threading.Thread(target=self.tweeterThread)
        self.thread2.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(1000, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        self.serial = serial.Serial(port='/dev/ttyUSB0')
        while self.running:
	    #print self.serial.inWaiting()
            if self.serial.inWaiting() != 0:
                arduino_data = numpy.array(self.serial.readline().split(), 
                                dtype=float)
                msg = arduino_data.tolist()
                msg.append(time.time())
                self.queue.put(msg)
            else:
                #print("Waiting")
                time.sleep(5)

    def tweeterThread(self):
        """
        This is where the tweeting is handled.
        """

        self.

    def endApplication(self):
        self.running = 0
        self.serial.close()


