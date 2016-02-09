#####
# Author :        Amit Juneja
# File :          figure_maker.py
# Description :   Plot beats from classifier_data_nobase and classifier_data folder
#              
# Date :          8th Feb 2016
#####
import matplotlib.pyplot as plt 
import numpy as np 

file1 = open('classifier_data/105_V.csv','r')
#file1 = open('classifier_data_nobase/105_V.csv','r')

file1 = file1.read().split('\n')

x = []

for i in file1:
	i = i.split(',')
	if len(i)>0:
		x.append(float(i[:-5]))
	else:
		del i

file1.close()

plt.plot(x[0])
plt.plot(x[1])

plt.savefig('fig1.png')
