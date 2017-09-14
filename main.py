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

y1 ="tan(pi * x)"
ast = parser.expr(y1)
code = ast.compile()

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

    counter = 0


    expr = compile("tan(x * pi)", "tmp.py", "eval")

    for i in my_range(Xmin, Xmax, resolution):
        x = i
        test = eval(expr)

        if ((abs(test) > 10)):
            y_values.append(np.nan)
        else:
            y_values.append(test)


        print(str(x) + " , " + str(test))

    '''
    
    while(counter < len(x_values)):
        x = x_values[counter]

        ymax = Ymax

        y_eval = eval(code)
        ycurrent = np.float64(y_eval)

        if ((abs(y_eval) > ymax)):
            y_values.append(np.nan)
        else:
            y_values.append(y_eval)
            y_eval_previous = y_values

        #if( (abs(y_eval) > ymax) ):
        #    y_values.append(np.nan)
        #else:
        #    y_values.append(y_eval)
        #   y_eval_previous = y_values



        #print(y_values[counter])
        print(str(counter) + " : " + str(x_values[counter])+ " , " + str(y_values[counter]))


        counter = counter + 1
    
    '''

    PlotTimeEnd = timeit.default_timer()
    print("Generated y values successfully")
    print("Initial Function Generation Time: " + str(PlotTimeEnd - PlotTimeStart) + " seconds")



#def evaluate(f,value):
    #x, y, z, t = symbols('x y z t')


    #return N(f.subs(x,value))
    #return f.subs(x, value)

def derivative(x_values, y_values):
    y_deriv=[]

    counter = 0
    FirstDerivativeTimeStart = timeit.default_timer()
    while(counter < len(x_values)):
        x1 = x_values[counter]
        y1 = y_values[counter]

        x = x1 + 0.001
        y2 = eval(code)
        x2 = x1 + 0.001

        slope = (y2 - y1) / (x2- x1)

        y_deriv.append(slope)
        counter = counter + 1
    FirstDerivativeTimeEnd = timeit.default_timer()
    print("Generated first derivative successfully")
    print("First Derivative Generation Time: " + str( FirstDerivativeTimeEnd - FirstDerivativeTimeStart ) + " seconds")

    return y_deriv

def secondDerivative(x_values, y_prime_values):
    SecondDerivativeTimeStart = timeit.default_timer()

    y_second_deriv=[]

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
    print("Second Derivative Generation Time: " + str(SecondDerivativeTimeEnd - SecondDerivativeTimeStart) + " seconds")

        #print(str(counter) + " : " + str(x_values[counter]) + " , " + str(y_second_deriv[counter]))
    return y_second_deriv



def graph(x,y, color):

    tg.plot(x, y,color)
    #tg.plot(x_values[1001:1999], y_values[1001:1999],'-b')

    #fig = tg.figure()
    #ax = fig.add_subplot(111)
    #ax.plot(x, y)

    # using 'spines', new in Matplotlib 1.0
    #ax.spines['left'].set_position('zero')
    #ax.spines['right'].set_color('none')
    #ax.spines['bottom'].set_position('zero')
    #ax.spines['top'].set_color('none')
    #ax.spines['left'].set_smart_bounds(True)
    #ax.spines['bottom'].set_smart_bounds(True)
    #ax.xaxis.set_ticks_position('bottom')
    #ax.yaxis.set_ticks_position('left')

    tg.ylim([Ymin, Ymax])
    #tg.show()


def main():
    start = timeit.default_timer()

    #y1 = input("Enter a function: ")

    #a = sympify(y1)

    #x, y, z, t = symbols('x y z t')



    #x = 0
    #print(eval(code))


    generateXValues()
    generateYValues()
    graph(x_values, y_values, '-r')
    graph(x_values, derivative(x_values, y_values), '-b')
    graph(x_values, secondDerivative(x_values, derivative(x_values, y_values)), '-g')

    stop = timeit.default_timer()

    print("Total Run time: " + str(stop - start) + " seconds")

    tg.show()







if __name__ == "__main__":
    main()    