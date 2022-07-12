import os.path

import keras as k
import keras.optimizers
import keras.losses
import keras.layers as kl
import numpy as np
import tensorflow as tf


class Logger:
    def info(self, msg):
        print(f"INFO: {msg}")


class MLP:
    def __init__(self, log):
        self.log = log
        self.num_epochs = 1000
        self.batch_size = 32
        self.version = 1
        layers = 2
        width = 10
        self.model_dir = f"Approximator/Models/model{self.version}"
        self.log.info(f"Create MLP Model version {self.version}")
        if os.path.exists(self.model_dir):
            self.log.info(f"Loading model from {self.model_dir}")
            self.model = self.load_model(self.model_dir)
        else:
            self.log.info("Loading clean model")
            self.model = self.get_model_layout(layers, width)

    def save(self):
        self.model.save(self.model_dir)

    def train(self, train_x, train_y, test_x, test_y):
        self.log.info(f"Training data shapes => training set: {train_x.shape}, test set: {test_x.shape}")

        early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=35,
            restore_best_weights=True,
        )

        train_x = self.scale_inputs(train_x)
        train_y = self.scale_inputs(train_y)
        test_x = self.scale_inputs(test_x)
        test_y = self.scale_inputs(test_y)
        history = self.model.fit(x=train_x, y=train_y, epochs=self.num_epochs, batch_size=self.batch_size,
                                 validation_data=(test_x, test_y), verbose=1,
                                 callbacks=[tf.keras.callbacks.TerminateOnNaN(), early_stopping])
        return history

    def predict(self, test_x):
        self.log.info(f"Prediction data shapes => data: {test_x.shape}")
        test_x = self.scale_inputs(test_x)
        p = self.model.predict(test_x)
        y = self.scale_output(p)
        return y

    def load_model(self, load_model_dir):
        uncompiled_model = keras.models.load_model(load_model_dir, compile=False)
        model = self._compile_model(uncompiled_model)
        return model

    def get_model_layout(self, layers, width):
        # These two lines are needed to ensure the same initial network is created each time
        initializer = tf.keras.initializers.GlorotUniform(seed=43)
        initializer._random_generator._force_generator = True

        model = k.Sequential()
        model.add(kl.Dense(width, input_dim=2, kernel_initializer=initializer, activation='relu'))
        for hidden in range(layers-1):
            model.add(kl.Dense(width, activation='relu', kernel_initializer=initializer))
        model.add(kl.Dense(1, kernel_initializer=initializer))
        model = self._compile_model(model)
        return model

    def _compile_model(self, uncompiled_model):
        # optimizer = k.optimizers.adam_v2.Adam(learning_rate=.001, clipnorm=0.50)
        loss_function = keras.losses.MeanAbsoluteError()
        uncompiled_model.compile(loss=loss_function, metrics=['mae'])
        return uncompiled_model

    def describe_model(self):
        description = {}
        description['last_layer'] = [float(w) for w in list(self.model.weights[4])]
        summary = []
        self.model.summary(print_fn=lambda x: summary.append(x))
        summary = "\n".join(summary)
        description['summary'] = summary
        return description

    def scale_inputs(self, X):
        return np.log(X)

    def scale_output(self, Y):
        return np.exp(Y)
