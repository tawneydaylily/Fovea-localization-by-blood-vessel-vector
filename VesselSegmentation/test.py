# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 08:09:11 2015

@author: Administrator
"""
import theano
import theano
from theano import function, config, shared
import theano.tensor as T
import numpy
import time

vlen = 10 * 30 * 768  # 10 x #cores x # threads per core
iters = 100

rng = numpy.random.RandomState(22)
x = shared(numpy.asarray(rng.rand(vlen), config.floatX))
f = function([], T.exp(x))
print(f.maker.fgraph.toposort())
t0 = time.time()
for i in range(iters):
    r = f()
t1 = time.time()
# print("Looping %d times took %f seconds" % (iters, t1 - t0))
print(theano.config.device)
print("Result is %s" % (r,))
if numpy.any([isinstance(x.op, T.Elemwise) for x in f.maker.fgraph.toposort()]):
    print(isinstance(x.op, T.Elemwise))
    print('Used the cpu')
else:
    print('Used the gpu')