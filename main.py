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
import math


Xmin = -10
Xmax = 10
Ymin = -10
Ymax = 10
resolution = 0.001

Upper = 100
Lower = 25

isRational = False

x_values=[]
y1 ="log(x,e)"


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
        if(abs(x) <= 1e-11):
            x_val.append(0.0)
        else:
            x_val.append( round(x, 3) )
    return x_val
    #print("Generated x values successfully")

def genF(Function, Domain):
    y = []

    PlotTimeStart = timeit.default_timer()

    counter = 0
    for i in Domain:
        x = i
        y_val = evaluate(x, Function)

        if(y_val > Ymax or y_val < Ymin):
            y.append(np.nan)
        else:
            y.append(y_val)

        #print("X: " + str(i) + " Y: " + str(y[counter]))
        counter += 1

    PlotTimeEnd = timeit.default_timer()

    print("Generated function values successfully")
    print("Function Generation Time: " + str(PlotTimeEnd - PlotTimeStart) + " seconds" + "\n")

    return y

def genFPrime(Function, Domain):

    firstDeriv = []

    counter = 0
    FirstDerivativeTimeStart = timeit.default_timer()
    for i in Domain:
        x = i

        yDeriv = deriv(x, Function)



        if (yDeriv > Ymax or yDeriv < Ymin):
            firstDeriv.append(np.nan)
        else:
            firstDeriv.append(yDeriv)

    FirstDerivativeTimeEnd = timeit.default_timer()
    print("Generated first derivative successfully")
    print("First Derivative Generation Time: " + str( FirstDerivativeTimeEnd - FirstDerivativeTimeStart ) + " seconds" + "\n")

    return firstDeriv

def genFDoublePrime(Function, Domain):

    y2ndDeriv = []

    SecondDerivativeTimeStart = timeit.default_timer()

    for i in Domain:
        x = i

        y2Deriv = secondDeriv(x, Function)

        if (y2Deriv > Ymax or y2Deriv < Ymin):
            y2ndDeriv.append(np.nan)
        else:
            y2ndDeriv.append(y2Deriv)



    SecondDerivativeTimeEnd = timeit.default_timer()

    print("Generated second derivative successfully")
    print("Second Derivative Generation Time: " + str(SecondDerivativeTimeEnd - SecondDerivativeTimeStart) + " seconds" + "\n")

    return y2ndDeriv

def plotToGraph(x,y, color):
    print("Plotting Points...")
    PlotTimeStart = timeit.default_timer()

    tg.plot(x, y, color)

    PlotTimeEnd = timeit.default_timer()

    print("Points Successfully Plotted")
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
    h = 0.0001
    y2 = evaluate(xval+h, yfunction)
    y1 = evaluate(xval-h, yfunction)

    if(y1==nan or y2 == nan):
        deriv = np.nan
    else:
        deriv = (y2-y1)/ (2*h)
    if (abs(deriv) <= 1e-9):
        deriv = 0
    return deriv

def secondDeriv(xval, yfunction):
    h = 0.0001
    y2 = deriv(xval+h, yfunction)
    y1 = deriv(xval-h, yfunction)

    if(y1==nan or y2 == nan):
        secondDeriv = np.nan
    else:
        secondDeriv = (y2-y1)/ (2*h)
    if (abs(secondDeriv) <= 5e-8 ):
        secondDeriv = 0
    #print("x: " + str(xval) + " y: " + str(secondDeriv))
    return secondDeriv

def Integrate(UpperBound, LowerBound, yFunc):

    lbEval = deriv(LowerBound, yFunc)
    ubEval = deriv(UpperBound, yFunc)
    TwoLEval = 3 * deriv( ((2*LowerBound) + UpperBound) / 3, yFunc)
    TwoUEval = 3 * deriv(( (LowerBound + (2 * UpperBound)) / 3 ) , yFunc)

    Integral = ((UpperBound - LowerBound) / 8 ) * ( lbEval +  TwoLEval   +  TwoUEval  + ubEval )
    return Integral

def compileHoles(Domain, yvals, yFunction):

    HoleX = []
    HoleY = []
    HoleCoor = [HoleX, HoleY]

    counter = 0
    for x in Domain:
        if(x != (Xmin or Xmax)):

            y = evaluate(x, yFunction)

            if (math.isnan(y)):

                yPrev = yvals[counter - 1]
                yNext = yvals[counter + 1]

                if(not(math.isnan(yPrev)) and not(math.isnan(yNext))):
                    HoleX.append(Domain[counter])
                    HoleY.append((yPrev + yNext) /2)


                    plotDot(Domain[counter], (yPrev + yNext) /2, "orange")

        counter +=1
    return HoleCoor

def findZeroes(Domain, yvals):
    Zeroes = []
    i = 0

    for y in yvals:

        yCurrent = y
        yPrev = yCurrent
        if(i > 0):
            yPrev = yvals[i-1]

        if((yCurrent < 0 and yPrev > 0) or (yCurrent > 0 and yPrev < 0) or ( abs(yCurrent) < 1e-9) or (abs(yCurrent) == 0) ):
            Zeroes.append(Domain[i] )

        i+=1

    return Zeroes

def findExtrema(Zeroes, yFunction):
    ExtremaX = []
    ExtremaY = []
    ExtremaCoor = [ExtremaX, ExtremaY]

    counter = 0
    for x in Zeroes:

        if(x != (Xmin or Xmax)):

            y_prev = deriv(x-0.001, yFunction)

            y_next = deriv(x+0.001, yFunction)


            if((y_prev > 0 and y_next < 0) or (y_prev < 0 and y_next > 0)):

                ExtremaX.append(x)
                ExtremaY.append(evaluate(x, yFunction))
                plotDot(x,evaluate(x, yFunction) ,"red")

        counter += 1
    return ExtremaCoor

def findInflection(FPrimeZeroes, yFunction):
    InflectionX = []
    InflectionY = []
    InflectionCoor = [InflectionX, InflectionY]

    counter = 0
    for x in FPrimeZeroes:

        if(x != (Xmin or Xmax)):

            y_prev = secondDeriv(x-0.001, yFunction)
            #print("prev" + str(y_prev))
            y_next = secondDeriv(x+0.001, yFunction)
            #print("next" + str(y_next))

            if( (y_prev and y_next) == 0):
                print("f'(x) is ZERO for all X")
                return InflectionCoor

            if((y_prev > 0 and y_next < 0) or (y_prev < 0 and y_next > 0) ):

                InflectionX.append(x)
                InflectionY.append(evaluate(x, yFunction))
                plotDot(x, evaluate(x, yFunction), "green")


        counter += 1
    return InflectionCoor


def plotDot(x,y,color):

    tg.scatter(x, y,c=color, s=100)

def preParseString(expr):
    print(expr)

    expr = expr.lower()
    expr = expr.replace("^", "**")
    expr = expr.replace("sec(", "(1)/cos(")
    expr = expr.replace("csc(", "(1)/sin(")
    expr = expr.replace("cot(", "(1)/tan(")

    print(expr)

    return expr

def main():
    Integrate = False
    get = input("f(x) = ")

    get = preParseString(get)

    y1COMPILED = compileExpression(get)

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

    print("Basic properties evaluated successfully" + "\n")

    if(Integrate == True):
        print("f(x) = " + get)

        print("Definite integral approximated using Simpson's 3/8 rule...")

        print("b = " + str(Upper))
        print("a = " + str(Lower))
        print("f(b) - f(a) = " + str(evaluate(Upper,y1COMPILED) - evaluate(Lower,y1COMPILED)))
        print( "Integral of f'(x) from a to b = " + str(Integrate(Upper,Lower,y1COMPILED)))

    compileHoles(x_values, y_values,y1COMPILED)

    print("Zeroes of f(x): " + str(findZeroes(x_values,y_values)))
    print("Zeroes of f'(x): " + str(findZeroes(x_values, y_deriv)))
    print("Zeroes of f''(x): " + str(findZeroes(x_values, y_second_deriv)))

    findExtrema(findZeroes(x_values, y_deriv), y1COMPILED)
    findInflection(findZeroes(x_values, y_second_deriv), y1COMPILED)

    print("Relative Extrema: Red Dot | Inflection Point: Green Dot")

    stop = timeit.default_timer()

    print("Total Run time: " + str(stop - start) + " seconds")

    showGraph()

if __name__ == "__main__":
    main()    