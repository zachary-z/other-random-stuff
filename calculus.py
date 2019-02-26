# This is a single- and multivariable calculus library
# > It can calculate the derivative of a function at a point
# > It can calculate definite integrals
# > It can calculate the gradient of a multivariable function
# > It can calculate the divergence and curl of a vector field
# Working on multiple integration and Jacobian implementation...

import Vector

def derivative(f, x):
    return (f(x-x/10000)+f(x+x/10000))/(2*x/10000)

def integral(f, a, b):
    summation = 0
    for i in range(10000):
        summation += (b-a)/10000 * f(a+i*(b-a)/1000)
    return summation

def grad(f, v):
    return vec(derivative(lambda x: f(x, v[1], v[2]), v[0]),
               derivative(lambda y: f(v[0], y, v[2]), v[1]),
               derivative(lambda z: f(v[0], f[1], z), v[2]))

def div(f, v):
    return grad(f,v)*v

def curl(f, v):
    return grad(f,v)^v
