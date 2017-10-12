from __future__ import division
import numpy as np
from math import *
import math


class Equation:

    def __init__(self, Expression = "", Xmin = -10, Xmax = 10, resolution = -1 ):
        self.Xmin = Xmin
        self.Xmax = Xmax
        if(resolution == -1):
            self.resolution = ((Xmax - Xmin) / 20000)
        else:
            self.resolution = resolution
        self.Expression = Expression
        self.preParseString()
        self.CompiledExpression = self.compileExpression()

        self.Domain = self.domainGeneration()

        self.YFunction = self.generateFunction(0)
        self.YDeriv = self.generateFunction(1)
        self.YSecondDeriv = self.generateFunction(2)

        self.Zeroes = self.findZeroes()
        self.FPrimeZeroes = self.findZeroes


    def compileExpression(self):
        return compile(self.Expression, "temp.py", "eval")

    def preParseString(self):

        self.Expression = self.Expression.lower()
        self.Expression = self.Expression.replace("^", "**")
        self.Expression = self.Expression.replace("sec(", "(1)/cos(")
        self.Expression = self.Expression.replace("csc(", "(1)/sin(")
        self.Expression = self.Expression.replace("cot(", "(1)/tan(")


    #steps through all values in the range using a resolution

    def valueGenerator(self):
        i = self.Xmin
        while i <= self.Xmax:


            yield i
            i += self.resolution

    #generates all the X values that will be evaluated

    def domainGeneration(self):
        x_val = []
        for x in self.valueGenerator():
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
    def generateFunction(self, level):
        yvals = []
        if(level == 0):
            for i in self.Domain:
                yvals.append(self.evaluate(i))
        if(level == 1):
            for i in self.Domain:
                yvals.append(self.deriv(i))
        if(level == 2):
            for i in self.Domain:
                yvals.append(self.secondDeriv(i))
        return yvals

    #evaluates the function at a given x value
    def evaluate(self, xval):
        x = xval
        try:
            y = eval(self.CompiledExpression)
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
    def deriv(self,xval):
        #the difference between the two points being evaluated
        h = 0.0001
        y2 = self.evaluate(xval+h)
        y1 = self.evaluate(xval-h)
        #If function is undefined at the point, then the derivative is undefined
        if(y1==np.nan or y2 == np.nan):
            deriv = np.nan
        #derivative is the slope between two points that are very close to each other
        else:
            deriv = (y2-y1)/ (2*h)
        #error handling for values close to zero being set equal to zero
        if (abs(deriv) <= 1e-9):
            deriv = 0
        return deriv

    def secondDeriv(self,xval):
        # the difference between the two points being evaluated
        h = 0.0001
        y2 = self.deriv(xval+h)
        y1 = self.deriv(xval-h)
        # If derivative is undefined at the point, then the second derivative is undefined
        if(y1==np.nan or y2 == np.nan):
            secondDeriv = np.nan
        else:
            secondDeriv = (y2-y1)/ (2*h)
        # error handling for values close to zero being set equal to zero. This is a larger bound than earlier as error accumulates.
        if (abs(secondDeriv) <= 5e-8 ):
            secondDeriv = 0
        return secondDeriv

    #Uses Simpson's 3/8th rule for precise integral estimation
    def Integrate(self, UpperBound,LowerBound):
        lbEval = self.deriv(LowerBound)
        ubEval = self.deriv(UpperBound)
        TwoLEval = 3 * self.deriv( ((2*LowerBound) + UpperBound) / 3)
        TwoUEval = 3 * self.deriv(( (LowerBound + (2 * UpperBound)) / 3 ))

        Integral = ((UpperBound - LowerBound) / 8 ) * ( lbEval +  TwoLEval   +  TwoUEval  + ubEval )
        return Integral

    def FindHoles(self):
        HoleX = []
        HoleY = []
        HoleCoor = [HoleX, HoleY]
        #Iterate through each y value, excluding the first and last y value to prevent index errors
        for i in range(1, len(self.Domain)-1):
            #checks if y value is undefined
            if math.isnan(self.YFunction[i]):
                yPrev = self.YFunction[i - 1]
                yNext = self.YFunction[i + 1]
                #if y value is undefined, checks if previous and next value are undefined as well
                if(not(math.isnan(yPrev)) and not(math.isnan(yNext))):
                    # if they are not undefined, then there is a hole
                    HoleX.append(self.Domain[i])
                    #approximate the y value of the hole by taking average of previous and next y value
                    HoleY.append((yPrev + yNext) /2)
        return HoleCoor

    def findZeroes(self, level):
        Zeroes = []
        i = 0

        if (level == 0):
            for i in self.Domain:
                yCurrent = i
                yPrev = yCurrent
                if (i > 0):
                    yPrev = self.YFunction[i - 1]

                if ((yCurrent < 0 and yPrev > 0) or (yCurrent > 0 and yPrev < 0) or (abs(yCurrent) < 1e-9) or (
                    abs(yCurrent) == 0)):
                    Zeroes.append(self.Domain[i])

                i += 1
        if (level == 1):
            for i in self.Domain:
                yCurrent = i
                yPrev = yCurrent
                if (i > 0):
                    yPrev = self.YDeriv[i - 1]

                if ((yCurrent < 0 and yPrev > 0) or (yCurrent > 0 and yPrev < 0) or (abs(yCurrent) < 1e-9) or (
                            abs(yCurrent) == 0)):
                    Zeroes.append(self.Domain[i])

                i += 1
        if (level == 2):
            for i in self.Domain:
                yCurrent = i
                yPrev = yCurrent
                if (i > 0):
                    yPrev = self.YSecondDeriv[i - 1]

                if ((yCurrent < 0 and yPrev > 0) or (yCurrent > 0 and yPrev < 0) or (abs(yCurrent) < 1e-9) or (
                            abs(yCurrent) == 0)):
                    Zeroes.append(self.Domain[i])

                i += 1

        return Zeroes

    def findRelativeExtrema(self):
        ExtremaX = []
        ExtremaY = []
        ExtremaCoor = [ExtremaX, ExtremaY]

        counter = 0
        for x in self.Zeroes:

            if(x != (self.Xmin or self.Xmax)):

                y_prev = self.deriv(x-0.001)

                y_next = self.deriv(x+0.001)


                if((y_prev > 0 and y_next < 0) or (y_prev < 0 and y_next > 0)):

                    ExtremaX.append(x)
                    ExtremaY.append(self.evaluate(x))

            counter += 1
        return ExtremaCoor

    def findInflection(self):
        InflectionX = []
        InflectionY = []
        InflectionCoor = [InflectionX, InflectionY]

        counter = 0
        for x in self.FPrimeZeroes:

            if(x != (self.Xmin or self.Xmax)):

                y_prev = self.secondDeriv(x-0.001)
                #print("prev" + str(y_prev))
                y_next = self.secondDeriv(x+0.001)
                #print("next" + str(y_next))

                if( (y_prev and y_next) == 0):

                    return InflectionCoor

                if((y_prev > 0 and y_next < 0) or (y_prev < 0 and y_next > 0) ):

                    InflectionX.append(x)
                    InflectionY.append(self.evaluate(x))



            counter += 1
        return InflectionCoor



y1 = Equation("x^2",-10,10)
print(y1.evaluate(3))