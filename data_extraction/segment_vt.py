import cPickle as cp 

file = open('training_data/train_set.p','r')
pay = cp.load(file)
file.close()

segments = []

for i in xrange(50):
	if i==49:
		start = i*2160
		end = 107995
		segments.append(pay[0][0][start:end])
	else:
		start = i*2160
		end = (i+1)*2160
		segments.append(pay[0][0][start:end])

file = open('training_data/segments_200.p','w+')
cp.dump(segments,file)
file.close()
