import os

with open('distribution.txt') as f:
	pay = f.read().split('\n')
	for lines in pay:
		lines = lines.split(',')
		if len(lines)==4:
			os.system('python extract_beats.py %s %s %s %s'%(lines[0],lines[1],lines[2],lines[3]))
		elif len(lines)==3:
			os.system('python extract_beats.py %s %s'%(lines[0],lines[1]))
		else:
			del lines


