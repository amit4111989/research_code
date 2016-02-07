import os
import sys
import timeit

import numpy

import theano
import theano.tensor as T
from theano.tensor.shared_randomstreams import RandomStreams

x = T.matrix('x')


def load_data():
    ''' Loads the dataset

    :type dataset: string
    :param dataset: the path to the dataset (here MNIST)
    '''

    #############
    # LOAD DATA #
    #############

    f = open('general_data_set_1.csv','r')
    payload = f.read()
    payload = payload.split('\n')
    #train_set_x = []
    train_set_x = []
    train_y = []
    for i in xrange(len(payload)):
        payload[i] = payload[i].split(',')
        if len(payload[i])>1:
            payload[i] = [float(val) for val in payload[i]]
            train_set_x.append(payload[i][:-5])
            train_y.append(int(payload[i][-1]))
        else:
            del payload[i]
    train_set = (np.array(train_set_x),train_y)
  
    
    #train_set_x = numpy.array(train_set_x,dtype='f')
    #train_set_x = numpy.asarray(train_set_x,dtype='f')

    #train_set, valid_set, test_set format: tuple(input, target)
    #input is an numpy.ndarray of 2 dimensions (a matrix)
    #witch row's correspond to an example. target is a
    #numpy.ndarray of 1 dimensions (vector)) that have the same length as
    #the number of rows in the input. It should give the target
    #target to the example with the same index in the input.

    def shared_dataset(data_xy, borrow=True):
        """ Function that loads the dataset into shared variables

        The reason we store our dataset in shared variables is to allow
        Theano to copy it into the GPU memory (when code is run on GPU).
        Since copying data into the GPU is slow, copying a minibatch everytime
        is needed (the default behaviour if the data is not in a shared
        variable) would lead to a large decrease in performance.
        """
        data_x, data_y = data_xy
        shared_x = theano.shared(np.asarray(data_x,
                                               dtype=theano.config.floatX),
                                 borrow=borrow)
        shared_y = theano.shared(np.asarray(data_y,
                                               dtype=theano.config.floatX),
                                 borrow=borrow)

        # one-hot encoded labels as {-1, 1}
        data_y = np.asarray(data_y, dtype='int32')
        n_classes = len(np.unique(data_y))  # dangerous?
        y1 = -1 * np.ones((data_y.shape[0], n_classes))
        y1[np.arange(data_y.shape[0]), data_y] = 1

        shared_y1 = theano.shared(np.asarray(y1,
                                               dtype=theano.config.floatX),
                                 borrow=borrow)

        # When storing data on the GPU it has to be stored as floats
        # therefore we will store the labels as ``floatX`` as well
        # (``shared_y`` does exactly that). But during our computations
        # we need them as ints (we use labels as index, and if they are
        # floats it doesn't make sense) therefore instead of returning
        # ``shared_y`` we will have to cast it to int. This little hack
        # lets ous get around this issue
        return shared_x, shared_y, T.cast(shared_y1,  'int32')

    #test_set_x, test_set_y, test_set_y1 = shared_dataset(test_set)
    #valid_set_x, valid_set_y, valid_set_y1 = shared_dataset(valid_set)
    train_set_x, train_set_y, train_set_y1 = shared_dataset(train_set)

    rval = [(train_set_x, train_set_y, train_set_y1) ]
    return rval


def load_testing_data():

    ''' Loads the dataset

    :type dataset: string
    :param dataset: the path to the dataset (here MNIST)
    '''

    #############
    # LOAD DATA #
    #############

    f = open('test_set.csv','r')
    payload = f.read()
    payload = payload.split('\n')
    #train_set_x = []
    train_set_x = []
    train_y = []
    for i in xrange(len(payload)):
        payload[i] = payload[i].split(',')
        if len(payload[i])>1:
            payload[i] = [float(val) for val in payload[i]]
            train_set_x.append(payload[i][:-1])
            train_y.append(int(payload[i][-1]))
        else:
            del payload[i]
    train_set = (numpy.array(train_set_x),train_y)
  
    
    #train_set_x = numpy.array(train_set_x,dtype='f')
    #train_set_x = numpy.asarray(train_set_x,dtype='f')

    #train_set, valid_set, test_set format: tuple(input, target)
    #input is an numpy.ndarray of 2 dimensions (a matrix)
    #witch row's correspond to an example. target is a
    #numpy.ndarray of 1 dimensions (vector)) that have the same length as
    #the number of rows in the input. It should give the target
    #target to the example with the same index in the input.

    def shared_dataset(data_xy, borrow=True):
    #     """ Function that loads the dataset into shared variables

    #     The reason we store our dataset in shared variables is to allow
    #     Theano to copy it into the GPU memory (when code is run on GPU).
    #     Since copying data into the GPU is slow, copying a minibatch everytime
    #     is needed (the default behaviour if the data is not in a shared
    #     variable) would lead to a large decrease in performance.
    #     """
         data_x, data_y = data_xy
         shared_x = theano.shared(numpy.asarray(data_x,
                                               dtype=theano.config.floatX),
                                  borrow=borrow)
         shared_y = theano.shared(numpy.asarray(data_y,
                                               dtype=theano.config.floatX),
                                  borrow=borrow)

    #     # one-hot encoded labels as {-1, 1}
      

    #     # When storing data on the GPU it has to be stored as floats
    #     # therefore we will store the labels as ``floatX`` as well
    #     # (``shared_y`` does exactly that). But during our computations
    #     # we need them as ints (we use labels as index, and if they are
    #     # floats it doesn't make sense) therefore instead of returning
    #     # ``shared_y`` we will have to cast it to int. This little hack
    #     # lets ous get around this issue
         return shared_x, shared_y

    # #test_set_x, test_set_y, test_set_y1 = shared_dataset(test_set)
    # #valid_set_x, valid_set_y, valid_set_y1 = shared_dataset(valid_set)
    train_set_x, train_set_y = shared_dataset(train_set)

    rval = [(train_set_x, train_set_y)]
    return rval
