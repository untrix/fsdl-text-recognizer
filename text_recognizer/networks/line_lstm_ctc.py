from boltons.cacheutils import cachedproperty
import tensorflow as tf
import tensorflow.keras.backend as K
from tensorflow.python.client import device_lib
from tensorflow.keras.layers import Conv2D, Dense, Dropout, Flatten, Input, MaxPooling2D, Permute, RepeatVector, Reshape, TimeDistributed, Lambda, LSTM, GRU, CuDNNLSTM, Bidirectional
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model as KerasModel

from text_recognizer.models.line_model import LineModel
from text_recognizer.networks.lenet import lenet
from text_recognizer.networks.misc import slide_window
from text_recognizer.networks.ctc import ctc_decode


def line_lstm_ctc(input_shape, output_shape, window_width=28, window_stride=14):
    image_height, image_width = input_shape
    output_length, num_classes = output_shape

    image_input = Input(shape=input_shape, name='image')
    y_true = Input(shape=(output_length,), name='y_true')
    input_length = Input(shape=(1,), name='input_length')
    label_length = Input(shape=(1,), name='label_length')

    gpu_present = len(device_lib.list_local_devices()) > 1
    lstm_fn = CuDNNLSTM if gpu_present else LSTM

    # Your code below here (Lab 3)
    image_reshaped = Reshape((image_height, image_width, 1))(image_input)
    image_patches = Lambda(
        slide_window,
        arguments={'window_width': window_width, 'window_stride': window_stride}
    )(image_reshaped)  # (num_windows, image_height, window_width, 1)
    convnet = lenet((image_height, window_width, 1), (num_classes,))
    convnet = KerasModel(inputs=convnet.inputs, outputs=convnet.layers[-2].output)

    convnet_outputs = TimeDistributed(convnet)(image_patches)  # (num_windows, 128)
    lstm_output = lstm_fn(128, return_sequences=True)(convnet_outputs)  # (num_windows, 128)
    softmax_output = TimeDistributed(Dense(num_classes, activation='softmax'), name='softmax_output')(lstm_output) # (num_windows, 128)
    # Your code above here (Lab 3)

    num_windows = int((image_width - window_width) / window_stride) + 1
    def temp(x, num_windows=num_windows):
        return x * num_windows
    input_length_processed = Lambda(temp)(input_length)

    ctc_loss_output = Lambda(
        lambda x: K.ctc_batch_cost(x[0], x[1], x[2], x[3]),
        name='ctc_loss'
    )([y_true, softmax_output, input_length_processed, label_length])

    ctc_decoded_output = Lambda(
        lambda x: ctc_decode(x[0], x[1]),
        name='ctc_decoded'
    )([softmax_output, input_length_processed])

    model = KerasModel(
        inputs=[image_input, y_true, input_length, label_length],
        outputs=[ctc_loss_output, ctc_decoded_output]
    )
    return model
