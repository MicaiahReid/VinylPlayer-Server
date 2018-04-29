# pylint: skip-file
import tensorflow as tf
import numpy as np
import cv2
from collections import Counter
import string
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
current_directory = os.path.dirname(os.path.realpath(__file__))
current_directory = current_directory.replace('\\','/')

def test(words):
    characters = sorted(list(set(Counter(string.ascii_letters).keys())))
    digits = sorted(list(set(Counter(string.digits).keys())))
    digits.extend(characters)
    classes = digits

    cnn_words = []
    with tf.Session() as sess:
        # Restore variables from disk.
        print(current_directory)
        meta_graph_path = current_directory + "/lib/bin/model/model.ckpt.meta"
        checkpoint_path = current_directory + "/lib/bin/model/"
        print("Meta Graph Path: " + meta_graph_path)
        print("Checkpoint Path: " + checkpoint_path)
        saver = tf.train.import_meta_graph(meta_graph_path)
        saver.restore(sess, tf.train.latest_checkpoint(checkpoint_path))
        graph = tf.get_default_graph()
        logits = graph.get_tensor_by_name("logits:0")
        x = graph.get_tensor_by_name("samples:0")

        # preprocess characters in each word for input into the network
        for word in words:
            characters = word        
            for i in range(len(characters)):
                characters[i] = cv2.resize(characters[i], (32, 32), interpolation = cv2.INTER_AREA)
                characters[i] = cv2.cvtColor(characters[i], cv2.COLOR_BGR2GRAY)                
                # print("Image after grayscale:")
                # plt.imshow(characters[i], cmap='gray')
                # plt.axis("off")
                # plt.show()
                characters[i] = np.reshape(characters[i], (characters[i].shape[0], characters[i].shape[1], 1))
            if(len(characters) <= 0):
                continue
            # feed characters of each word into network
            feed_dict = {x: characters}
            output = sess.run(logits, feed_dict=feed_dict)
            output = tf.argmax(output, 1)
            output = output.eval()

            # decode network output
            word = []
            for i in output:
                word.append(classes[i])
            word = ''.join(word)
            cnn_words.append(word)

    return ' '.join(cnn_words)