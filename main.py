from __future__ import division
import matplotlib.pyplot as tg
from sympy.parsing.sympy_parser import *
from sympy import *
import parser
import math



Xmin = -10
Xmax = 10
Ymin = -10
Ymax = 10
resolution = 0.001

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


    for x in my_range(Xmin, Xmax, resolution):
        x_values.append(x)

    counter = 0
    print("Generated x values successfully")



    while(counter < len(x_values)):
        x = x_values[counter]
        y_values.append(eval(code))
        #print(y_values[counter])
        print(str(x_values[counter])+ " , " + str(y_values[counter]))


        counter = counter + 1
    print("Generated y values successfully")



#def evaluate(f,value):
    #x, y, z, t = symbols('x y z t')


    #return N(f.subs(x,value))
    #return f.subs(x, value)

def graph():
    tg.plot(x_values, y_values)
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