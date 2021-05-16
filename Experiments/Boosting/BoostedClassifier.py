
from math import log, exp

from LinearClassifier import AxisAlignedClassifier

class BoostedClassifier():
    def __init__(self, data_set):
        self.G_set = []
        self.alpha_set = []             ## Weight on classifier

        self.data_set = data_set
        self.weights = []               ## Weight on data points, wrong ones get more weight

        self.__init_weights(data_set.data)

    def add_classifier(self):
        G_m = AxisAlignedClassifier(self.data_set, self.weights)

        if not G_m.valid_weak_classifier():
            return False

        err_m, I = G_m.err(self.data_set.data, self.weights)
        alpha_m = self.__alpha(err_m)
        print err_m, alpha_m

        self.__find_new_w(I, alpha_m)

        self.G_set.append(G_m)
        self.alpha_set.append(alpha_m)
        return True

    def boosted_predict(self, data_point):
        sum = 0.0
        for index in range(len(self.G_set)):
            G = self.G_set[index]
            alpha = self.alpha_set[index]
            sum += alpha * G.predict(data_point)
        if sum > 0:
            return 1
        else:
            return -1

    def show_params(self):
        for g in self.G_set:
            assert isinstance(g, AxisAlignedClassifier)
            print g.x_bound, g.y_bound


    # Initialize all weights the same.
    def __init_weights(self, data):
        num_weights = len(data)
        self.weights = []
        w = 1.0/ num_weights
        for idx in range(num_weights):
            self.weights.append(w)

    def __alpha(self, err):
        alpha = 0.5 * log((1.0 - err) / err)
        return alpha

    # I - Incorrect vector,
    #     0 indicates the value was correct
    #     1 indicates incorrect
    def __find_new_w(self, I, alpha):
        new_w = []
        assert len(I) == len(self.data_set.data)
        assert len(I) == len(self.weights)

        for index in range(len(self.weights)):
            w_i = self.weights[index]
            I_i = I[index]
            scale = exp(alpha * I_i)
            new_w_i = w_i * scale
            new_w.append(new_w_i)

        self.weights = new_w

