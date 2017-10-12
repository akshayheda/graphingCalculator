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
resolution = ((Xmax - Xmin)/20000)
input = ""



def compileExpression(expr):

    print("Expression to be compiled: " + expr)
    return compile(expr, "temp.py", "eval")

def preParseString(expr):
    print(expr)

    expr = expr.lower()
    expr = expr.replace("^", "**")
    expr = expr.replace("sec(", "(1)/cos(")
    expr = expr.replace("csc(", "(1)/sin(")
    expr = expr.replace("cot(", "(1)/tan(")

    print(expr)

    return expr

#steps through all values in the range using a resolution
def valueGenerator(xmin, xmax, resolution):
    while xmin <= xmax:
        yield xmin
        xmin += resolution

#generates all the X values that will be evaluated
def domainGeneration():
    x_val = []
    for x in valueGenerator(Xmin, Xmax, resolution):
        #floats are unable to be exactly zero, so we set it equal to zero if it is really close to zero
        if(abs(x) <= 1e-11):
            x_val.append(0.0)
        #all x values are rounded to 3 digits to reduce float error
        else:
            x_val.append( round(x, 3) )
    return x_val

#evaluates all x values for the function, derivative, or second derivative
#@param Function: the y function being evaluated
#@param Domain: the array of X values to evaluate
#@param level: can be 0 for function, 1 for derivative, or 2 for second derivative
def generateFunction(Function, Domain, level):
    yvals = []
    if(level == 0):
        for i in Domain:
            yvals.append(evaluate(i, Function))
    if(level == 1):
        for i in Domain:
            yvals.append(deriv(i, Function))
    if(level == 2):
        for i in Domain:
            yvals.append(secondDeriv(i, Function))
    return yvals

#evaluates the function at a given x value
def evaluate(xval, yfunction):
    x = xval
    try:
        y = eval(yfunction)
    #error handling for invalid evaluation
    except ValueError:
        y=np.nan
    #error handling for divide by zero errors
    except ZeroDivisionError:
        y=np.nan
    #error handling for complex numbers
    if (np.iscomplex(y)):
        y = (np.nan)
    #error handling for float error - if a value is below the bound, it is set to zero
    if (abs(y) < 1e-9):
        y = 0
    return y


#derivative evaluation using a difference quotient
def deriv(xval, yfunction):
    #the difference between the two points being evaluated
    h = 0.0001
    y2 = evaluate(xval+h, yfunction)
    y1 = evaluate(xval-h, yfunction)
    #If function is undefined at the point, then the derivative is undefined
    if(y1==nan or y2 == nan):
        deriv = np.nan
    #derivative is the slope between two points that are very close to each other
    else:
        deriv = (y2-y1)/ (2*h)
    #error handling for values close to zero being set equal to zero
    if (abs(deriv) <= 1e-9):
        deriv = 0
    return deriv

def secondDeriv(xval, yfunction):
    # the difference between the two points being evaluated
    h = 0.0001
    y2 = deriv(xval+h, yfunction)
    y1 = deriv(xval-h, yfunction)
    # If derivative is undefined at the point, then the second derivative is undefined
    if(y1==nan or y2 == nan):
        secondDeriv = np.nan
    else:
        secondDeriv = (y2-y1)/ (2*h)
    # error handling for values close to zero being set equal to zero. This is a larger bound than earlier as error accumulates.
    if (abs(secondDeriv) <= 5e-8 ):
        secondDeriv = 0
    return secondDeriv

#Uses Simpson's 3/8th rule for precise integral estimation
def Integrate(UpperBound, LowerBound, yFunc):
    lbEval = deriv(LowerBound, yFunc)
    ubEval = deriv(UpperBound, yFunc)
    TwoLEval = 3 * deriv( ((2*LowerBound) + UpperBound) / 3, yFunc)
    TwoUEval = 3 * deriv(( (LowerBound + (2 * UpperBound)) / 3 ) , yFunc)

    Integral = ((UpperBound - LowerBound) / 8 ) * ( lbEval +  TwoLEval   +  TwoUEval  + ubEval )
    return Integral

def compileHoles(Domain, yvals):
    HoleX = []
    HoleY = []
    HoleCoor = [HoleX, HoleY]
    #Iterate through each y value, excluding the first and last y value to prevent index errors
    for i in range(1, len(Domain)-1):
        #checks if y value is undefined
        if math.isnan(yvals[i]):
            yPrev = yvals[i - 1]
            yNext = yvals[i + 1]
            #if y value is undefined, checks if previous and next value are undefined as well
            if(not(math.isnan(yPrev)) and not(math.isnan(yNext))):
                # if they are not undefined, then there is a hole
                HoleX.append(Domain[i])
                #approximate the y value of the hole by taking average of previous and next y value
                HoleY.append((yPrev + yNext) /2)
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

                return InflectionCoor

            if((y_prev > 0 and y_next < 0) or (y_prev < 0 and y_next > 0) ):

                InflectionX.append(x)
                InflectionY.append(evaluate(x, yFunction))



        counter += 1
    return InflectionCoor

