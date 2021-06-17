__author__ = 'robert'

from math import exp


def sigmoid(x):
    return 1.0 / (1.0 + exp(-x))

def loss(labels, predictions):
    _loss = 0
    for index in range(len(labels)):
        label = labels[index]
        prediction = predictions[index]
        if label > prediction:
            _loss += label - prediction
        else:
            _loss += prediction - label

    return _loss


data = [1, 5]
classes = [1, 0]

def find_class(x, w, b):
    y = w * x + b
    prediction = sigmoid(y)
    return prediction

def gradients(x, label, sig_y):
    s_by_b = -(label - sig_y) * sig_y * (1 - sig_y)
    s_by_w = s_by_b * x

    return s_by_w, s_by_b

def predict():
    w = 1.0
    b = 1.0
    alpha = 0.1
    grad_L_by_b = 0.0
    grad_L_by_w = 0.0

    for iter in range(200):
        predictions = []
        for data_index in range(len(data)):
            x = data[data_index]
            label = classes[data_index]
            prediction = find_class(x, w, b)
            predictions.append(prediction)
            L_by_w, L_by_b =  gradients(x, label, prediction)
            grad_L_by_b += L_by_b
            grad_L_by_w += L_by_w

        print("Predictions:{}".format(predictions))
        print("Loss:{}".format(loss(classes, predictions)))
        #print("Gradient: ({}, {})".format(grad_L_by_w, grad_L_by_b))
        w -= alpha * grad_L_by_w
        b -= alpha * grad_L_by_b
    print("w:{}  b:{}".format(w, b))

def simple_lr():
    print "lr"
    predict()

