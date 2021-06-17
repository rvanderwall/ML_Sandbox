from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import io
import imageio
from IPython.display import Image, display
from ipywidgets import widgets, Layout, HBox

# https://keras.io/examples/vision/conv_lstm/

def log(msg):
    n = datetime.now()
    print(f"{n}: {msg}")

log("Starting")
log("Conv LSTM for Frame prediction in video imaging")
print(tf.config.experimental.list_physical_devices('GPU'))

def get_data_sets():
    # Download and load the dataset.
    fpath = keras.utils.get_file(
        "moving_mnist.npy",
        "http://www.cs.toronto.edu/~nitish/unsupervised_video/mnist_test_seq.npy",
    )
    dataset = np.load(fpath)
    log(f"Finished getting data: {dataset.shape}")

    # Swap the axes representing the number of frames and number of data samples.
    dataset = np.swapaxes(dataset, 0, 1)
    # We'll pick out 1000 of the 10000 total examples and use those.
    dataset = dataset[:1000, ...]
    # Add a channel dimension since the images are grayscale.
    dataset = np.expand_dims(dataset, axis=-1)
    log(f"Trim data and expand dimensions: {dataset.shape}")

    # Split into train and validation sets using indexing to optimize memory.
    indexes = np.arange(dataset.shape[0])
    np.random.shuffle(indexes)
    train_index = indexes[: int(0.9 * dataset.shape[0])]
    val_index = indexes[int(0.9 * dataset.shape[0]) :]
    train_dataset = dataset[train_index]
    val_dataset = dataset[val_index]
    log("Data split into training and validation")

    # Normalize the data to the 0-1 range.
    train_dataset = train_dataset / 255
    val_dataset = val_dataset / 255
    return train_dataset, val_dataset


# We'll define a helper function to shift the frames, where
# `x` is frames 0 to n - 1, and `y` is frames 1 to n.
def create_shifted_frames(data):
    x = data[:, 0 : data.shape[1] - 1, :, :]
    y = data[:, 1 : data.shape[1], :, :]
    return x, y


def visualize(train_dataset):
    # Construct a figure on which we will visualize the images.
    fig, axes = plt.subplots(4, 5, figsize=(10, 8))

    # Plot each of the sequential images for one random data example.
    data_choice = np.random.choice(range(len(train_dataset)), size=1)[0]
    for idx, ax in enumerate(axes.flat):
        ax.imshow(train_dataset[data_choice][idx], cmap="gray")
        ax.set_title(f"Frame {idx + 1}")
        ax.axis("off")

    # Print information and display the figure.
    print(f"Displaying frames for example {data_choice}.")
    plt.show()


def build_model(x_train):
    # Construct the input layer with no definite frame size.
    inp = layers.Input(shape=(None, *x_train.shape[2:]))

    # We will construct 3 `ConvLSTM2D` layers with batch normalization,
    # followed by a `Conv3D` layer for the spatiotemporal outputs.
    x = layers.ConvLSTM2D(
        filters=64,
        kernel_size=(5, 5),
        padding="same",
        return_sequences=True,
        activation="relu",
    )(inp)
    x = layers.BatchNormalization()(x)
    x = layers.ConvLSTM2D(
        filters=64,
        kernel_size=(3, 3),
        padding="same",
        return_sequences=True,
        activation="relu",
    )(x)
    x = layers.BatchNormalization()(x)
    x = layers.ConvLSTM2D(
        filters=64,
        kernel_size=(1, 1),
        padding="same",
        return_sequences=True,
        activation="relu",
    )(x)
    x = layers.Conv3D(
        filters=1, kernel_size=(3, 3, 3), activation="sigmoid", padding="same"
    )(x)

    # Next, we will build the complete model and compile it.
    model = keras.models.Model(inp, x)
    model.compile(
        loss=keras.losses.binary_crossentropy, optimizer=keras.optimizers.Adam(),
    )
    return model


def train_model(model, x_train, y_train, x_val, y_val):
    # Define some callbacks to improve training.
    early_stopping = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10)
    reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor="val_loss", patience=5)

    # Define modifiable training hyperparameters.
    epochs = 1
    batch_size = 5

    # Fit the model to the training data.
    model.fit(
        x_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=(x_val, y_val),
        callbacks=[early_stopping, reduce_lr],
        verbose=True
    )

MODEL_NAME="Models/Model1"
def save_model(model):
    model.save(MODEL_NAME)

def restore_model():
    # pip install 'h5py==2.10.0' --force-reinstall
    model = keras.models.load_model(MODEL_NAME)
    return model

def show_prediction(model, example):

    # Pick the first/last ten frames from the example.
    frames = example[:10, ...]
    original_frames = example[10:, ...]

    # Predict a new set of 10 frames.
    for _ in range(10):
        # Extract the model's prediction and post-process it.
        new_prediction = model.predict(np.expand_dims(frames, axis=0))
        new_prediction = np.squeeze(new_prediction, axis=0)
        predicted_frame = np.expand_dims(new_prediction[-1, ...], axis=0)

        # Extend the set of prediction frames.
        frames = np.concatenate((frames, predicted_frame), axis=0)

    # Construct a figure for the original and new frames.
    fig, axes = plt.subplots(2, 10, figsize=(20, 4))

    # Plot the original frames.
    for idx, ax in enumerate(axes[0]):
        ax.imshow(np.squeeze(original_frames[idx]), cmap="gray")
        ax.set_title(f"Frame {idx + 11}")
        ax.axis("off")

    # Plot the new frames.
    new_frames = frames[10:, ...]
    for idx, ax in enumerate(axes[1]):
        ax.imshow(np.squeeze(new_frames[idx]), cmap="gray")
        ax.set_title(f"Frame {idx + 11}")
        ax.axis("off")

    # Display the figure.
    plt.show()

def make_gifs(model, examples):
    # Iterate over the examples and predict the frames.
    predicted_videos = []
    for example in examples:
        # Pick the first/last ten frames from the example.
        frames = example[:10, ...]
        original_frames = example[10:, ...]
        new_predictions = np.zeros(shape=(10, *frames[0].shape))

        # Predict a new set of 10 frames.
        for i in range(10):
            # Extract the model's prediction and post-process it.
            frames = example[: 10 + i + 1, ...]
            new_prediction = model.predict(np.expand_dims(frames, axis=0))
            new_prediction = np.squeeze(new_prediction, axis=0)
            predicted_frame = np.expand_dims(new_prediction[-1, ...], axis=0)

            # Extend the set of prediction frames.
            new_predictions[i] = predicted_frame

        # Create and save GIFs for each of the ground truth/prediction images.
        for frame_set in [original_frames, new_predictions]:
            # Construct a GIF from the selected video frames.
            current_frames = np.squeeze(frame_set)
            current_frames = current_frames[..., np.newaxis] * np.ones(3)
            current_frames = (current_frames * 255).astype(np.uint8)
            current_frames = list(current_frames)

            # Construct a GIF from the frames.
            with io.BytesIO() as gif:
                imageio.mimsave(gif, current_frames, "GIF", fps=5)
                predicted_videos.append(gif.getvalue())

    # Display the videos.
    print(" Truth\tPrediction")
    for i in range(0, len(predicted_videos), 2):
        # Construct and display an `HBox` with the ground truth and prediction.
        box = HBox(
            [
                widgets.Image(value=predicted_videos[i]),
                widgets.Image(value=predicted_videos[i + 1]),
            ]
        )
        open(f"Images/Img_{i}.gif", 'wb').write(predicted_videos[i])
        open(f"Images/Img_{i+1}.gif", 'wb').write(predicted_videos[i+1])

        display((box,))
        plt.show()


def run():
    train_dataset, val_dataset = get_data_sets()
    # Apply the processing function to the datasets.
    x_train, y_train = create_shifted_frames(train_dataset)
    x_val, y_val = create_shifted_frames(val_dataset)

    # Inspect the dataset.
    log("Training Dataset Shapes: " + str(x_train.shape) + ", " + str(y_train.shape))
    log("Validation Dataset Shapes: " + str(x_val.shape) + ", " + str(y_val.shape))

    # visualize(train_dataset)
    train = False
    if train:
        model = build_model(x_train)
        train_model(model, x_train, y_train, x_val, y_val)
        save_model(model)
    else:
        model = restore_model()

    # Select a random example from the validation dataset.
    example = val_dataset[np.random.choice(range(len(val_dataset)), size=1)[0]]
    # show_prediction(model, example)

    # Select a few random examples from the dataset.
    examples = val_dataset[np.random.choice(range(len(val_dataset)), size=5)]
    make_gifs(model, examples)

if __name__ == "__main__":
    run()