import torch


class DataSrc:
    def __init__(self):
        torch.manual_seed(142)
        self.data_length = 1024

    def prep_training_data(self, target_func):
        """
            Generate a data set of
                x from [0..1]
                y = target_func(x)
        :return:
        """
        train_data_length = self.data_length
        train_data = torch.zeros((train_data_length, 2))
        train_data[:, 0] = torch.rand(train_data_length)
        train_data[:, 1] = torch.Tensor(list([target_func(x) for x in train_data[:, 0]]))
        train_labels = torch.zeros(train_data_length)
        train_set = [
            (train_data[i], train_labels[i]) for i in range(train_data_length)
        ]
        return train_set
