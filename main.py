from __future__ import division
import matplotlib.pyplot as tg
from sympy.parsing.sympy_parser import *
from sympy import *
from parser import *
import numpy as np
import seaborn
from decimal import *
from math import *

import timeit

x, y, z, t = symbols('x y z t')


Xmin = -10
Xmax = 10
Ymin = -10
Ymax = 10
resolution = 0.001

isRational = False

x_values=[]
y_values=[]
y_deriv=[]
y_second_deriv=[]

y1 ="(3/4)*x**(4/3)"
num = ""
denom = ""


#expr = compile(y1, "tmp.py", "eval")

def compileExpression(expr):
    print("Expression to be compiled: " + expr)
    return compile(expr, "temp.py", "eval")

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step
    print("Generating domain")

def generateXValues():

    x_val = []

    for x in my_range(Xmin, Xmax, resolution):
        x_val.append(x)
        #print(x_values[i])
    return x_val
    print("Generated x values successfully")

def genF(Function, Domain):
    y = []
    for i in Domain:
        x = i
        y.append(evaluate(x, Function))


def generateYValues(CompiledFunction):
    #Start time

    PlotTimeStart = timeit.default_timer()

    y = []


    for i in my_range(Xmin, Xmax, resolution):
        x = i
        try:

            test = eval(CompiledFunction)

        except ValueError:
            test = Ymax + 1

        if ((abs(test) > Ymax) or np.iscomplex(test)):
            y.append(np.nan)
        else:
            y.append(test)


        print(str(x) + " , " + str(test))


    PlotTimeEnd = timeit.default_timer()
    print("Generated y values successfully")
    print("Initial Function Generation Time: " + str(PlotTimeEnd - PlotTimeStart) + " seconds" + "\n")

    return y





def derivative(x_values, y_values,Function):

    counter = 0
    FirstDerivativeTimeStart = timeit.default_timer()
    while(counter < len(x_values)):
        x1 = x_values[counter]
        y1 = y_values[counter]

        x = x1 + 0.001
        y2 = 0
        try:

            y2 = eval(Function)

        except ValueError:
            y2 = np.nan




        x2 = x1 + 0.001

        slope = (y2 - y1) / (x2- x1)

        y_deriv.append(slope)
        counter = counter + 1

    FirstDerivativeTimeEnd = timeit.default_timer()
    print("Generated first derivative successfully")
    print("First Derivative Generation Time: " + str( FirstDerivativeTimeEnd - FirstDerivativeTimeStart ) + " seconds" + "\n")

    return y_deriv

def secondDerivative(x_values, y_prime_values):
    SecondDerivativeTimeStart = timeit.default_timer()

    ymax = Ymax

    counter = 0

    while(counter < len(x_values)):
        x1 = x_values[counter]
        y1 = y_prime_values[counter]

        x = x1 + 0.001
        y2 = y_prime_values[counter - 1]
        x2 = x1 - 0.001

        slope = (y2 - y1) / (x2- x1)

        if ((abs(slope) > ymax)):
            y_second_deriv.append(np.nan)
        else:
            y_second_deriv.append(slope)
        counter = counter + 1

    SecondDerivativeTimeEnd = timeit.default_timer()

    print("Generated second derivative successfully")
    print("Second Derivative Generation Time: " + str(SecondDerivativeTimeEnd - SecondDerivativeTimeStart) + " seconds" + "\n")

        #print(str(counter) + " : " + str(x_values[counter]) + " , " + str(y_second_deriv[counter]))
    return y_second_deriv

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


def findDomainRestrictions(y_vals):
    print("Now searching for domain restrictions")

    domainRestrictions = []

    domainRestrictions = findZeroes(y_vals)



    return domainRestrictions

def findZeroes(y_vals):
    zeroes = []

    tolerance = 0
    counter = 0

    for y in y_vals:
        if( y == -1.0259154636926837e-13  ):
            print(counter)
            zeroes.append(x_values[counter])

        counter += 1



    return zeroes


def plotToGraph(x,y, color):

    tg.plot(x, y,color)

    tg.ylim([Ymin, Ymax])

def showGraph():

    tg.show()

def evaluate(xval, yfunction):
    x = xval
    try:
        y = eval(yfunction);
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

    print("y2: " + str(y2))
    print("y1: " + str(y1))
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

    print("y2: " + str(y2))
    print("y1: " + str(y1))
    if(y1==nan or y2 == nan):
        secondDeriv = np.nan
    else:
        secondDeriv = (y2-y1)/ (2*h)
    if (abs(secondDeriv) < 1e-9):
        secondDeriv = 0
    return secondDeriv

def main():
    y1COMPILED = compileExpression(y1)


    #y1SYMPY = parse_expr(y1)


    print(evaluate(0, y1COMPILED))
    print(deriv(0,y1COMPILED))
    print(secondDeriv(0,y1COMPILED))

    start = timeit.default_timer()

    #x_values = generateXValues()
    #y_values = generateYValues(y1COMPILED)


    #plotToGraph(x_values, y_values, '-r')
    #plotToGraph(x_values, derivative(x_values, y_values, y1COMPILED), '-b')
    #plotToGraph(x_values, secondDerivative(x_values, y_deriv), '-g')

    print("Basic properties evaluated successfully")

    #splitFunction(y1)
    if (1 == 0):
        print("Function is rational")

        denomCOMPILED = compile(denom, "tmp.py", "eval")
        print("Successfully Compiled Denominator")
        denomY = generateYValues(denomCOMPILED)
        print(denomY)
        #print(findDomainRestrictions(denomY))




    #print("Zeroes: " + str(findZeroes(y_values)) )

    stop = timeit.default_timer()

    print("Total Run time: " + str(stop - start) + " seconds")

    print("f(x) = " + y1)


    showGraph()







if __name__ == "__main__":
    main()    