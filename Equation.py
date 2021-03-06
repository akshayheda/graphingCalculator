from __future__ import division
import numpy as np
from math import *
import math
import re

class Equation:
    def __init__(self, Expression="", Xmin=-10, Xmax=10, Ymin=-10, Ymax=10, resolution=-1):

        '''

        Equation Constructor

        :param Expression:
        :param Xmin:
        :param Xmax:
        :param Ymin:
        :param Ymax:
        :param resolution:

        The Equation contructor will generate all aspects of the equation in one shot once it is created. From there
        any of the attributes can be accessed by the user or another function from a single command without waiting
        for the attributes to generate.

        Attributes are evaluated in order of priority

        '''

        # Initialize the instrance variables used in the main functions from the contructor parameters
        self.Xmin = Xmin
        self.Xmax = Xmax
        self.Ymin = Ymin
        self.Ymax = Ymax
        if (resolution == -1):
            self.resolution = ((Xmax - Xmin) / 20000)
        else:
            self.resolution = resolution
        self.Expression = Expression

        # Convert the string input into python readable equation string
        # Convert python readable string into an python file that can have x values passed it it and return y values
        self.CompiledExpression = self.compileExpression()

        # Generate the domain
        self.Domain = self.domainGeneration()

        # Generate the Y values for f, f', and f''
        self.YFunction = self.generateFunction(0)
        self.YDeriv = self.generateFunction(1)
        self.YSecondDeriv = self.generateFunction(2)

        # Locate zeroes with in the Y values of f, f', and f''
        self.Zeroes = self.findZeroes(0)
        self.FPrimeZeroes = self.findZeroes(1)
        self.FDoublePrimeZeroes = self.findZeroes(2)

        # Use calculus to find relative extrema and inflection points
        self.ExtremaCoor = self.findRelativeExtrema()
        self.InflectionCoor = self.findInflection()

        # Locate removable discontinuities
        self.Holes = self.FindHoles()


    @staticmethod
    def parse(eq):


        #makes the equation parsable by using regex to replace edge cases
        eq = eq.lower()
        eq = eq.replace("^", "**")

        #handles cofunctions and converts to standard functions
        eq = eq.replace("sec(", "(1)/cos(")
        eq = eq.replace("csc(", "(1)/sin(")
        eq = eq.replace("cot(", "(1)/tan(")

        #replaces inverse functions with python notation
        eq = eq.replace("arctan(", "atan(")
        eq = eq.replace("arcsin(", "asin(")
        eq = eq.replace("arccos(", "acos(")

        eq = eq.replace("xx", "x*x")
        eq = eq.replace("xxx", "x*x*x")
        eq = eq.replace("xxxx", "x*x*x*x")

        #uses regex to convert implicit multiplication to explicit multiplication
        #matches each edge case (sin, cos, tan, etc)
        eq = re.sub("([0-9])x", "\\1*x", eq)
        eq = re.sub("([0-9])\(", "\\1*(", eq)
        eq = re.sub("([0-9])([a-z])", "\\1*\\2", eq)
        eq = re.sub("\)([a-z])", ")*\\1", eq)
        eq = eq.replace(")(", ")*(")

        #replaces square roots with numerical values truncated rounded at 3 digits of precision
        def parseSQRT(equation):
            #finds an instance of sqrt, then isolates the value, and replaces with the sqrt(value)
            start = 0
            start = equation.find("sqrt(", start)
            if start == -1:
                return equation
            end = equation.find(")", start + 1)
            number = equation[start + 5: end]
            number = float(number)
            equation = equation.replace(str(equation[start:end +1]), str(round(sqrt(number), 3)))
            return equation
        eq = parseSQRT(eq)

        return eq

    #case to deal with repeatedly asymptotic functions
    def AsymptoticFunction(self):
        if(self.getExpression().find("tan(") != -1):
            return True
        elif(self.getExpression().find("/tan(") != -1):
            return True
        elif (self.getExpression().find("/sin(") != -1):
            return True
        elif (self.getExpression().find("/cos(") != -1):
            return True
        else:
            return False


    # publically accessable getter functions, to access generated values of this object
    def getExpression(self):
        return self.Expression

    def getDomain(self):
        return self.Domain

    def getYFunction(self):
        return self.YFunction

    def getYDeriv(self):
        return self.YDeriv

    def getYSecondDeriv(self):
        return self.YSecondDeriv

    def getYZeroes(self):
        return self.Zeroes

    def getFPrimeZeroes(self):
        return self.FPrimeZeroes

    def getFDoublePrimeZeroes(self):
        return self.FDoublePrimeZeroes

    def getExtremaCoor(self):
        return self.ExtremaCoor

    def getInflectionCoor(self):
        return self.InflectionCoor

    def getHoleCoor(self):
        return self.Holes

    # creates a python file that can be evaluated from the expression
    def compileExpression(self):
        return compile(self.Expression, "temp.py", "eval")


    # steps through all values in the range using a resolution

    def valueGenerator(self):
        i = self.Xmin
        while i <= self.Xmax:
            yield i
            i += self.resolution

    # generates all the X values that will be evaluated

    def domainGeneration(self):
        x_val = []
        for x in self.valueGenerator():
            # floats are unable to be exactly zero, so we set it equal to zero if it is really close to zero
            if (abs(x) <= 1e-11):
                x_val.append(0.0)
            # all x values are rounded to 3 digits to reduce float error
            else:
                x_val.append(round(x, 3))

        return x_val

    # evaluates all x values for the function, derivative, or second derivative
    # @param Function: the y function being evaluated
    # @param Domain: the array of X values to evaluate
    # @param level: can be 0 for function, 1 for derivative, or 2 for second derivative
    def generateFunction(self, level):

        showFValues = False
        showFPrimeValues = False
        showFDoublePrimeValues = False

        yvals = []

        if (level == 0):
            for i in self.Domain:
                value = self.evaluate(i)
                yvals.append(value)
                if(showFValues): print("X: " + str(i),"f(x): " + str(value))
        if (level == 1):
            for i in self.Domain:
                value = self.deriv(i)
                yvals.append(value)
                if (showFPrimeValues): print("X: " + str(i), "f'(x): " + str(value))
        if (level == 2):
            for i in self.Domain:
                value = self.secondDeriv(i)
                yvals.append(value)
                if (showFDoublePrimeValues): print("X: " + str(i), "f(x): " + str(value))
        return yvals

    # evaluates the function at a given x value
    def evaluate(self, xval):
        x = xval
        try:
            y = eval(self.CompiledExpression)
        # error handling for invalid evaluation
        except ValueError:
            y = np.nan
        # error handling for divide by zero errors
        except ZeroDivisionError:
            y = np.nan
        # error handling for complex numbers
        except OverflowError:
            y = np.nan

        if (np.iscomplex(y)):
            y = np.nan
        # error handling for float error - if a value is below the bound, it is set to zero
        if (abs(y) < 1e-9):
            y = 0
        if(self.AsymptoticFunction() and (abs(self.Ymin) + abs(self.Ymax)) < y):
            y = np.nan

        return y

    # derivative evaluation using a difference quotient
    def deriv(self, xval):
        # the difference between the two points being evaluated
        h = 0.0001
        y2 = self.evaluate(xval + h)
        y1 = self.evaluate(xval - h)
        y = self.evaluate(xval)
        if (isnan(y)):
            return np.nan
        deriv = (y2 - y1) / (2 * h)
        # If function is undefined at the point, then the derivative is undefined
        if (y1 == np.nan or y2 == np.nan or deriv == np.nan or self.evaluate(xval) == np.nan):
            deriv = np.nan
        # derivative is the slope between two points that are very close to each other
        else:
            deriv = (y2 - y1) / (2 * h)
        # error handling for values close to zero being set equal to zero
        if (abs(deriv) <= 1e-9):
            deriv = 0
        return deriv

    def secondDeriv(self, xval):
        # the difference between the two points being evaluated
        h = 0.0001
        y2 = self.deriv(xval + h)
        y1 = self.deriv(xval - h)
        y = self.deriv(xval)
        if (isnan(y)):
            return np.nan
        secondDeriv = (y2 - y1) / (2 * h)
        # If function is undefined at the point, then the second derivative is undefined
        if (y1 == np.nan or y2 == np.nan or secondDeriv == np.nan or self.deriv(xval) == np.nan):
            secondDeriv = np.nan
        # second derivative is the slope between two points that are very close to each other
        else:
            secondDeriv = (y2 - y1) / (2 * h)
        # error handling for values close to zero being set equal to zero
        if (abs(secondDeriv) <= 1e-9):
            secondDeriv = 0
        return secondDeriv


    # Uses Simpson's 3/8th rule for precise integral estimation
    # integral = ((b-a)/8) [f(a) + 3f((2a + b))/3)) + 3f((a+2b)/3) + f(b)]
    def integrate(self, a, b, level):
        #case 1: if upper and lower bound are the same, return 0
        if (a == b):
            return 0
        if (b > a):
            return self.nsimpson(a, b, level)
        #if bounds are flipped, return -1 * integral
        if (a > b):
            temp = b
            b = a
            a = temp
            return -1 * self.nsimpson(a, b, level)
    #uses n interval simpson's rule to approximate integral
    def nsimpson(self, a, b, level):
        #number of intervals is 30 for every range of 1, with an additional 300 for good measure
        n = ceil((b - a) * 30 + 300)
        h = (b - a) / n
        print(n)

        #allows for level to passed in with appropriate return value
        #function integral
        if (level == 0):
            #adds the endpoints to the sum
            s = self.evaluate(a) + self.evaluate(b)
            #loops through while stepping by 2 to add 4f(x)
            for i in range(1, n, 2):
                s += 4 * self.evaluate(a + i * h)
            #loops through the other half of intervals to add the 2f(x)
            for i in range(2, n - 1, 2):
                s += 2 * self.evaluate(a + i * h)
            #returns integral
            return s * h / 3

        #derivative integral
        if (level == 1):
            #adds the endpoints to the sum
            s = self.deriv(a) + self.deriv(b)
            #loops through while stepping by 2 to add 4f'(x)
            for i in range(1, n, 2):
                s += 4 * self.deriv(a + i * h)
            #loops through the other half of intervals to add the 2f'(x)
            for i in range(2, n - 1, 2):
                s += 2 * self.deriv(a + i * h)
            #returns integral
            return s * h / 3

        #second derivative integral
        if (level == 2):
            #adds the endpoints to the sum
            s = self.secondDeriv(a) + self.secondDeriv(b)
            #loops through while stepping by 2 to add 4f''(x)
            for i in range(1, n, 2):
                s += 4 * self.secondDeriv(a + i * h)
            #loops through the other half of intervals to add the 2f''(x)
            for i in range(2, n - 1, 2):
                s += 2 * self.secondDeriv(a + i * h)
            #returns integral
            return s * h / 3


    def FindHoles(self):
        HoleX = []
        HoleY = []

        # Iterate through each y value, excluding the first and last y value to prevent index errors
        for i in range(1, len(self.Domain) - 2):

            # checks if y value is not undefined
            if math.isnan(self.YFunction[i]):

                yPrev = self.YFunction[i - 1]
                yNext = self.YFunction[i + 1]

                # if y value is undefined, checks if previous and next value are undefined as well
                if (not (math.isnan(yPrev)) and not (math.isnan(yNext))):
                    if (abs(yPrev - yNext) < 1):
                        # if they are not undefined, then there is a hole
                        HoleX.append(self.Domain[i])
                        # approximate the y value of the hole by taking average of previous and next y value
                        HoleY.append((yPrev + yNext) / 2)

        return [HoleX, HoleY]

    def findZeroes(self, level):
        Zeroes = []
        # function
        if (level == 0):
            # iterates through y values, starting from index 1, to prevent index errors for previous y value
            for i in range(1, len(self.YFunction) - 1):
                yCurrent = self.YFunction[i]
                yPrev = self.YFunction[i - 1]
                # checks if function crosses 0, or if y value is zero
                if ((yCurrent < 0 and yPrev > 0) or (yCurrent > 0 and yPrev < 0) or (abs(yCurrent) < 1e-9)):
                    Zeroes.append(self.Domain[i])
        # derivative
        if (level == 1):
            for i in range(1, len(self.YFunction) - 1):
                yCurrent = self.YDeriv[i]
                yPrev = self.YDeriv[i - 1]
                # checks if deriv crosses 0, or if deriv is zero
                if ((yCurrent < 0 and yPrev > 0) or (yCurrent > 0 and yPrev < 0) or (abs(yCurrent) < 1e-9)):
                    Zeroes.append(self.Domain[i])
        # second derivative
        if (level == 2):
            for i in range(1, len(self.YFunction) - 1):
                yCurrent = self.YSecondDeriv[i]
                yPrev = self.YSecondDeriv[i - 1]
                # checks if deriv crosses 0, or if second deriv is zero
                if ((yCurrent < 0 and yPrev > 0) or (yCurrent > 0 and yPrev < 0) or (abs(yCurrent) < 1e-9)):
                    Zeroes.append(self.Domain[i])
        return Zeroes

    def findRelativeExtrema(self):
        ExtremaX = []
        ExtremaY = []
        # iterates through the critical values of the function
        for x in self.FPrimeZeroes:
            y_prev = self.deriv(x - 0.001)
            y_next = self.deriv(x + 0.001)
            # checks if the derivative crosses x axis
            if ((y_prev > 0 and y_next < 0) or (y_prev < 0 and y_next > 0)):
                ExtremaX.append(x)
                ExtremaY.append(self.evaluate(x))
        return [ExtremaX, ExtremaY]

    def findInflection(self):
        InflectionX = []
        InflectionY = []
        # iterative through possible point of inflections
        for x in self.FDoublePrimeZeroes:
            y_prev = self.secondDeriv(x - 0.001)
            y_next = self.secondDeriv(x + 0.001)
            # if previous and next are zero, then the second derivative is zero, and there are no inflection points
            if ((y_prev and y_next) == 0):
                return [InflectionX, InflectionY]
            # checks if second derivative crosses X axis
            if ((y_prev > 0 and y_next < 0) or (y_prev < 0 and y_next > 0)):
                InflectionX.append(x)
                InflectionY.append(self.evaluate(x))
        return [InflectionX, InflectionY]


