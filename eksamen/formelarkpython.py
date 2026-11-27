#
# Formelark
#

#
# Oprettelse av numpy-matriser
#
import numpy as np

L = np.zeros((3,4)) # 3 rader, 4 kolonner
L = np.eye(3)       # 3x3 identitetsmatrise

#
# x = [0, 0.25, 0.5, 0.75]
#
x = np.linspace(0, 0.75, 4) 
x = np.linspace(0, 1, 4, endpoint=False)
x = np.arange(0, 1, 0.25)


#
# opprettelse av numerisk funksjon f = np.sin(x*y)
#
x = np.linspace(0,1,10)
y = np.linspace(0,1,10)
x,y = np.meshgrid(x,y)

f = np.sin(x*y) 

#
# integrasjon og derivasjon scipy
#
from scipy.integrate import tplquad, dblquad, quad

# integrasjon og derivasjon scipy
#
from scipy.integrate import tplquad, dblquad, quad

# Integral av x**2 for x = a..b
#
f = lambda x : x*2
a = 0
b = 1
I = quad(f, a, b)

# Dobbeltintegral av x*y for x = a..b og y = g(x)..h(x)
#
f = lambda y,x : x*y
a = 0
b = 1
g = lambda x : 0
h = lambda x : x
I = dblquad(f, a, b, g, h)

# Trippelinteral av x*y*z fro x = a..b, y = g(x)..h(x), z = q(x,y)..r(x,y)
#
f = lambda z,y,x : x*y*z
a = 0
b = 1
g = lambda x : 0
h = lambda x : x
q = lambda x,y : 0
r = lambda x,y : x+y
I = tplquad(f, a, b, g, h, q, r)


#
# Integrasjon og derivasjon med sympy
#
import sympy as sp
x,y,z = sp.symbols("x,y,z")

# bestemt og ubestemt integral av x**2
f = x*x
I = sp.integrate(f,x)        # ubestemt integral
I = sp.integrate(f, (x,0,1)) # bestemt integral

# dobbeltintegral
f = x*y
I = sp.integrate(f, (y, 0, x))
I = sp.integrate(I, (x, 0, 1))

# trippelintegral
f = x*y*z
I = sp.integrate(f, (z, 0, x+y))
I = sp.integrate(I, (y, 0, x))
I = sp.integrate(I, (x, 0, 1))

# derivasjon
f = x*y
fx = sp.diff(f, x)
fxy = sp.diff(fx, y)

# forenkling
f = sp.cos(x)**2 + sp.sin(y)**2
g = sp.simplify(f) # 1

# innsetting av verdier
f = x*y
f21 = f.subs(x, 2).subs(y,1) # f(2,1) = 2

#
# Plotting
#
# Last inn siden på nytt for hvert plott.
#
import matplotlib.pyplot as plt

x = np.linspace(0, 2*np.pi, 20)
f = np.sin(x)
plt.plot(x,f)
plt.show()


x = np.linspace(0, 1, 20)
y = np.linspace(0,1, 20)
x,y = np.meshgrid(x,y)
f = x*y
plt.imshow(f, cmap="hot")
plt.show()

x = np.linspace(0, 1, 20)
y = np.linspace(0,1, 20)
x,y = np.meshgrid(x,y)
f = x**3*y**3
plt.axes(projection="3d").plot_surface(x,y,f)
plt.show()




