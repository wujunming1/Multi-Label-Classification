#!/usr/bin/python
import tensorflow as tf

from config import Config
from model import Multi_Label_Class
from dataset import DataSet

FLAGS = tf.app.flags.FLAGS # transfer parameters of "tf.app.run( )" needed
# Use ==================================
tf.flags.DEFINE_string('phase', 'train',
                       'The phase can be train, eval')

tf.flags.DEFINE_boolean('load_cnn', True,
                        'Turn on to load a pretrained CNN model')
tf.flags.DEFINE_string('cnn_model_file', './pretrain_cnn/vgg16_no_fc.npy',
                       'The file containing a pretrained CNN model')

tf.flags.DEFINE_boolean('train_cnn', False,
                        'Turn on to train both CNN and RNN. \
                         Otherwise, only RNN is trained')

# =================================
tf.flags.DEFINE_boolean('load', False,
                        'Turn on to load a pretrained model from either \
                        the latest checkpoint or a specified file')
tf.flags.DEFINE_string('model_file', None,
                       'If sepcified, load a pretrained model from this file')

tf.flags.DEFINE_integer('beam_size', 3,
                        'The size of beam search for caption generation')




        
def main(argv):
    config = Config()
    config.phase = FLAGS.phase
    config.train_cnn = FLAGS.train_cnn
    FLAGS.load_cnn = FLAGS.load_cnn


    with tf.Session() as sess:
        #if FLAGS.phase == 'train':
        # training phase
        model = Multi_Label_Class(config) # Already building model?
        sess.run(tf.global_variables_initializer())
        if FLAGS.load_cnn:
            print('Load CNN is True........')
            model.load_cnn(sess, FLAGS.cnn_model_file)
        print('tf.get_default_graph().finalize()')
        tf.get_default_graph().finalize() # Returns the default graph for the current thread.
        model.save()
        model.train(sess) # Training model
        
        # elif FLAGS.phase == 'eval':
        # evaluation phase
        config.phase = 'eval'
        model = Multi_Label_Class(config)
        model.load(sess, FLAGS.model_file)
        tf.get_default_graph().finalize()
        model.eval(sess)


if __name__ == '__main__':
    tf.app.run() 
    #Runs the program with an optional 'main' function and 'argv' list.
    # tf.app.run(main=None, argv=None)
