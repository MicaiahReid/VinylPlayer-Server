# pylint: skip-file
import tensorflow as tf
import numpy as np
import cv2
from collections import Counter
import string
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# current_directory = os.getcwd()
current_directory = os.path.dirname(os.path.realpath(__file__))
current_directory = current_directory.replace('\\','/')

def test(x_data):
    characters = sorted(list(set(Counter(string.ascii_letters).keys())))
    digits = sorted(list(set(Counter(string.digits).keys())))
    digits.extend(characters)
    classes = digits

    # resize data and make grayscale
    for i in range(len(x_data)): 
        x_data[i] = cv2.resize(x_data[i], (32, 32), interpolation = cv2.INTER_AREA)
        x_data[i] = cv2.cvtColor(x_data[i], cv2.COLOR_BGR2GRAY)
        # print("Image after grayscale:")
        # plt.imshow(x_data[i], cmap='gray')
        # plt.axis("off")
        # plt.show()
        x_data[i] = np.reshape(x_data[i], (x_data[i].shape[0], x_data[i].shape[1], 1))
    
    batch_size = len(x_data)

    with tf.Session() as sess:
        # Restore variables from disk.
        print(current_directory)
        meta_graph_path = current_directory + "/model/model.ckpt.meta"
        checkpoint_path = current_directory + "/model/"
        print("Meta Graph Path: " + meta_graph_path)
        print("Checkpoint Path: " + checkpoint_path)

        new_saver = tf.train.import_meta_graph(meta_graph_path)
        new_saver.restore(sess, tf.train.latest_checkpoint(checkpoint_path))

        graph = tf.get_default_graph()
        logits = graph.get_tensor_by_name("logits:0")
        x = graph.get_tensor_by_name("samples:0")
        feed_dict = {x: x_data}
        output = sess.run(logits, feed_dict=feed_dict)
        output = tf.argmax(output, 1)
        output = output.eval()
        print(output)
        print(len(output))

        if output is None:
            return ''

        # decode network output
        word = []
        for i in output:
            word.append(classes[i])
        word = ''.join(word)
        print(word)
        return word