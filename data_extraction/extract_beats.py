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
# Example Usage : (to extract x no. of beat labels)
#                 python extract_beats.py 102 1 V 4
#                 (to extract all beat labels)
#                 python extract_beats.py 102 1 V all
#                 (to extract first 5 min data)
#                 python extract_beats.py 102 2
#                 (to extract last 25 min data)
#                 python extract_beats.py 102 3
# Dataset URL :   https://www.physionet.org/physiobank/database/mitdb/
# Date :          23rd Nov 2015
#####

import scipy
import numpy
import scipy.signal
import sys
import itertools


def clean_signal(
      ecg,  # The raw ECG signal
      rate=360,   # Sampling rate in HZ
      # Window size in seconds to use for
      lowfreq=0.5,
      # High frequency of the band pass filter
      highfreq=45.0,
):

   # baseline correction and bandpass filter of signals
   lowpass = scipy.signal.butter(1, highfreq/(rate/2.0), 'low')
   highpass = scipy.signal.butter(1, lowfreq/(rate/2.0), 'high')
   # TODO: Could use an actual bandpass filter
   ecg_low = scipy.signal.filtfilt(*lowpass, x=ecg)
   ecg_band = scipy.signal.filtfilt(*highpass, x=ecg_low)
   return ecg_band


def shift_offset(ecg):
   """   Add an offset so that the signal stays within positive values """
   ecg = [i+0.08 for i in ecg]
   return ecg

def delete_empty_vals(ecg):
   index_to_delete = []

   for e in ecg:
      if not e:
         index_to_delete.append(ecg.index(e))

   for i in index_to_delete:
      del ecg[i]

   return ecg

def extract_signal(filename):

   f = open('data/'+filename+'.csv','r')
   data = f.read()
   f.close()
   data = data.split('\n')
   output = []
   for i in data:
      i = i.split(',')
      if len(i)>1:
         temp = float(i[1])
         temp = (temp)/1023.50
         output.append(temp)
   return output

def extract_labels(filename,job, beat_class=None, no_of_beats=None):

   f = open('data/'+filename+'_atr.txt','r')
   data = f.read()
   f.close()
   data = data.split('\n')
   output = []
   job_3_output=0
   if job==1:
      beat_class = get_beat_class(beat_class)
   for i in xrange(len(data)):
      if data[i]:
         if not i==0 and not i==len(data)-1 and data[i] and data[i+1]: #skip first and last beats
            arr = data[i].split()
            arr2 = data[i-1].split()
            arr3 = data[i+1].split()
            # calculate pre-rr interval
            if(arr[0].split(':')[0]>arr2[0].split(':')[0]):
               pre_rr = float(arr[0].split(':')[1])+60.00 - float(arr2[0].split(':')[1])
            else:
               pre_rr = float(arr[0].split(':')[1]) - float(arr2[0].split(':')[1])
            # calculate post-rr interval
            if(arr3[0].split(':')[0]>arr[0].split(':')[0]):
               post_rr = float(arr3[0].split(':')[1])+60.00 - float(arr[0].split(':')[1])
            else:
               post_rr = float(arr3[0].split(':')[1]) - float(arr[0].split(':')[1])
            # calculate avg-rr interval
            avg_interval = (pre_rr+post_rr)/2.00
            avg_rr = 60.00/avg_interval
            # calculate local-rr interval
            local_rr = 10.00/avg_interval
            # get beat class 0 , 1 , 2 , 3 , 4 depending on label
            beat = get_beat_class(arr[2])
            # extract particular beats if job==1
            if job==1:
               if len(output)>=int(no_of_beats):
                  break
               elif beat==beat_class:
                  output.append([int(arr[1]),beat,pre_rr,post_rr,avg_rr,local_rr])
               else:
                  pass
            # extract first 5 min of beats if job==2
            if job==2:
               time = arr[0].split(':')
               if int(time[0])<5:
                     output.append([int(arr[1]),beat,pre_rr,post_rr,avg_rr,local_rr])
               else:
                  break
            # extract last 25 min of beats if job==3
            if job==3:
               time = arr[0].split(':')
               if int(time[0])>=5:
                     output.append([int(arr[1]),beat,pre_rr,post_rr,avg_rr,local_rr])

   return output

def get_beat_class(beat):

   # MIT-BIH classes mapped to AAMI classes

   N = ['N', 'L', 'R', 'e', 'j']
   V = ['V', 'E']
   S = ['A', 'a', 'J', 'S']
   F = ['F']
   Q = ['/', 'Q', 'f']

   if beat in V:
      output = 1
   elif beat in S:
      output = 2
   elif beat in F:
      output = 3
   elif beat in Q:
      output = 4
   else:
      output = 0

   return output

def extract_features(ecg,beat_index):
   output = []

   #99 samples before r-peak
   for i in xrange(99):
      index = 99-i
      output.append(ecg[beat_index-index])

   #200 samples after rpeak
   for i in xrange(201):
      if not (beat_index+i) == len(ecg):
         output.append(ecg[beat_index+i])
      else:
         return False

   return output

if __name__ == '__main__':

   filename = sys.argv[1]
   job = int(sys.argv[2])
   if job==1:
      beat_class = sys.argv[3]
      no_of_samples = sys.argv[4]

      # Get all beats for matching beat class. This makes sure all beats are captured
      if no_of_samples == "all":
         no_of_samples = '2000'

   #remove gain and baseline from .csv and extract lead II signals

   ecg = extract_signal(filename)

   # Take care of empty values
   ecg = delete_empty_vals(ecg)

   ecg = numpy.loadtxt(ecg)

   #clean noise from signal data

   ecg = clean_signal(ecg)

   # raise offset so that values are above 0 (necessary for denosiing autoencoders)

   ecg = shift_offset(ecg)

   #extract r-peaks and labels from annotation file for desired beats

   if job==1:
      label = extract_labels(filename,job, beat_class, no_of_samples)
      print '...extracting complete'
   else:
      label = extract_labels(filename,job)
      print '...extracting complete'

   # make feature array of samples for desired beats
   samples = []

   print 'Making Features...'
   for sample in xrange(len(ecg)):
      for peaks in label:
         if sample==peaks[0]:
            features = extract_features(ecg,sample)
            if features:
               features.append(peaks[2])
               features.append(peaks[3])
               features.append(peaks[4])
               features.append(peaks[5])
               features.append(peaks[1])
               samples.append(features)
            else:
               print 'rpeak at beat', sample, 'skipped'

   # write samples to a file
   #
   print '...Writing Data...'
   if job==1:
      outfile = open('training_data/'+filename+'_'+beat_class+'.csv', 'w+')
   elif job==2:
      outfile = open('training_data/'+filename+'_train'+'.csv', 'w+')
   else:
      outfile = open('testing_data/'+filename+'_test'+'.csv', 'w+')

   print '...Almost Done...'

   # partition train set into train and validation sets

   if not job==2:
      for sample in samples:
         # this is important because sample.index(val) can result in varying indexes depeding on the number of duplicates
         val_count=1
         for val in sample:
            if len(sample)==val_count and not val_count==len(samples):
               outfile.write(str(val)+'\n')
            else:
               outfile.write(str(val)+',')
            val_count+=1


      outfile.close()

   else:
      sample_count = 0
      for sample in samples:
         # this is important because sample.index(val) can result in varying indexes depeding on the number of duplicates
         val_count=1
         if sample_count == (len(samples)/2)-1:
            outfile.close()
            outfile = open('validation_data/'+filename+'_valid'+'.csv', 'w+')
         for val in sample:
            if len(sample)==val_count and not val_count==len(samples):
               outfile.write(str(val)+'\n')
            else:
               outfile.write(str(val)+',')
            val_count+=1
         sample_count+=1


      outfile.close()




