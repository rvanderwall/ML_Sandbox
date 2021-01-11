import numpy as np
from NCP.Models import Models
from NCP.Visualizer import Visualizer
print("Hello, starting Neural Circuit Policy application.")


def create_data(N):
    data_x = np.stack(
        [np.sin(np.linspace(0, 3 * np.pi, N)),
         np.cos(np.linspace(0, 3 * np.pi, N))],
        axis=1
    )

    data_x = np.expand_dims(data_x, axis=0).astype(np.float32)
    data_y = np.sin(np.linspace(0, 6 * np.pi, N)).reshape([1, N, 1]).astype(np.float32)
    return data_x, data_y


def run_model(ltc_cell, model, losses, title):
    model.summary()
    v.visualize_model(ltc_cell, title)
    prediction = model(x).numpy()
    v.visualize_prediction(y, prediction, title + ": Before training")

    hist = model.fit(x=x, y=y, batch_size=1, epochs=200, verbose=1)
    losses.append((hist.history["loss"], title))
    v.visualize_loss(losses)

    prediction = model(x).numpy()
    v.visualize_prediction(y, prediction, title + ": After training")
    return losses


m = Models()
v = Visualizer()

N=48
x, y = create_data(N)
print("data_x.shape: ", str(x.shape))
print("data_y.shape: ", str(y.shape))
v.visualize_data(x, y)

ltc_cell, model = m.build_fc_model()
losses = run_model(ltc_cell, model, [], "Fully-connected")
fc_count = ltc_cell.synapse_count

ltc_cell, model = m.build_rand_model()
losses = run_model(ltc_cell, model, losses, "Random (75%)")
ran_count = ltc_cell.synapse_count

ltc_cell, model = m.build_NCP_model()
losses = run_model(ltc_cell, model, losses, "NCP")
ncp_count = ltc_cell.synapse_count

sparcity = 1 - ncp_count / fc_count
print(f"Sparsity level is {(100*sparcity):0.2f}%")
