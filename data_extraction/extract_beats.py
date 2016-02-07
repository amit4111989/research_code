#####
# Author :        Amit Juneja
# File :          extract_beats.py
# Description :   Extract beats from MIT-BIH Arrhythmia data
#                 Each beat has 99 samples before R-peak and 200 samples after R-peak
#                 R-peaks can be detected w/ annotation files
# Prerequisites : Download *.atr , *.dat , *.hea
#                 Extract annotations and data with WFDB CLI on Linux/Mac
#
#                 Write data to *.csv with rdsamp command
#
#                 ex : rdsamp -r 102 >> 102.csv
#
#                 Write annotations to *_atr.txt with rdann command
#
#                 ex : rdann -r 102 -a atr >> 102_atr.txt
#
# Example Usage : python extract_beats.py 102 V
# Dataset URL :   https://www.physionet.org/physiobank/database/mitdb/
# Date :          23rd Nov 2015
#####

import numpy
import scipy.signal
import sys
import itertools


def clean_signal(
      ecg,  # The raw ECG signal
      rate=360,   # Sampling rate in HZ
      # Window size in seconds to use for
      lowfreq=0.1,
      # High frequency of the band pass filter
      highfreq=100.0,
):

   # baseline correction and bandpass filter of signals
   lowpass = scipy.signal.butter(1, highfreq/(rate/2.0), 'low')
   highpass = scipy.signal.butter(1, lowfreq/(rate/2.0), 'high')
   # TODO: Could use an actual bandpass filter
   ecg_low = scipy.signal.filtfilt(*lowpass, x=ecg)
   ecg_band = scipy.signal.filtfilt(*highpass, x=ecg_low)
   return ecg_band


def extract_signal(filename):

   f = open('data/'+filename+'.csv','r')
   data = f.read()
   f.close()
   data = data.split('\n')
   output = []
   for i in data:
      i = i.split(',')
      print i[1]
      if len(i)>1:
         temp = float(i[1])
         temp = (temp-1024.00)/200.00
         output.append(temp)
   return output

def extract_labels(filename,beat_class):

   f = open('data/'+filename+'_atr.txt','r')
   data = f.read()
   f.close()
   data = data.split('\n')
   output = []
   for i in data:
      arr = i.split()
      if arr[2]==beat_class:
         output.append([int(arr[1]),arr[2]])
   return output

def extract_features(ecg,beat_index):
   output = []

   #99 samples before r-peak
   for i in xrange(99):
      index = 99-i
      output.append(ecg[beat_index-index])

   #200 samples after rpeak
   for i in xrange(201):
      output.append(ecg[beat_index+i])

   return output

if __name__ == '__main__':

   filename = sys.argv[1]
   beat_class = sys.argv[2]

   #remove gain and baseline from .csv and extract lead II signals

   ecg = extract_signal(filename)
   ecg = numpy.loadtext(ecg)

   #clean noise from signal data

   ecg = clean_signal(ecg)

   #extract r-peaks and labels from annotation file for desired beats

   label = extract_labels(filename,beat_class)

   # make feature array of samples for desired beats
   samples = []

   for sample in xrange(ecg):
      for peaks in label:
         if sample==peaks[0]:
            features = extract_features(ecg,sample)
            samples.append(features)
            samples.append(peaks[1])

   # write samples to a file

   outfile = open(filename+'_'+beat_class+'.csv', 'w+')

   for sample in samples:
      sample = list(itertools.chain(*sample))
      outfile.write(str(sample.split(',')))
      outfile.write('\n')

   outfile.close()




