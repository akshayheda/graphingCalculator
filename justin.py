from math import tan, pi
import numpy as np
def frange(x, y, incr):
	while x < y:
		yield x
		x += incr

expr = compile("tan(x * pi)", "tmp.py", "eval")
gened = []



for i in frange(-10, 10, 0.001):
    x = i
    test = eval(expr)

    if ((abs(test) > 10)):
        gened.append(np.nan)
    else:
        gened.append(test)


    print(str(x) + " , " + str(test))