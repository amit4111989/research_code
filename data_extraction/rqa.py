from pyunicorn.timeseries.recurrence_plot import RecurrencePlot
import cPickle as cp 

file = open('training_data/segments.p','r')
pay = cp.load(file)
file.close()

rqa_features = []

for i in pay:
	clf = RecurrencePlot(i, threshold=0.1)
	params = []
	params.append(clf.recurrence_rate())
	params.append(clf.determinism())
	params.append(clf.average_diaglength())
	params.append(clf.diag_entropy())
	params.append(clf.white_vert_entropy())
	params.append(clf.vert_entropy())
	params.append(clf.laminarity())
	params.append(clf.max_diaglength())
	params.append(clf.max_vertlength())
	params.append(clf.mean_recurrence_time())
	rqa_features.append(params)

file = open('training_data/rqa_features.p','w+')
cp.dump(rqa_features,file)
file.close()
