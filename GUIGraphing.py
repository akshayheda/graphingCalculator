from __future__ import division
from math import *
import math
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import numpy as np
import tkinter as tk
from tkinter import *
from graphingCalculator.Equation import Equation

LARGE_FONT = ("Verdana", 12)

fig, ax = plt.subplots()

Xmin = -10.0
Xmax = 10.0
Ymin = -10.0
Ymax = 10.0
resolution = 0.001
compiledSuccess = False

eq = ""
eqPrev = "memes"
xminPrev = -10.0
xmaxPrev = 10.0
yminPrev = -10.0
ymaxPrev = 10.0

def animate(i):
    global eq

    eq = eq.lower()
    eq = eq.replace("^", "**")
    eq = eq.replace("sec(", "(1)/cos(")
    eq = eq.replace("csc(", "(1)/sin(")
    eq = eq.replace("cot(", "(1)/tan(")

    try:
        func = compile(eq, "temp.py", "eval")

        x = 0
        eval(func)
        compiledSuccess = True
    except ZeroDivisionError:
        compiledSuccess = True
    except ValueError:
        compiledSuccess = True
    except SyntaxError:
        compiledSuccess = False
        print("CHECK FUNCTION: ERROR!!!")
    except NameError:
        compiledSuccess = False
        print("CHECK FUNCTION: ERROR!!!")



    global eqPrev

    global Xmin
    global Xmax
    global Ymin
    global Ymax

    global xminPrev
    global xmaxPrev
    global yminPrev
    global ymaxPrev

    xmin = Xmin
    xmax = Xmax
    ymin = Ymin
    ymax = Ymax
    xScale = 1
    yScale = 1



    boundEvalChange = False

    if( not(str(xminPrev) == str(xmin))) or not (str(xmaxPrev) == str(xmax) or not(str(yminPrev) == str(ymin))) or not (str(ymaxPrev) == str(ymax) ):



        boundEvalChange = True

        print("xMin " + str(xminPrev) + " | " + str(xmin))
        print("xMax " + str(xmaxPrev) + " | " + str(xmax))
        print("yMin " + str(yminPrev) + " | " + str(ymin))
        print("yMax " + str(ymaxPrev) + " | " + str(ymax))

        xminPrev = xmin
        xmaxPrev = xmax
        yminPrev = ymin
        ymaxPrev = ymax

        print("\n")

    try:
        func = compile(eq, "temp.py", "eval")

        x = 0
        eval(func)
        compiledSuccess = True
    except ZeroDivisionError:
        compiledSuccess = True
    except ValueError:
        compiledSuccess = True
    except SyntaxError:
        compiledSuccess = False
        print("CHECK FUNCTION: ERROR!!!")
    except NameError:
        compiledSuccess = False
        print("CHECK FUNCTION: ERROR!!!")

    if((len(eq) > 0 and not(eqPrev == eq) and compiledSuccess) or (boundEvalChange) and compiledSuccess):
        print(boundEvalChange)

        boundEvalChange = False

        print(len(eq))

        print("Reseting")
        ax.cla()
        compiledSuccess = False
        eqPrev = eq

        Y = Equation(eq, xmin, xmax)

        print("Graphing")
        ax.plot(Y.getDomain(), Y.getYFunction(), "red")
        ax.plot(Y.getDomain(), Y.getYDeriv(), "blue")
        ax.plot(Y.getDomain(), Y.getYSecondDeriv(), "green")

        plt.scatter(Y.getHoleCoor()[0], Y.getHoleCoor()[1], s=100, facecolors='none', edgecolors='purple')
        plt.scatter(Y.getExtremaCoor()[0], Y.getExtremaCoor()[1], c="orange", s=100)
        plt.scatter(Y.getInflectionCoor()[0], Y.getInflectionCoor()[1], c="black", s=100)
        print(Y.getInflectionCoor()[0], Y.getInflectionCoor()[1])

    ax.set_ylim([ymin, ymax])

    ax.grid(False, which='both')

    # set the x-spine (see below for more info on `set_position`)
    ax.spines['left'].set_position('zero')

    # turn off the right spine/ticks
    ax.spines['right'].set_color('none')
    ax.yaxis.tick_left()

    # set the y-spine
    ax.spines['bottom'].set_position('zero')

    # turn off the top spine/ticks
    ax.spines['top'].set_color('none')
    ax.xaxis.tick_bottom()
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.xticks(np.arange(xmin, xmax + 1, xScale))
    plt.yticks(np.arange(ymin, ymax + 1, yScale))


class GraphingCalculator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        tk.Tk.wm_title(self, "Graphing Calculator")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}


        frame = GraphPage(container, self)

        self.frames[GraphPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(GraphPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()



class GraphPage(tk.Frame):
    global eq
    global label

    global Xmax
    global Xmin
    global xminEntry
    global xmaxEntry

    global Ymax
    global Ymin
    global yminEntry
    global ymaxEntry

    def updateFunction(self):
        global label
        global eq
        global Xmax
        global Xmin
        global Ymax
        global Ymin

        func = e1.get()
        print("Trying to update")
        eq = func
        print(eq)
        if(len(xminEntry.get()) > 0):
            Xmin = float(xminEntry.get())
        else:
            Xmin = -10.0

        if (len(xmaxEntry.get()) > 0):
            Xmax = float(xmaxEntry.get())
        else:
            Xmax = 10.0

        if (len(yminEntry.get()) > 0):
            Ymin = float(yminEntry.get())
        else:
            Ymin = -10.0

        if (len(ymaxEntry.get()) > 0):
            Ymax = float(ymaxEntry.get())
        else:
            Ymax = 10.0



    def __init__(self, parent, controller):
        global eq
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Graphing Calculator ", font=LARGE_FONT)
        label.pack(pady=10, padx=10)



        global e1
        e1 = Entry(self)

        e1.pack()
        e1.focus_set()

        global xminEntry
        xminEntry = Entry(self)

        xminEntry.pack()
        xminEntry.focus_set()

        global xmaxEntry
        xmaxEntry = Entry(self)

        xmaxEntry.pack()
        xmaxEntry.focus_set()

        global yminEntry
        yminEntry = Entry(self)

        yminEntry.pack()
        yminEntry.focus_set()

        global ymaxEntry
        ymaxEntry = Entry(self)

        ymaxEntry.pack()
        ymaxEntry.focus_set()

        button1 = Button(self, text="Graph!",command=self.updateFunction )
        button1.pack()

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


app = GraphingCalculator()
ani = animation.FuncAnimation(fig, animate, interval=1000)
app.mainloop()
