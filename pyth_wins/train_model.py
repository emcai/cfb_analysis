import numpy as np
import csv
import sys

from sklearn import metrics
from sklearn.linear_model import LogisticRegression

def load_data(file_name):
	dataset = []
	with open(file_name) as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			dataset.append(row)
	dataset = dataset[1:]
	X_data = np.array(dataset)[:,1:4].astype(float)
	Y_data = np.array(dataset)[:,4].astype(int)
	return X_data, Y_data

def classify(X_train, Y_train, X_test, clf):
	clf.fit(X_train, Y_train)
	return(clf.predict(X_test))

def main():
	if len(sys.argv) != 3:
		print("Usage: <training file> <testing file>")
		exit()
	X_train, Y_train = load_data(sys.argv[1])
	X_test, Y_test = load_data(sys.argv[2])

	clf = LogisticRegression()
	clf.fit(X_train, Y_train)
	Y_predicted = clf.predict(X_test)
	Y_prob = clf.predict_proba(X_test)
	acc = metrics.accuracy_score(Y_test, Y_predicted)
	print(acc)

	for x in range(len(Y_prob)):
		print((x + 2, Y_prob[x][1], Y_predicted[x]))

if __name__ == '__main__':
	main()