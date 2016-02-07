import logging
import sys
import time

import numpy as np
from numpy import arange, dot, maximum, ones, tanh, zeros
from numpy.random import randn

from sklearn import datasets


import autodiff

try:
    from util import show_filters
except:
    print 'WARNING: show_filters will not work'
    def show_filters(*a, **kw): pass


dtype = 'float32'
n_classes = 3         # -- denoted L in the math expressions
img_shape = (28, 28)

#data_view = mnist.views.OfficialVectorClassification(x_dtype=dtype)
#x = data_view.all_vectors[data_view.fit_idxs[:n_examples]]
#y = data_view.all_labels[data_view.fit_idxs[:n_examples]]
iris = datasets.load_iris()
x = iris.data[:, :2]  # we only take the first two features.
y = iris.target
n_examples = len(x)


def ova_svm_prediction(W, b, x):
    return np.argmax(np.dot(x, W) + b, axis=1)


def hinge(u):
    return np.maximum(0, 1 - u)

ugrid = np.arange(-5, 5, .1)
#plot(ugrid, hinge(ugrid), label='hinge loss')
#plot(ugrid, ugrid < 0, label='zero-one loss')
#legend()

# -- prepare a "1-hot" version of the labels, denoted Y in the math
y1 = -1 * ones((len(y), n_classes)).astype(dtype)
y1[arange(len(y)), y] = 1

def ova_svm_cost(W, b, x, y1):
    # -- one vs. all linear SVM loss
    margin = y1 * (dot(x, W) + b)
    cost = hinge(margin).mean(axis=0).sum()
    return cost

def ova_svm_cost_l2(W, b, x):
    raise NotImplementedError('implement me')

# re-run the SGD and LBFGS training fragments after filling
# in this function body to implement an L2-regularized SVM.

# In cases where the training data are linearly separable, this can be very important.
# How big does \alpha have to be to make any difference?

# initialize the model
W = zeros((x.shape[1], n_classes), dtype=dtype)
b = zeros(n_classes, dtype=dtype)

# -- do n_online_loops passes through the data set doing SGD
#    This can be faster at the beginning than L-BFGS
t0 = time.time()
online_batch_size = 1
n_online_epochs = 1
n_batches = n_examples / online_batch_size
#W, b = autodiff.fmin_sgd(ova_svm_cost, (W, b),
#            streams={
#                'x': x.reshape((n_batches, online_batch_size, x.shape[1])),
#                'y1': y1.reshape((n_batches, online_batch_size, y1.shape[1]))},
#           	 loops=n_online_epochs,
#		step_size=0.01,
#		print_interval=n_examples,
#            )
#print 'SGD took %.2f seconds' % (time.time() - t0)
#show_filters(W.T, img_shape, (2, 5))

# -- L-BFGS optimization of our SVM cost.

def batch_criterion(W, b):
    return ova_svm_cost(W, b, x, y1)

W, b = autodiff.fmin_l_bfgs_b(batch_criterion, (W, b), maxfun=20, m=20, iprint=1)

print 'final_cost', batch_criterion(W, b)
# -- N. B. the output from this command comes from Fortran, so iPython does not see it.
#    To monitor progress, look at the terminal from which you launched ipython
#show_filters(W.T, img_shape, (2, 5))

train_predictions = ova_svm_prediction(W, b, x)
train_errors = y != train_predictions
print 'Current train set error rate', np.mean(train_errors)

test_predictions = ova_svm_prediction(W, b, iris.data[:,:2])
test_errors = iris.target != test_predictions
print 'Current test set error rate', np.mean(test_errors)

