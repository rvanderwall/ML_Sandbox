__author__ = 'robert'

from ShowUtils import show_data
from DataSet import DataSet
from BoostedClassifier import BoostedClassifier

# Dots in a 6x7 box
data = [
        [(1, 3), +1],
        [(2, 2), +1],
        [(3, 2), -1],
        [(3, 5), -1],
        [(3, 6), +1],
        [(4, 4), -1],
        [(4, 7), +1],
        [(5, 6), +1],
        [(6, 2), -1],
        [(6, 6), -1]
]
x_max=7
y_max=7


# data = [
#         [(0, 0), -1],
#         [(0, 1), +1],
#         [(1, 0), +1],
#         [(1, 1), -1],
# ]
# x_max=1
# y_max=1

def boost():
    data_set = DataSet(data, x_max, y_max)
    show_data(data_set)
    booster = BoostedClassifier(data_set)

    for i in range(3):
        added = booster.add_classifier()
        if not added:
            break

    for d in data_set.data:
        data_point, v = d
        predict = booster.boosted_predict(data_point)
        print predict, v

    booster.show_params()

    predicted_data = []
    for x in range(x_max+1):
        for y in range(y_max+1):
            predicted = booster.boosted_predict((x,y))
            predicted_data.append([(x,y), predicted])

    p_dataset = DataSet(predicted_data, x_max, y_max)
    show_data(p_dataset)
