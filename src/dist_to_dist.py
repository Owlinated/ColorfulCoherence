import tensorflow as tf
from keras.engine import Layer
from tensorflow import Tensor

from src.util.util import softmax_temperature


class DistToDist(Layer):
    """
    Layer to convert color distribution into lab color space
    """

    def __init__(self, color_map: Tensor, **kwargs):
        """
        Create layer to convert distribution into lab color space
        :param shape: Shape of grayscale input
        :param kwargs:
        """
        super(DistToDist, self).__init__(**kwargs)
        self.color_map = color_map

    def call(self, x, mask=None):
        [grayscale, color_classes] = x

        # Flatten classes into 2D array
        color_classes_flat = tf.reshape(color_classes, (-1, tf.shape(color_classes)[-1]))
        # Apply softmax with low temperature to create approximate one hot encoding
        color_classes_flat = softmax_temperature(color_classes_flat)

        # Reshape ab colors into 2D image plus channels
        color_classes_flat = tf.reshape(color_classes_flat, (-1, 256, 256, 313))

        return color_classes_flat

    def get_output_shape_for(self, input_shape):
        return input_shape
