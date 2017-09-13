from __future__ import division
import matplotlib.pyplot as tg
from sympy.parsing.sympy_parser import *
from sympy import *
import parser
import numpy as np
from decimal import *
import math



Xmin = -10
Xmax = 10
Ymin = -10
Ymax = 10
resolution = np.float128(0.01)


x_values=[]
y_values=[]

y1 ="1/x"
ast = parser.expr(y1)
code = ast.compile()

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step
    print("Generating range")


def generatePoints(a):

    i = 0

    for x in my_range(Xmin, Xmax, resolution):
        x_values.append(x)
        print(x_values[i])
        i = i + 1
    counter = 0
    print("Generated x values successfully")



    while(counter < len(x_values)):
        x = x_values[counter]

        ymax = 10000000000000000

        y_eval = eval(code)
        if(y_eval > ymax):
            y_values.append("NaN")

        y_values.append(eval(code))
        #print(y_values[counter])
        print(str(counter) + " : " + str(x_values[counter])+ " , " + str(y_values[counter]))


        counter = counter + 1
    print("Generated y values successfully")



#def evaluate(f,value):
    #x, y, z, t = symbols('x y z t')


    #return N(f.subs(x,value))
    #return f.subs(x, value)

def graph():

    tg.plot(x_values[0:999], y_values[0:999],'-b')
    tg.plot(x_values[1001:1999], y_values[1001:1999],'-b')
    tg.show()

def main():

    #y1 = input("Enter a function: ")

    #a = sympify(y1)

    x, y, z, t = symbols('x y z t')

    a = parse_expr(y1)

    #x = 0
    #print(eval(code))



    generatePoints(a)
    graph()


if __name__ == "__main__":
    main()