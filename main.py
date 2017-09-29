from __future__ import division
import matplotlib.pyplot as tg
from sympy.parsing.sympy_parser import *
#from sympy import *
from parser import *
import numpy as np
import seaborn
from decimal import *
from math import *
import timeit




Xmin = -10
Xmax = 10
Ymin = -10
Ymax = 10
resolution = 0.001

isRational = False

x_values=[]



y1 ="sin(x)/x"
Function = ""
num = ""
denom = ""

def compileExpression(expr):
    print("Expression to be compiled: " + expr)
    return compile(expr, "temp.py", "eval")

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

def generateXValues():

    x_val = []

    for x in my_range(Xmin, Xmax, resolution):
        x_val.append(x)
    return x_val
    print("Generated x values successfully")

def genF(Function, Domain):
    y = []

    PlotTimeStart = timeit.default_timer()

    for i in my_range(Xmin, Xmax, resolution):
        x = i
        y.append(evaluate(x, Function))

    PlotTimeEnd = timeit.default_timer()

    print("Generated function values successfully")
    print("Function Generation Time: " + str(PlotTimeEnd - PlotTimeStart) + " seconds" + "\n")

    return y

def genFPrime(Function, Domain):

    firstDeriv = []

    counter = 0
    FirstDerivativeTimeStart = timeit.default_timer()
    for i in my_range(Xmin, Xmax, resolution):
        x = i
        firstDeriv.append(deriv(x, Function))

    FirstDerivativeTimeEnd = timeit.default_timer()
    print("Generated first derivative successfully")
    print("First Derivative Generation Time: " + str( FirstDerivativeTimeEnd - FirstDerivativeTimeStart ) + " seconds" + "\n")

    return firstDeriv

def genFDoublePrime(Function, Domain):

    y2ndDeriv = []

    SecondDerivativeTimeStart = timeit.default_timer()

    for i in my_range(Xmin, Xmax, resolution):
        x = i
        y2ndDeriv.append(secondDeriv(x, Function))

    SecondDerivativeTimeEnd = timeit.default_timer()

    print("Generated second derivative successfully")
    print("Second Derivative Generation Time: " + str(SecondDerivativeTimeEnd - SecondDerivativeTimeStart) + " seconds" + "\n")

    return y2ndDeriv


def splitFunction(StringFunction):
    index = 0

    numerator = StringFunction
    denominator = 1


    for c in y1:
        if(c == "/"):
            isRational = True
            numerator = StringFunction[0:index]
            denominator = StringFunction[index + 1:len(y1)]
        index+=1

    num = numerator
    denom = denominator

    print("Numerator: " + num + " Denominator: " + denom)

def plotToGraph(x,y, color):
    print("Plotting Points...")
    PlotTimeStart = timeit.default_timer()

    tg.plot(x, y, color)

    PlotTimeEnd = timeit.default_timer()

    print("Plotting Points")
    print("Plot Generation Time: " + str(PlotTimeEnd - PlotTimeStart) + " seconds" + "\n")



    tg.ylim([Ymin, Ymax])

def showGraph():

    tg.show()

def evaluate(xval, yfunction):
    x = xval
    try:
        y = eval(yfunction)
    except ValueError:
        y=np.nan
    except ZeroDivisionError:
        y=np.nan

    if (np.iscomplex(y)):
        y = (np.nan)
    if (abs(y) < 1e-9):
        y = 0
    return y

def deriv(xval, yfunction):
    h = 0.001
    y2 = evaluate(xval+h, yfunction)
    y1 = evaluate(xval-h, yfunction)

    if(y1==nan or y2 == nan):
        deriv = np.nan
    else:
        deriv = (y2-y1)/ (2*h)
    if (abs(deriv) < 1e-9):
        deriv = 0
    return deriv

def secondDeriv(xval, yfunction):
    h = 0.001
    y2 = deriv(xval+h, yfunction)
    y1 = deriv(xval-h, yfunction)

    if(y1==nan or y2 == nan):
        secondDeriv = np.nan
    else:
        secondDeriv = (y2-y1)/ (2*h)
    if (abs(secondDeriv) < 1e-9):
        secondDeriv = 0
    return secondDeriv

def Integrate(UpperBound, LowerBound, yFunction):

    Integral = ((UpperBound - LowerBound) / 8 )*()



def main():
    y1COMPILED = compileExpression(y1)

    start = timeit.default_timer()

    #Generate the domain
    x_values = generateXValues()

    #Generate the y values
    y_values = genF(y1COMPILED, x_values)

    #Generate the first derivative
    y_deriv = genFPrime(y1COMPILED, x_values)

    #Generate the second derivative
    y_second_deriv = genFDoublePrime(y1COMPILED, x_values)

    plotToGraph(x_values, y_values, '-r')
    plotToGraph(x_values, y_deriv, '-b')
    plotToGraph(x_values, y_second_deriv, '-g')

    print("Basic properties evaluated successfully")

    stop = timeit.default_timer()

    print("Total Run time: " + str(stop - start) + " seconds")

    print("f(x) = " + y1)

    print(evaluate(0,y1COMPILED))

    showGraph()

if __name__ == "__main__":
    main()    