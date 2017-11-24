from keras.models import Model
from keras.layers import BatchNormalization, Conv2D, Input, Dense, Activation, Flatten, Concatenate, Lambda
from keras.initializers import TruncatedNormal

def new_model(input_shape, policy_width, parameters=None, naive=True):
    """
    Defines the structure of the model.
    Currently, a simple convolution network is used.
    """
    if naive:
        return naive_model(input_shape, policy_width, parameters)
    else:
        raise NotImplementedError

def naive_model(input_shape, policy_width, parameters):
    initializer = TruncatedNormal()
    inputs = Input(input_shape)

    # Main net. Should be improved
    x = Conv2D(32, (1, 1), kernel_initializer=initializer, bias_initializer=initializer, activation='relu')(inputs)
    x = Conv2D(32, (3, 3), kernel_initializer=initializer, bias_initializer=initializer)(x)
    # x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Conv2D(32, (3, 3), kernel_initializer=initializer, bias_initializer=initializer)(x)
    # x = BatchNormalization()(x)
    x = Activation('relu')(x)
    without_head = x

    # Policy net
    x = Conv2D(2, (1,1), kernel_initializer=initializer, bias_initializer=initializer)(without_head)
    # x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Flatten()(x)
    policy = Dense(policy_width, kernel_initializer=initializer, bias_initializer=initializer)(x)

    # Value net
    x = Conv2D(1, (1,1), kernel_initializer=initializer, bias_initializer=initializer)(without_head)
    # x = BatchNormalization()(x)
    x = Activation('relu')(x)
    x = Flatten()(x)
    x = Dense(64, activation='relu', kernel_initializer=initializer, bias_initializer=initializer)(x)
    x = Dense(1, activation='tanh', kernel_initializer=initializer, bias_initializer=initializer)(x)
    value = x

    # Concatenation
    x = Concatenate()([policy, value])
    model = Model(inputs=inputs, outputs=x)

    if parameters is not None:
        model.set_weights(parameters)

    model.summary()

    return model