from keras.models import Model
from keras.layers import Conv2D, Input, LeakyReLU, MaxPool2D, \
                         Dropout, BatchNormalization, Dense, \
                         Flatten, concatenate

class ConvNet:

    def __init__(self, input_shape):
        self.model = self.create_model(input_shape)

    def create_model(self, input_shape):
        board_in = Input((input_shape[0], input_shape[1], 1))
        turn_in = Input((1,))

        # Conv layers
        hid = Conv2D(32, 3, padding='same')(board_in)
        hid = LeakyReLU(0.2)(hid)
        hid = BatchNormalization()(hid)
        hid = MaxPool2D((2,2))(hid)

        hid = Conv2D(64, 3, padding='same')(hid)
        hid = LeakyReLU(0.2)(hid)
        hid = BatchNormalization()(hid)

        hid = Conv2D(128, 3, padding='same')(hid)
        hid = LeakyReLU(0.2)(hid)
        hid = BatchNormalization()(hid)
        hid = Flatten()(hid)

        merged = concatenate([hid, turn_in])

        hid = Dense(128)(merged)
        hid = LeakyReLU(0.2)(hid)
        hid = BatchNormalization()(hid)
        hid = Dropout(0.3)(hid)

        out = Dense(2, activation='softmax')(hid)
        model = Model(inputs=[board_in, turn_in], outputs=out)
        model.compile(optimizer='adam', loss='binary_crossentropy')
        return model 

    def train(self, X, y, batch_size, epochs = 100, validation_split = 0.3):
        return self.model.fit([X['board'], X['turn']], y, batch_size=batch_size, epochs=epochs, validation_split=validation_split)

    def predict(self, X):
        return self.model.predict(X)