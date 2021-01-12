import matplotlib.pyplot as plt
import seaborn as sns


class Visualizer:
    def __init__(self):
        pass

    def visualize_data_bar(self, title, data_x, data_y, lim):
        sns.set()
        plt.figure(figsize=(6, 4))
        # plt.plot(data_x, label="N")
        plt.bar(data_x, height=data_y)
        plt.legend(loc="upper right")
        self._plot(title, lim)

    def visualize_data_line(self, title, data_x, data_y, lim):
        sns.set()
        plt.figure(figsize=(6, 4))
        plt.plot(data_x, data_y)
        self._plot(title, lim)

    def visualize_data_scatter(self, title, data_x, data_y, lim):
        sns.set()
        plt.figure(figsize=(6, 4))
        plt.scatter(data_x, data_y)
        self._plot(title, lim)

    def visualize_data_img(self, title, images):
        # only plot the first 16 images
        end = max(16, len(images))
        for i in range(end):
            plt.subplot(4, 4, i + 1)
            plt.imshow(images[i].reshape(28, 28), cmap="gray_r")
            plt.xticks([])
            plt.yticks([])

        self._plot(title)

    @staticmethod
    def _plot(title, lim=None):
        if lim is not None:
            plt.ylim((-lim, lim))
        plt.title(title)
        plt.show()
