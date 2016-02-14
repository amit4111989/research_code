import os
import cPickle
import numpy as np

x = []
y = []

for subdir, dirs, files in os.walk('training_data'):
	for file in files:
		with open(file,'r') as f:
			pay = f.read().split('\n')
			for beats in pay:
				beats = beats.split(',')
				if len(beats)>1:
					train_beats = [float(i) for i in beats]
					x.append(train_beats[:-5])
					y.append(train_beats[-1])
train_set = (np.array(x),y)

file = open('training_data/train_set.p','w+')
cPickle.dump(train_set,file)
file.close()


x = []
y = []
for subdir, dirs, files in os.walk('testing_data'):
	for file in files:
		with open(file,'r') as f:
			pay = f.read().split('\n')
			for beats in pay:
				beats = beats.split(',')
				if len(beats)>1:
					test_beats = [float(i) for i in beats]
					x.append(test_beats[:-5])
					y.append(test_beats[-1])
test_set = (np.array(x),y)

file = open('testing_data/train_set.p','w+')
cPickle.dump(test_set,file)
file.close()

