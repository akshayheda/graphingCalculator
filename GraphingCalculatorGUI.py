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
plt.style.use('seaborn-whitegrid')
LARGE_FONT = ("Verdana", 12)
csfont = {'fontname':'Comic Sans MS'}

fontSize = 10
fontName = "Segoe UI"

fig, ax = plt.subplots()

Y = "ReplacedWithFunction"

Xmin = -10.0
Xmax = 10.0
Ymin = -10.0
Ymax = 10.0
A = 0.0
B = 0.0
resolution = 0.001
compiledSuccess = False

ErrorLog = ""
eq = ""
eqPrev = ""
xminPrev = -10.0
xmaxPrev = 10.0
yminPrev = -10.0
ymaxPrev = 10.0
Aprev = 0.0
Bprev = 0.0

FTC = 0.0
FTCL = ""
integral = 0.0
app = 0


def animate(i):
    global app
    app.getFrame().updateFunction()
    global eq
    global ErrorLog
    eq = Equation.parse(eq)

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
    except NameError:
        compiledSuccess = False

    global Xmin
    global Xmax
    global Ymin
    global Ymax

    global A
    global B

    global xminPrev
    global xmaxPrev
    global yminPrev
    global ymaxPrev

    global integral
    global Aprev
    global Bprev

    xmin = Xmin
    xmax = Xmax
    ymin = Ymin
    ymax = Ymax

    AprevTemp = A
    BprevTemp = B

    xScale = 1
    yScale = 1



    boundEvalChange = False

    if( not(str(xminPrev) == str(xmin))) or not (str(xmaxPrev) == str(xmax) or not(str(yminPrev) == str(ymin))) or not \
            str(ymaxPrev) == str(ymax) or not(str(Aprev) == str(AprevTemp))or not (str(Bprev) == str(BprevTemp)):



        boundEvalChange = True

        xminPrev = xmin
        xmaxPrev = xmax
        yminPrev = ymin
        ymaxPrev = ymax
        Aprev = AprevTemp
        Bprev = BprevTemp

    global eqPrev

    eqPrevTemp = eq
    eqChange = False

    if (not (str(eqPrev) == str(eqPrevTemp))):
        eqChange = True

        eqPrev = eqPrevTemp

    if((eqChange and compiledSuccess) or ((boundEvalChange) and compiledSuccess)):

        ax.cla()

        boundEvalChange = False
        compiledSuccess = False
        eqChange = False

        print("New Function: f(x) = ", eq)
        print("Function or Bounds Changed: Updating Graph...")

        global Y
        try:
            Y = Equation(eq, xmin, xmax, ymin, ymax)
            initializationSuccess = True
        except TypeError:
            initializationSuccess = False

        if(initializationSuccess == True):
            fofx, = ax.plot(Y.getDomain(), Y.getYFunction(), "red", label = "Function")
            fprimeofx, = ax.plot(Y.getDomain(), Y.getYDeriv(), "blue", label = "First Derivative")
            fdoubleprimeofx, = ax.plot(Y.getDomain(), Y.getYSecondDeriv(), "green", label = "Second Derivative")

            fhole = plt.scatter(Y.getHoleCoor()[0], Y.getHoleCoor()[1], s=50, facecolors='none', edgecolors='purple')
            fextrema = plt.scatter(Y.getExtremaCoor()[0], Y.getExtremaCoor()[1], c="blue", s=25)
            finflection = plt.scatter(Y.getInflectionCoor()[0], Y.getInflectionCoor()[1], c="green", s=25)

            #plt.legend()
            plt.legend([fofx, fprimeofx, fdoubleprimeofx, fhole, fextrema, finflection] , ["Function","First Derivative", "Second Derivative", "Holes", "Extrema", "Inflection"], bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)


            global integral
            integral = 0
            integral = Y.integrate(A, B, 1)

            if(isnan(integral)):
                integral = "<Could Not Evaluate: Check Bounds>"
            else:
                integral = round(integral,5)

            global FTC
            FTC = 0
            FTC = round(Y.evaluate(B) - Y.evaluate(A), 5)

            global FTCL
            FTCL = ""
            FTCL = "f(" + str(B) + ") -  f(" + str(A) + ") = "

            print("Integral from A (", str(A) + " ) to B (", str(B) + " ) of f'(x) is " , str(integral))
            print("Showing FTC...")
            print("f(", str(B) + " ) -  f(", str(A) + " ) = ", str(round(Y.evaluate(B) - Y.evaluate(A),5 )))
            print("|-^-^-^-^-^-^-^-^-^-^-^-|", eq,"|-^-^-^-^-^-^-^-^-^-^-^-|" + "\n")

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
            plt.xticks(fontsize=10, **csfont)
            plt.yticks(fontsize=10, **csfont)
            plt.xticks(np.arange(xmin, xmax + 1, xScale))
            plt.yticks(np.arange(ymin, ymax + 1, yScale))

            #plt.savefig(eq + ".svg", dpi = 1000)

        app.getFrame().updateFunction()

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


        self.frame = GraphPage(container, self)

        self.frames[GraphPage] = self.frame

        self.frame.grid(row=0, column=0, sticky="nsew")

        self.frame.configure(background = "white")

        self.show_frame(GraphPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def getFrame(self):
        return self.frame



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

    global A
    global B
    global AEntry
    global BEntry

    global Y
    global integral
    global FTC

    def updateFunction(self):
        global label
        global eq
        global Xmax
        global Xmin
        global Ymax
        global Ymin

        global A
        global B

        global fontName
        global fontSize


        func = e1.get()

        eq = func

        try:
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

            if (len(AEntry.get()) > 0):
                A = float(AEntry.get())
            else:
                A = 0

            if (len(BEntry.get()) > 0):
                B = float(BEntry.get())
            else:
                B = 0

            IntegralLabelText = Label(self, text="Integral of f'(x) from A to B =", font=(fontName, fontSize))
            IntegralLabelText.grid(row=8, column=0)

            global integral

            IntegralLabel = Label(self, text=integral, font=(fontName, fontSize))
            IntegralLabel.configure(background = "white")
            IntegralLabel.grid(row=8, column=1)

            global FTCL

            FTCLabelText = Label(self, text=FTCL, font=(fontName, fontSize))
            FTCLabelText.configure(background = "white")
            FTCLabelText.grid(row=9, column=0)

            global FTC

            FTCLabel = Label(self, text=str(FTC), font=(fontName, fontSize))
            FTCLabel.configure(background = "white")
            FTCLabel.grid(row=9, column=1)

        except ValueError:
            print("Check Fields")





    def __init__(self, parent, controller):
        global fontName
        global fontSize

        global eq
        tk.Frame.__init__(self, parent)

        self.mainTitleText = StringVar()
        self.mainTitleText.set('Graphing Calculator')
        self.mainTitle = Label(self, text=self.mainTitleText.get(), font = (fontName,16))
        self.mainTitle.configure(background = "white")
        self.mainTitle.grid(row=0)

        global e1
        e1 = Entry(self)
        e1.configure(background = "#E0E0E0")
        e1.grid(row=2, column=1)

        EquationLabel = Label(self, text="f(x) =", font = (fontName,fontSize))
        EquationLabel.configure(background = "white")
        EquationLabel.grid(row=2, column=0)

        global xminEntry
        xminEntry = Entry(self)
        xminEntry.configure(background = "#E0E0E0")
        xminEntry.grid(row=3, column=1)

        xminLabel = Label(self, text="Xmin:", font = (fontName,fontSize))
        xminLabel.configure(background = "white")
        xminLabel.grid(row=3, column=0)

        global xmaxEntry
        xmaxEntry = Entry(self)
        xmaxEntry.configure(background = "#E0E0E0")
        xmaxEntry.grid(row=4, column=1)

        xmaxLabel = Label(self, text="Xmax:", font = (fontName,fontSize))
        xmaxLabel.configure(background = "white")
        xmaxLabel.grid(row=4, column=0)

        global yminEntry
        yminEntry = Entry(self)
        yminEntry.configure(background = "#E0E0E0")
        yminEntry.grid(row=5, column=1)

        yminLabel = Label(self, text="Ymin:", font = (fontName,fontSize))
        yminLabel.configure(background = "white")
        yminLabel.grid(row=5, column=0)

        global ymaxEntry
        ymaxEntry = Entry(self)
        ymaxEntry.configure(background = "#E0E0E0")
        ymaxEntry.grid(row=6, column=1)

        ymaxLabel = Label(self, text="Ymax:", font = (fontName,fontSize))
        ymaxLabel.configure(background = "white")
        ymaxLabel.grid(row=6, column=0)

        global AEntry
        AEntry = Entry(self)
        AEntry.configure(background = "#E0E0E0")
        AEntry.grid(row=7, column=1)

        ALabel = Label(self, text="Lower Limit (A):", font = (fontName,fontSize))
        ALabel.configure(background = "white")
        ALabel.grid(row=7, column=0)

        global BEntry
        BEntry = Entry(self)
        BEntry.configure(background = "#E0E0E0")
        BEntry.grid(row=8, column=1)

        BLabel = Label(self, text="Upper Limit (B):", font = (fontName,fontSize))
        BLabel.configure(background = "white")
        BLabel.grid(row=8, column=0)

        graphingFrame = Frame(self)
        canvas = FigureCanvasTkAgg(fig, graphingFrame)

        canvas.show()
        canvas.get_tk_widget().grid(row=1)

        canvas._tkcanvas.grid(row=2)
        graphingFrame.grid(row =1, columnspan=2, sticky=W)





app = GraphingCalculator()
ani = animation.FuncAnimation(fig, animate, interval=250)

app.mainloop()
