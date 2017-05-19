from sklearn import datasets, linear_model
import matplotlib.pyplot as plt
import numpy as np
import sys

data_new = []

with open('matches.tsv', 'r') as data_in:
	data = [[x.strip() for x in d.split('\t')] for d in data_in]

# Artiest	Titel	Taal	Positie	Punten	Jaar	Volgorde	Land	URI	Energy	Liveliness	Tempo	Speechiness	Acousticness	Instrumentalness	Dancebality	Key	Duration_ms	Loudness	Valence

array = np.array(data)

size = len(array) * 0.9

X_train = array[:size, [9, 11, 13, 15, 19]].astype(float)
y_train = array[:size, 3].astype(float)

X_test = array[size:, [9, 11, 13, 15, 19]].astype(float)
y_test = array[size:, 3].astype(float)

regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)

print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"
      % np.mean((regr.predict(X_test) - y_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regr.score(X_test, y_test))

data = []
songs = []

with open('2017-finalists.tab', 'r') as data_in:
	for d in data_in:
		d = d.split('\t')
		data.append(d[1:])
		songs.append(d[0])


test_array = np.array(data).astype(float)

predictions =  zip(regr.predict(test_array), songs)

predictions.sort(key = lambda x: x[0])

for num, song in enumerate(predictions):
	print num+1, song[1]		