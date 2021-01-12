import torch
import torchvision
import torchvision.transforms as xform


class DataSrc:
    def __init__(self):
        torch.manual_seed(142)
        self.shape = (28, 28)

    def image_shape(self):
        return self.shape

    def prep_training_data(self):
        # The MNIST dataset consists of 28 × 28 pixel grayscale images of handwritten digits from 0 to 9.
        transform = xform.Compose(
            [xform.ToTensor(), xform.Normalize((0.5,), (0.5,))]
        )
        train_set = torchvision.datasets.MNIST(
            root=".", train=True, download=True, transform=transform
        )
        return train_set
