


##
## First pass, hard code bounds
## Next pass, find the bounds to minimize error
##

class AxisAlignedClassifier:
    def __init__(self, data_set, w):
        self.x_bound = None
        self.y_bound = None
        self.__find_best_bounds(data_set, w)

    def valid_weak_classifier(self):
        return self.x_bound is not None or self.y_bound is not None

    def predict(self, data_point):
        #  Only axis-aligned planes allowed
        x, y = data_point
        if self.x_bound is not None:
            return self.__test_bound(x, self.x_bound)
        else:
            return self.__test_bound(y, self.y_bound)

    def __test_bound(self, v, bound):
        if bound > 0:
            if v < bound:
                return +1
            else:
                return -1
        else:
            if v > -bound:
                return +1
            else:
                return -1

    #
    # Error should never exceed 0.5
    # If it does, it is not a weak classifier and should be rejected
    #
    def err(self, data, data_weights):
        err = 0
        w_sum = 0.0
        I = []
        for index in range(len(data)):
            w_i = data_weights[index]
            w_sum += w_i
            p, v = data[index]
            h = self.predict(p)
            if h != v:
                err += w_i
                I.append(1.0)
            else:
                err += 0.0
                I.append(0)
        return err / w_sum, I

    def __find_best_bounds(self, data_set, w):
        best_x_err = 0.5
        best_x = None

        best_y_err = 0.5
        best_y = None

        for sign in [1.0, -1.0]:
            for x in range(data_set.max_x):
                self.x_bound = sign * (x + 0.5)
                err, _ = self.err(data_set.data, w)
                if err < best_x_err:
                    best_x_err = err
                    best_x = self.x_bound

        self.x_bound = None
        for sign in [1.0, -1.0]:
            for y in range(data_set.max_y):
                self.y_bound = sign * (y + 0.5)
                err, _ = self.err(data_set.data, w)
                if err < best_y_err:
                    best_y_err = err
                    best_y = self.y_bound

        self.x_bound = None
        self.y_bound = None
        if best_x_err < best_y_err:
            self.x_bound = best_x
        else:
            self.y_bound = best_y

