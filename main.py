from __future__ import division
import matplotlib.pyplot as tg
from sympy.parsing.sympy_parser import *
from sympy import *



Xmin = -10
Xmax = 10
Ymin = -10
Ymax = 10
resolution = 0.1

x_values=[]
y_values=[]

y1 ="((x -2) * (x-3 ))/ (x-2)"

def my_range(start, end, step):
    while start <= end:
        yield start
        start += step
    print("Generating range")


def generatePoints(a):


    for x in my_range(Xmin, Xmax, resolution):
        x_values.append(x)

    counter = 0
    print("Generated x values successfully")



    while(counter < len(x_values)):

        y_values.append(evaluate(a,x_values[counter]))
        #print(y_values[counter])

        counter = counter + 1
    print("Generated y values successfully")


def evaluate(f,value):
    x, y, z, t = symbols('x y z t')


    return N(f.subs(x,value))
    #return f.subs(x, value)

def graph():

    tg.plot(x_values, y_values)


    tg.show()

def main():

    #y1 = input("Enter a function: ")

    #a = sympify(y1)

    x, y, z, t = symbols('x y z t')

    a = parse_expr(y1)

    print(evaluate(a, 2))


    generatePoints(a)
    graph()

if __name__ == "__main__":
    main()