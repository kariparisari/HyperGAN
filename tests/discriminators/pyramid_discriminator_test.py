import tensorflow as tf
import hyperchamber as hc
import numpy as np
from hypergan.discriminators.pyramid_discriminator import PyramidDiscriminator
from hypergan.gan_component import ValidationException
from hypergan.ops import TensorflowOps
import hypergan as hg

from hypergan.gan_component import GANComponent

from unittest.mock import MagicMock

config = {
        'initial_depth': 1,
        'activation': tf.nn.tanh,
        'layers': 3,
        'depth_increase' : 3,
        'block' : hg.discriminators.common.standard_block
        }

class PyramidDiscriminatorTest(tf.test.TestCase):
    def test_config(self):
        with self.test_session():
            gan = hg.GAN()
            discriminator = PyramidDiscriminator(gan, config)
            self.assertEqual(discriminator.config.activation, tf.nn.tanh)

    def test_create(self):
        graph = hc.Config({
            'x': tf.constant(1., shape=[32,32,32,3])
        })

        with self.test_session():
            remove_d_config = hg.Configuration.default()
            remove_d_config['discriminators'] = []
            remove_d_config['losses'] = []
            remove_d_config['trainer'] = None
            gan = hg.GAN(config = remove_d_config, graph = {
                'x': tf.constant(1, shape=[1,4,4,1], dtype=tf.float32)
            })
            discriminator = PyramidDiscriminator(gan, config)
            gan.create()
            net = discriminator.create()
            self.assertEqual(int(net.get_shape()[1]), 7)

    def test_validate(self):
        with self.assertRaises(ValidationException):
            PyramidDiscriminator(hg.GAN(), {})
        
if __name__ == "__main__":
    tf.test.main()
