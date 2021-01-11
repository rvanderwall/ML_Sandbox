import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.autograd import Variable

from attention.Embedding import PositionalEncoding
from attention.NN import NoamOpt, LabelSmoothing

def plot_mask(mask):
    plt.figure(figsize=(5,5))
    plt.imshow(mask)
    plt.show()


def plot_encoding():
    plt.figure(figsize=(15, 5))
    pe = PositionalEncoding(20, 0)
    y = pe.forward(Variable(torch.zeros(1, 100, 20)))
    plt.plot(np.arange(100), y[0, :, 4:8].data.numpy())
    plt.legend(["dim %d" % p for p in [4, 5, 6, 7]])
    plt.show()

def plot_rates():
    opts = [NoamOpt(512, 1, 4000, None),
            NoamOpt(512, 1, 8000, None),
            NoamOpt(256, 1, 4000, None)]
    plt.plot(np.arange(1, 20000), [[opt.rate(i) for opt in opts] for i in range(1, 20000)])
    plt.legend(["512:4000", "512:8000", "256:4000"])
    plt.show()

def plot_label_smoothing():
    # Example of label smoothing.
    crit = LabelSmoothing(5, 0, 0.4)
    predict = torch.FloatTensor([[0, 0.2, 0.7, 0.1, 0],
                                 [0, 0.2, 0.7, 0.1, 0],
                                 [0, 0.2, 0.7, 0.1, 0]])
    v = crit(Variable(predict.log()),
             Variable(torch.LongTensor([2, 1, 0])))

    # Show the target distributions expected by the system.
    plt.imshow(crit.true_dist)
    plt.show()

def plot_loss_smooth():
    crit = LabelSmoothing(5, 0, 0.1)
    def loss(x):
        d = x + 3 * 1
        predict = torch.FloatTensor([[0, x / d, 1 / d, 1 / d, 1 / d],
                                     ])
        # print(predict)
        return crit(Variable(predict.log()),
                    Variable(torch.LongTensor([1]))).data

    plt.plot(np.arange(1, 100), [loss(x) for x in range(1, 100)])
    plt.show()
