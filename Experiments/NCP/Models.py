from tensorflow import keras
import kerasncp as kncp


class Models:
    def __build_model(self, wiring):
        ltc_cell = kncp.LTCCell(wiring)

        model = keras.models.Sequential(
            [
                keras.layers.InputLayer(input_shape=(None, 2)),
                keras.layers.RNN(ltc_cell, return_sequences=True),
            ]
        )
        model.compile(
            optimizer=keras.optimizers.Adam(0.01),
            loss='mean_squared_error',
        )
        return ltc_cell, model

    def build_fc_model(self):
        fc_wiring = kncp.wirings.FullyConnected(8, 1)  # 8 units, 1 motor unit
        return self.__build_model(fc_wiring)

    def build_rand_model(self):
        fc_wiring = kncp.wirings.Random(8, 1, sparsity_level=0.75)
        return self.__build_model(fc_wiring)

    def build_NCP_model(self):
        ncp_wiring = kncp.wirings.NCP(
            inter_neurons=3,
            command_neurons=4,
            motor_neurons=1,
            sensory_fanout=2,
            inter_fanout=2,
            recurrent_command_synapses=3,
            motor_fanin=4,
        )
        return self.__build_model(ncp_wiring)
