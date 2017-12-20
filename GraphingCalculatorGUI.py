from math import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import numpy as np
import platform
import tkinter as tk
from tkinter import *

#determines OS, and changes font depending on OS
OperatingSystem = platform.system()
OperatingSystem = "Windows"
if(OperatingSystem == "Windows"):
    from Equation import Equation
    fontName = "Segoe UI"
else:
    from graphingCalculator.Equation import Equation
    fontName = "Arial Narrow"
fontSize = 10
TickFont = {'fontname':fontName}
TickFontSize = 10


#declares the graph
fig, ax = plt.subplots()

#styles the graph with domain/range, axis, and ticks
ax.set_ylim([-10, 10])
ax.grid(False, which='both')
ax.spines['left'].set_position('zero')
ax.spines['right'].set_color('none')
ax.yaxis.tick_left()
ax.spines['bottom'].set_position('zero')
ax.spines['top'].set_color('none')
ax.xaxis.tick_bottom()
plt.xticks(fontsize=TickFontSize, **TickFont)
plt.yticks(fontsize=TickFontSize, **TickFont)
plt.xticks(np.arange(-10, 10 + 1, 1))
plt.yticks(np.arange(-10, 10 + 1, 1))



Y = "ReplacedWithFunction"
#globals for inputs, with default values
Xmin = -10.0
Xmax = 10.0
Ymin = -10.0
Ymax = 10.0
A = 0.0
B = 0.0
resolution = 0.001
compiledSuccess = False

#previous values of inputs, to check for change in input
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
FTCL = "f(" + "B" + ") -  f(" + "A" + ") = "
integral = 0.0
app = 0

#global booleans for whether to show functions
showF = True
showFPrime = True
showFDoublePrime = True

#update function, run regularly to update according to changes on the GUI
def animate(i):
    global app
    #app.getFrame().updateFunction()
    global eq
    global ErrorLog
    eq = Equation.parse(eq)
    #attempts to compile function to verify proper input
    try:
        func = compile(eq, "temp.py", "eval")
        ErrorLog = eq
        x = 0
        eval(func)
        compiledSuccess = True
    #catches errors to prevent failure, updates compile global flag
    except ZeroDivisionError:
        compiledSuccess = True
    except ValueError:
        compiledSuccess = True
    except SyntaxError:
        compiledSuccess = False
    except NameError:
        compiledSuccess = False
    except TypeError:
        compiledSuccess = False

    #redeclaration of globals
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
    #checks if any inputs have changed, if they have, updates "prev" values and updates graph
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
        #clears axis for update
        ax.cla()

        boundEvalChange = False
        compiledSuccess = False
        eqChange = False

        print("New Function: f(x) = ", eq)
        print("Function or Bounds Changed: Updating Graph...")

        #tries to initialize "Equation" object
        global Y
        try:
            Y = Equation(eq, xmin, xmax, ymin, ymax)
            initializationSuccess = True
        except TypeError:
            initializationSuccess = False
        #if valid function, plots function, deriv, 2nd deriv, and holes, extrema, inflections
        if(initializationSuccess == True):
            #checks global flags for showing functions
            if(showF):fofx, = ax.plot(Y.getDomain(), Y.getYFunction(), "red", label = "Function")
            if (showFPrime):fprimeofx, = ax.plot(Y.getDomain(), Y.getYDeriv(), "blue", label = "First Derivative")
            if (showFDoublePrime):fdoubleprimeofx, = ax.plot(Y.getDomain(), Y.getYSecondDeriv(), "green", label = "Second Derivative")

            fhole = plt.scatter(Y.getHoleCoor()[0], Y.getHoleCoor()[1], s=50, facecolors='none', edgecolors='purple')
            fextrema = plt.scatter(Y.getExtremaCoor()[0], Y.getExtremaCoor()[1], c="blue", s=25)
            finflection = plt.scatter(Y.getInflectionCoor()[0], Y.getInflectionCoor()[1], c="green", s=25)

            #creates legend to explain the colors/symbols
            if(showF and showFPrime and showFDoublePrime):
                plt.legend([fofx, fprimeofx, fdoubleprimeofx, fhole, fextrema, finflection] , ["Function","First Derivative", "Second Derivative", "Holes", "Extrema", "Inflection"], bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)
            else:
                plt.legend([fhole, fextrema, finflection] , ["Holes", "Extrema", "Inflection"], bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)


            #FTC Demonstration
            #integrates from A to B
            global integral
            integral = 0
            integral = Y.integrate(A, B, 1)

            #error handling for invalid integrals
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


            #adds graph styling
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
            plt.xticks(fontsize=TickFontSize, **TickFont)
            plt.yticks(fontsize=TickFontSize, **TickFont)
            plt.xticks(np.arange(xmin, xmax + 1, xScale))
            plt.yticks(np.arange(ymin, ymax + 1, yScale))
            #plt.savefig(eq + ".svg", dpi = 1000)
        #app.getFrame().updateFunction()


#Tkinter GUI
class GraphingCalculator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")

        #creates window title
        tk.Tk.wm_title(self, "Graphing Calculator")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        #grids the container for the rest of the elements
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
    #redeclares global within class
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


    def __init__(self, parent, controller):

        def updateFunction(event):
            #redeclares global with method scope
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
            #tests for change in bounds, if invalid bounds, defaults to 10
            try:
                if (len(xminEntry.get()) > 0):
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

                #checks A & B, defaults to 0
                if (len(AEntry.get()) > 0):
                    A = float(AEntry.get())
                else:
                    A = 0

                if (len(BEntry.get()) > 0):
                    B = float(BEntry.get())
                else:
                    B = 0
                #labels and entry boxes for integral & FTC
                IntegralLabelText = Label(self, text="Integral of f'(x) from A to B =", font=(fontName, fontSize))
                IntegralLabelText.configure(background="white")
                IntegralLabelText.grid(row=9, column=0)

                global integral

                IntegralLabel = Label(self, text=integral, font=(fontName, fontSize))
                IntegralLabel.configure(background="white")
                IntegralLabel.grid(row=9, column=1)

                global FTCL

                FTCLabelText = Label(self, text=FTCL, font=(fontName, fontSize))
                FTCLabelText.configure(background="white")
                FTCLabelText.grid(row=10, column=0)

                global FTC

                FTCLabel = Label(self, text=str(FTC), font=(fontName, fontSize))
                FTCLabel.configure(background="white")
                FTCLabel.grid(row=10, column=1)

            except ValueError:
                print("Check Fields")

        global fontName
        global fontSize

        global eq
        tk.Frame.__init__(self, parent)
        #labels and entry boxes for all other inputs
        #makes function update when pressing enter on any input box
        self.mainTitleText = StringVar()
        self.mainTitleText.set('Graphing Calculator')
        self.mainTitle = Label(self, text=self.mainTitleText.get(), font = (fontName,16))
        self.mainTitle.configure(background = "white")
        self.mainTitle.grid(row=0, columnspan = 2)

        global e1
        e1 = Entry(self)
        e1.configure(background = "#E0E0E0")
        e1.grid(row=2, column=1)
        e1.bind('<Return>',updateFunction)

        EquationLabel = Label(self, text="f(x) =", font = (fontName,fontSize))
        EquationLabel.configure(background = "white")
        EquationLabel.grid(row=2, column=0)

        global xminEntry
        xminEntry = Entry(self)
        xminEntry.configure(background = "#E0E0E0")
        xminEntry.grid(row=3, column=1)
        xminEntry.bind('<Return>',updateFunction)

        xminLabel = Label(self, text="Xmin:", font = (fontName,fontSize))
        xminLabel.configure(background = "white")
        xminLabel.grid(row=3, column=0)

        global xmaxEntry
        xmaxEntry = Entry(self)
        xmaxEntry.configure(background = "#E0E0E0")
        xmaxEntry.grid(row=4, column=1)
        xmaxEntry.bind('<Return>',updateFunction)

        xmaxLabel = Label(self, text="Xmax:", font = (fontName,fontSize))
        xmaxLabel.configure(background = "white")
        xmaxLabel.grid(row=4, column=0)

        global yminEntry
        yminEntry = Entry(self)
        yminEntry.configure(background = "#E0E0E0")
        yminEntry.grid(row=5, column=1)
        yminEntry.bind('<Return>',updateFunction)

        yminLabel = Label(self, text="Ymin:", font = (fontName,fontSize))
        yminLabel.configure(background = "white")
        yminLabel.grid(row=5, column=0)

        global ymaxEntry
        ymaxEntry = Entry(self)
        ymaxEntry.configure(background = "#E0E0E0")
        ymaxEntry.grid(row=6, column=1)
        ymaxEntry.bind('<Return>',updateFunction)

        ymaxLabel = Label(self, text="Ymax:", font = (fontName,fontSize))
        ymaxLabel.configure(background = "white")
        ymaxLabel.grid(row=6, column=0)

        global AEntry
        AEntry = Entry(self)
        AEntry.configure(background = "#E0E0E0")
        AEntry.grid(row=7, column=1)
        AEntry.bind('<Return>',updateFunction)

        ALabel = Label(self, text="Lower Limit (A):", font = (fontName,fontSize))
        ALabel.configure(background = "white")
        ALabel.grid(row=7, column=0)

        global BEntry
        BEntry = Entry(self)
        BEntry.configure(background = "#E0E0E0")
        BEntry.grid(row=8, column=1)
        BEntry.bind('<Return>',updateFunction)

        BLabel = Label(self, text="Upper Limit (B):", font = (fontName,fontSize))
        BLabel.configure(background = "white")
        BLabel.grid(row=8, column=0)

        graphingFrame = Frame(self)
        canvas = FigureCanvasTkAgg(fig, graphingFrame)

        nameLabel = Label(self, text="Created by Saketh Kollu and Akshay Heda (P.3)", font = (fontName,fontSize))
        nameLabel.configure(background="white")
        nameLabel.grid(row=11, columnspan = 2)

        githubLabel = Label(self, text="https://github.com/akshayheda/graphingCalculator", font=(fontName, fontSize -2))
        githubLabel.configure(background="white")
        githubLabel.grid(row=12, columnspan=2)

        canvas.show()
        canvas.get_tk_widget().grid(row=1)

        canvas._tkcanvas.grid(row=2)
        graphingFrame.grid(row =1, columnspan=2, sticky=W)




#creates the page, checking for changes every 250ms
app = GraphingCalculator()
ani = animation.FuncAnimation(fig, animate, interval=250)

app.mainloop()
