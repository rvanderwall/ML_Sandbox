__author__ = 'robert'

import numpy as np

classifications = ["a",
                   "b",
                   "c",
                   "d"]

def build_vectors():
    class_vectors = []
    num_classes =len(classifications)
    index = 0
    for klass in classifications:
        vector = list(np.zeros(num_classes))
        vector[index] = 1
        class_vectors.append(vector)
        index += 1

    return class_vectors

def vectorize(val, class_vectors):
    index = classifications.index(val)
    return class_vectors[index]

def bv():
    print ("OK")
    vs = build_vectors()
    print (vs)
    v = vectorize("a", vs)
    print (v)
    v = vectorize("d", vs)
    print (v)

