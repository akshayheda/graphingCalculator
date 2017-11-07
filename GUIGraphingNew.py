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
from Equation import Equation

LARGE_FONT = ("Verdana", 12)

fig, ax = plt.subplots()

Xmin = -10.0
Xmax = 10.0
Ymin = -10.0
Ymax = 10.0
resolution = 0.001
compiledSuccess = False

showF = True
showFPrime = True
showFDoublePrime = True
showMarkers = True
Integrate = True
ErrorLog = ""
eq = ""
eqPrev = "memes"
xminPrev = -10.0
xmaxPrev = 10.0
yminPrev = -10.0
ymaxPrev = 10.0

def parse():
    global eq

    eq = eq.lower()
    eq = eq.replace("^", "**")
    eq = eq.replace("fabs(", "abs(")
    eq = eq.replace("sec(", "(1)/cos(")
    eq = eq.replace("csc(", "(1)/sin(")
    eq = eq.replace("cot(", "(1)/tan(")

    eq = eq.replace("1x", "1*x")
    eq = eq.replace("2x", "2*x")
    eq = eq.replace("3x", "3*x")
    eq = eq.replace("4x", "4*x")
    eq = eq.replace("5x", "5*x")
    eq = eq.replace("6x", "6*x")
    eq = eq.replace("7x", "7*x")
    eq = eq.replace("8x", "8*x")
    eq = eq.replace("9x", "9*x")
    eq = eq.replace("0x", "0*x")

    eq = eq.replace("1(", "1*(")
    eq = eq.replace("2(", "2*(")
    eq = eq.replace("3(", "3*(")
    eq = eq.replace("4(", "4*(")
    eq = eq.replace("5(", "5*(")
    eq = eq.replace("6(", "6*(")
    eq = eq.replace("7(", "7*(")
    eq = eq.replace("8(", "8*(")
    eq = eq.replace("9(", "9*(")
    eq = eq.replace("0(", "0*(")

    eq = eq.replace("1s", "1*s")
    eq = eq.replace("2s", "2*s")
    eq = eq.replace("3s", "3*s")
    eq = eq.replace("4s", "4*s")
    eq = eq.replace("5s", "5*s")
    eq = eq.replace("6s", "6*s")
    eq = eq.replace("7s", "7*s")
    eq = eq.replace("8s", "8*s")
    eq = eq.replace("9s", "9*s")
    eq = eq.replace("0s", "0*s")

    eq = eq.replace("1c", "1*c")
    eq = eq.replace("2c", "2*c")
    eq = eq.replace("3c", "3*c")
    eq = eq.replace("4c", "4*c")
    eq = eq.replace("5c", "5*c")
    eq = eq.replace("6c", "6*c")
    eq = eq.replace("7c", "7*c")
    eq = eq.replace("8c", "8*c")
    eq = eq.replace("9c", "9*c")
    eq = eq.replace("0c", "0*c")

    eq = eq.replace("1t", "1*t")
    eq = eq.replace("2t", "2*t")
    eq = eq.replace("3t", "3*t")
    eq = eq.replace("4t", "4*t")
    eq = eq.replace("5t", "5*t")
    eq = eq.replace("6t", "6*t")
    eq = eq.replace("7t", "7*t")
    eq = eq.replace("8t", "8*t")
    eq = eq.replace("9t", "9*t")
    eq = eq.replace("0t", "0*t")

    eq = eq.replace("1l", "1*l")
    eq = eq.replace("2l", "2*l")
    eq = eq.replace("3l", "3*l")
    eq = eq.replace("4l", "4*l")
    eq = eq.replace("5l", "5*l")
    eq = eq.replace("6l", "6*l")
    eq = eq.replace("7l", "7*l")
    eq = eq.replace("8l", "8*l")
    eq = eq.replace("9l", "9*l")
    eq = eq.replace("0l", "0*l")

    eq = eq.replace("1a", "1*a")
    eq = eq.replace("2a", "2*a")
    eq = eq.replace("3a", "3*a")
    eq = eq.replace("4a", "4*a")
    eq = eq.replace("5a", "5*a")
    eq = eq.replace("6a", "6*a")
    eq = eq.replace("7a", "7*a")
    eq = eq.replace("8a", "8*a")
    eq = eq.replace("9a", "9*a")
    eq = eq.replace("0a", "0*a")

    eq = eq.replace("1g", "1*g")
    eq = eq.replace("2g", "2*g")
    eq = eq.replace("3g", "3*g")
    eq = eq.replace("4g", "4*g")
    eq = eq.replace("5g", "5*g")
    eq = eq.replace("6g", "6*g")
    eq = eq.replace("7g", "7*g")
    eq = eq.replace("8g", "8*g")
    eq = eq.replace("9g", "9*g")
    eq = eq.replace("0g", "0*g")

    eq = eq.replace(")(", ")*(")


def animate(i):

    global eq
    global ErrorLog
    parse()

    try:
        func = compile(eq, "temp.py", "eval")
        ErrorLog = eq
        x = 0
        eval(func)
        compiledSuccess = True
    except ZeroDivisionError:
        compiledSuccess = True
    except ValueError:
        compiledSuccess = True
    except SyntaxError:
        compiledSuccess = False
        ErrorLog = "CHECK FUNCTION: ERROR!!!"
        print("CHECK FUNCTION: ERROR!!!")
    except NameError:
        compiledSuccess = False
        ErrorLog = "CHECK FUNCTION: ERROR!!!"
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

    global showF
    global showFPrime
    global showFDoublePrime
    global showMarkers
    global Integrate
    print("\n", "Show Values")
    print("showF: ", showF)
    print("showFPrime: ", showFPrime)
    print("showFDoublePrime: ", showFDoublePrime)
    print("showMarkers: ", showMarkers)
    print("Integrate: ", Integrate)

    if((len(eq) > 0 and not(eqPrev == eq) and compiledSuccess) or (boundEvalChange) and compiledSuccess):
        print(boundEvalChange)

        boundEvalChange = False
        compiledSuccess = False
        ax.cla()

        eqPrev = eq

        Y = Equation(eq, xmin, xmax)


        if showF:
            ax.plot(Y.getDomain(), Y.getYFunction(), "red")
        if showFPrime:
            ax.plot(Y.getDomain(), Y.getYDeriv(), "blue")
        if showFDoublePrime:
            ax.plot(Y.getDomain(), Y.getYSecondDeriv(), "green")
        if showMarkers:
            plt.scatter(Y.getHoleCoor()[0], Y.getHoleCoor()[1], s=100, facecolors='none', edgecolors='purple')
            plt.scatter(Y.getExtremaCoor()[0], Y.getExtremaCoor()[1], c="orange", s=100)
            plt.scatter(Y.getInflectionCoor()[0], Y.getInflectionCoor()[1], c="black", s=100)
        if Integrate:
            integral = Y.Integrate(xmin, xmax,0 )
            print(integral)

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

    global showF
    global showFPrime
    global showFDoublePrime
    global showMarkers
    global Integrate

    global showFButtonVar

    def updateFunction(self):
        global label
        global eq
        global Xmax
        global Xmin
        global Ymax
        global Ymin

        global showF
        global showFPrime
        global showFDoublePrime
        global showMarkers
        global Integrate

        global showFButton
        global showFPrimeButton
        global showFDoublePrimeButton
        global showMarkersButton
        global IntegrateButton

        global showFButtonVar

        global ErrorLog
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

        #print(showFButtonVar.get())
        #if(showFButtonVar.get() == 0):
            #showF = False
        #else:
         #   showF = True
        Log = eq


    def __init__(self, parent, controller):
        global eq
        tk.Frame.__init__(self, parent)

        self.mainTitleText = StringVar()
        self.mainTitleText.set('Graphing Calculator')
        self.mainTitle = Label(self, text=self.mainTitleText.get())
        self.mainTitle.grid(row=0)

        global e1
        e1 = Entry(self)
        e1.grid(row=1, column=1)
        EquationLabel = Label(self, text="f(x) =")
        EquationLabel.grid(row=1, column=0)

        global xminEntry
        xminEntry = Entry(self)
        xminEntry.grid(row=2, column=1)

        xminLabel = Label(self, text="Xmin:")
        xminLabel.grid(row=2, column=0)

        global xmaxEntry
        xmaxEntry = Entry(self)
        xmaxEntry.grid(row=3, column=1)

        xmaxLabel = Label(self, text="Xmax:")
        xmaxLabel.grid(row=3, column=0)

        global yminEntry
        yminEntry = Entry(self)
        yminEntry.grid(row=4, column=1)

        yminLabel = Label(self, text="Ymin:")
        yminLabel.grid(row=4, column=0)

        global ymaxEntry
        ymaxEntry = Entry(self)
        ymaxEntry.grid(row=5, column=1)

        ymaxLabel = Label(self, text="Ymax:")
        ymaxLabel.grid(row=5, column=0)

        global showFButton
        global showFPrimeButton
        global showFDoublePrimeButton
        global showMarkersButton
        global IntegrateButton

        global ErrorLog
        LogLabel = Label(text=str(ErrorLog))
        LogLabel.pack()

        global showFButtonVar
        showFButtonVar = IntVar()
        showFButton = Checkbutton(self, text="Show f(x)", variable = showFButtonVar, onvalue = 1, offvalue = 0)
        showFButton.grid(row=6)
        showFButton.select()




        showFPrime = BooleanVar()
        '''
        Checkbutton(self, text="Show f'(x)", variable=showFPrime).grid(row=7)
        showFDoublePrime = BooleanVar()
        Checkbutton(self, text="Show f''(x)", variable=showFDoublePrime).grid(row=8)
        showMarkers = BooleanVar()
        Checkbutton(self, text="Show markers", variable=showMarkers).grid(row=9)
        '''
        button1 = Button(self, text="Graph!", command=self.updateFunction)
        button1.grid(row=10)

        graphingFrame = Frame(self)
        canvas = FigureCanvasTkAgg(fig, graphingFrame)

        canvas.show()
        canvas.get_tk_widget().grid(row=1)

        canvas._tkcanvas.grid(row=2)
        graphingFrame.grid(row =11, column = 2)




app = GraphingCalculator()
ani = animation.FuncAnimation(fig, animate, interval=1000)
app.mainloop()
