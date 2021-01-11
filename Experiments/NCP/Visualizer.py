import kerasncp as kncp
import matplotlib.pyplot as plt
import seaborn as sns


class Visualizer:
    def visualize_1D_data(self, data_x, data_y):
        sns.set()
        plt.figure(figsize=(6, 4))
        plt.plot(data_x, label="N")
        plt.plot(data_y, label="P(N)")
        plt.ylim((0, 1.0))
        plt.title("Poisonn distribution")
        plt.legend(loc="upper right")
        plt.show()

    def visualize_data(self, data_x, data_y):
        sns.set()
        plt.figure(figsize=(6, 4))
        plt.plot(data_x[0, :, 0], label="Input feature 1")
        plt.plot(data_x[0, :, 1], label="Input feature 2")
        plt.plot(data_y[0, :, 0], label="Target output")
        plt.ylim((-1, 1))
        plt.title("Training data")
        plt.legend(loc="upper right")
        plt.show()

    def visualize_prediction(self, data_y, predict_y, title):
        sns.set()
        plt.figure(figsize=(6, 4))
        plt.plot(data_y[0, :, 0], label="Target output")
        plt.plot(predict_y[0, :, 0], label="LTC output")
        plt.ylim((-1, 1))
        plt.title(title)
        plt.legend(loc="upper right")
        plt.show()

    def visualize_loss(self, losses):
        sns.set()
        plt.figure(figsize=(6, 4))
        for loss, label in losses:
            plt.plot(loss, label=label)
        plt.xlabel("Training steps")
        plt.show()

    def visualize_model(self, ltc_cell: kncp.LTCCell, title):
        sns.set_style("white")
        plt.figure(figsize=(6, 4))
        legend_handles = ltc_cell.draw_graph(draw_labels=True, neuron_colors={"command": "tab:cyan"})
        plt.legend(handles=legend_handles, loc="upper center", bbox_to_anchor=(1, 1))
        plt.tight_layout()
        plt.title(title)
        plt.show()
