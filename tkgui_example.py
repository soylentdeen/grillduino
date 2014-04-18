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
# implement the default mpl key bindings
#from matplotlib.backend_bases import key_press_handler

class GuiPart:
    def __init__(self, master, queue, endCommand):
        self.queue = queue
        # Set up the GUI

	vcmd = (master.register(self.addTemp), 
               '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        #self.entry = tk.Entry(self.root, validate="key", validatecommand=vcmd)

        DoneButton = Tkinter.Button(master, text='Done', command=endCommand)
        DoneButton.pack()

	RefreshButton = Tkinter.Button(master, text='Refresh',
			command=self.refresh)
        RefreshButton.pack()

	self.TempEntry = Tkinter.Entry(master)
	self.TempEntry.bind('<Return>', self.addTemp)
	self.TempEntry.pack()

	self.data = numpy.array([])
	self.temp = [numpy.array([]), numpy.array([])]

        figure = pyplot.figure(figsize=(5, 4), dpi=100)
	axis = figure.add_axes([0.1, 0.1, 0.8, 0.8])

        self.line, = axis.plot(self.data)
	self.canvas = FigureCanvasTkAgg(figure, master)
	self.canvas.show()
	#toolbar = NavigationToolbar2TkAgg( canvas, master )
	#toolbar.update()
	self.canvas._tkcanvas.pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
	# Add more GUI stuff here


    def refresh(self):
        self.line.set_data(range(len(self.data)), self.data)
        ax = self.canvas.figure.axes[0]
        ax.set_xlim(0, len(self.data))
        ax.set_ylim(self.data.min(), self.data.max())        
        self.canvas.draw()

    def addTemp(self, event):
       temp = float(self.TempEntry.get())
       t = time.clock()
       self.temp[0] = numpy.append(self.temp[0], t)
       self.temp[1] = numpy.append(self.temp[1], temp)
       print "Hi!"
	

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                # As a test, we simply print it
                #print msg
		self.data = numpy.append(self.data, numpy.array(msg, numpy.float))
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

        # Create the queue
        self.queue = Queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
    	self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

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
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.
            time.sleep(rand.random() * 0.3)
            msg = rand.random()
            self.queue.put(msg)

    def endApplication(self):
        self.running = 0

rand = random.Random()
root = Tkinter.Tk()

client = ThreadedClient(root)
root.mainloop()

