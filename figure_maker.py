#####
# Author :        Amit Juneja
# File :          figure_maker.py
# Description :   Plot beats from classifier_data_nobase and classifier_data folder
#
# Date :          8th Feb 2016
#####
import matplotlib.pyplot as plt
import numpy as np
import os


#file1 = open('data_extraction/classifier_data/105_V.csv','r')
#file1 = open('current_benchmarking/train_set.csv','r')
#file1 = open('data_extraction/classifier_data_nobase/105_V.csv','r')

#file1 = file1.read().split('\n')

labels = {0:[],1:[],2:[],3:[],4:[]}

label_name = ['N','V','S','F','Q']

colors = [(0.0, 0.0, 0.0),(0.0, 0.0, 1.0),(0.75, 0, 0.75),(1.0, 0.0, 0.0),(0.75, 0.75, 0)]

x = []
my_path = os.path.abspath(__file__)
for subdir, dirs, files in os.walk('data_extraction/classifier_data/V_new2/'):
	count=0
	for file in files:
		with open('data_extraction/classifier_data/V_new2/'+file,'r') as f:
			pay = f.read().split('\n')
			beats_arr = []
			plt.figure(0)
			for lines in pay:
				line = lines.split(',')
				if len(line)>1:
					beats = [float(val) for val in line[:-5]]
					plt.plot(beats,color=colors[count])
					beats_arr.append(beats)
				else:
					del line

			#plt.savefig('figures/temp/'+file[:-4]+'.png')
		if count==4:
			count=0
		else:
			count+=1
	plt.savefig('figures/temp/all_V_new2.png')
# for i in file1:
#   i = i.split(',')
#   if len(i)>1:
#     j = [float(val) for val in i[:-5]]
#     x.append(j)
#   else:
#     del i


# for i in file1:
#   i = i.split(',')
#   if len(i)>1:
#     j = [float(val) for val in i[:-5]]
#     label = int(i[-1])
#     labels[label].append(j)
#   else:
#     del i

# for i in xrange(5):
# for plts in labels[i]:
#    plt.figure(i)
#    plt.plot(plts,label=label_name[i],color=colors[i])
#    plt.savefig('figures/'+label_name[i]+'_arrhythmia.png')

#plt.plot(x[0],color=colors[0])
#plt.plot(x[1],color=colors[0])
#plt.plot(x[2],color=colors[1])
#plt.plot(x[3],color=colors[1])

#plt.savefig('figures/105_V_comparison.png')
