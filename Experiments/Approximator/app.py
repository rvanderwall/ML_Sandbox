import random
from math import log
import pandas

from Approximator.Model import Logger, MLP
from Visualization.Visualizer import Visualizer

from sklearn.model_selection import train_test_split


def generator(x1, x2):
    return x1 * x2 + 20


def get_data(lgr, num_samples):
    random.seed(42)

    x_data = []
    y_data = []

    X1 = random.choices([10, 20, 50], k=num_samples)
    for x1 in X1:
        x2 = random.uniform(30000, 50000)  # SqFt
        y = generator(x1, x2)
        x_data.append((x1, x2))
        y_data.append(y)

    x_data = pandas.DataFrame(x_data)
    y_data = pandas.DataFrame(y_data)
    train_x, test_x, train_y, test_y = train_test_split(x_data, y_data, test_size=0.1, random_state=123)
    lgr.info(f"Training set: {train_x.shape} ==> {train_y.shape}")
    lgr.info(f"    test set: {test_x.shape} ==> {test_y.shape}")
    return train_x, train_y, test_x, test_y


def show_stats(lgr, model, v: Visualizer):
    for x1 in [10, 20, 50, 100]:
        X = []
        Y = []
        for x2 in range(500, 50_000, 10):
            X.append((x1, x2))
            actual = generator(x1, x2)
            Y.append(actual)

        X = pandas.DataFrame(X)
        Y = pandas.DataFrame(Y)
        predict = model.predict(X)
        error = abs(Y - predict)
        err_pct = error / Y
        avg_err = float(error.sum() / len(error))
        avg_pct = float(100.0 * err_pct.sum() / len(err_pct))
        lgr.info(f"x1={x1}; Average err: {avg_err} ({avg_pct:3.2f}%)")
        v.visualize_2_data_lines(f"Predict {x1}", list(X[1]), list(Y[0]), list(predict[:,0]))


def main():
    print("Approximator")
    log = Logger()
    v = Visualizer()
    mlp = MLP(log)
    train_x, train_y, test_x, test_y = get_data(log, 100)
    mlp.train(train_x, train_y, test_x, test_y)
    mlp.save()
    show_stats(log, mlp, v)


if __name__ == '__main__':
    main()
