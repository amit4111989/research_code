import os
import cPickle
import numpy as np

x = []
y = []

for subdir, dirs, files in os.walk('training_data'):
	for file in files:
		with open('training_data/'+file,'r') as f:
			pay = f.read().split('\n')
			for beats in pay:
				beats = beats.split(',')
				if len(beats)>1:
					try:
						train_beats = [float(i) for i in beats]
					except:
						continue
					else:
						x.append(train_beats[:-5])
						y.append(train_beats[-1])
train_set = (np.array(x,dtype='float32'),np.array(y))

file = open('training_data/train_set.p','w+')
cPickle.dump(train_set,file)
file.close()


x = []
y = []
for subdir, dirs, files in os.walk('testing_data'):
	for file in files:
		with open('testing_data/'+file,'r') as f:
			pay = f.read().split('\n')
			for beats in pay:
				beats = beats.split(',')
				if len(beats)>1:
					try:
						test_beats = [float(i) for i in beats]
					except:
						continue
					else:
						x.append(test_beats[:-5])
						y.append(test_beats[-1])
test_set = (np.array(x,dtype='float32'),np.array(y))

file = open('testing_data/test_set.p','w+')
cPickle.dump(test_set,file)
file.close()

x = []
y = []
for subdir, dirs, files in os.walk('validation_data'):
	for file in files:
		with open('validation_data/'+file,'r') as f:
			pay = f.read().split('\n')
			for beats in pay:
				beats = beats.split(',')
				if len(beats)>1:
					try:
						test_beats = [float(i) for i in beats]
					except:
						continue
					else:
						x.append(test_beats[:-5])
						y.append(test_beats[-1])
test_set = (np.array(x,dtype='float32'),np.array(y))

file = open('validation_data/valid_set.p','w+')
cPickle.dump(test_set,file)
file.close()

