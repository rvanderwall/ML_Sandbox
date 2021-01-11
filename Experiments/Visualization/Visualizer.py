import matplotlib.pyplot as plt
import seaborn as sns


class Visualizer:
    def visualize_data_bar(self, title, data_x, data_y, lim):
        sns.set()
        plt.figure(figsize=(6, 4))
        # plt.plot(data_x, label="N")
        plt.bar(data_x, height=data_y)
        plt.ylim((0, lim))
        plt.title(title)
        plt.legend(loc="upper right")
        plt.show()

    def visualize_data_line(self, title, data_x, data_y, lim):
        sns.set()
        plt.figure(figsize=(6, 4))
        plt.ylim((-lim, lim))
        plt.plot(data_x, data_y)
        plt.title(title)
        plt.show()

    def visualize_data_scatter(self, title, data_x, data_y, lim):
        sns.set()
        plt.figure(figsize=(6, 4))
        plt.ylim((-lim, lim))
        plt.scatter(data_x, data_y)
        plt.title(title)
        plt.show()
