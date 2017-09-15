from __future__ import division
import matplotlib.pyplot as tg
from sympy.parsing.sympy_parser import *
import parser
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


x_values=[]
y_values=[]
y_deriv=[]
y_second_deriv=[]

y1 ="sin(x) +x"
expr = compile(y1, "tmp.py", "eval")


def my_range(start, end, step):
    while start <= end:
        yield start
        start += step
    print("Generating range")

def generateXValues():
    for x in my_range(Xmin, Xmax, resolution):
        x_values.append(x)
        #print(x_values[i])

    print("Generated x values successfully")

def generateYValues():
    #Start timer
    PlotTimeStart = timeit.default_timer()



    for i in my_range(Xmin, Xmax, resolution):
        x = i
        test = eval(expr)

        if ((abs(test) > 10)):
            y_values.append(np.nan)
        else:
            y_values.append(test)


        print(str(x) + " , " + str(test))


    PlotTimeEnd = timeit.default_timer()
    print("Generated y values successfully")
    print("Initial Function Generation Time: " + str(PlotTimeEnd - PlotTimeStart) + " seconds" + "\n")



def derivative(x_values, y_values):

    counter = 0
    FirstDerivativeTimeStart = timeit.default_timer()
    while(counter < len(x_values)):
        x1 = x_values[counter]
        y1 = y_values[counter]

        x = x1 + 0.001
        y2 = eval(expr)
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

    ymax = 10000

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

def findZeroes(y_values):
    zeroes = []

    tolerance = 0
    counter = 0

    for y in y_values:
        if( y == -1.0259154636926837e-13  ):
            zeroes.append(x_values[counter])
        counter += 1



    return zeroes


def plotToGraph(x,y, color):

    tg.plot(x, y,color)

    tg.ylim([Ymin, Ymax])

def showGraph():

    tg.show()

def main():

    start = timeit.default_timer()

    generateXValues()
    generateYValues()
    plotToGraph(x_values, y_values, '-r')
    plotToGraph(x_values, derivative(x_values, y_values), '-b')
    plotToGraph(x_values, secondDerivative(x_values, y_deriv), '-g')

    #print(findZeroes(y_values))

    stop = timeit.default_timer()

    print("Total Run time: " + str(stop - start) + " seconds")

    print("f(x) = " + y1)
    showGraph()







if __name__ == "__main__":
    main()    