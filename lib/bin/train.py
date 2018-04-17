# pylint: skip-file
import string 
from collections import Counter
import tensorflow as tf
import matplotlib.pyplot as plt
import math
import numpy as np
import segmentation as seg
import dataset as D
import layers

# get classes
characters = sorted(list(set(Counter(string.ascii_letters).keys())))
digits = sorted(list(set(Counter(string.digits).keys())))
whitespace = sorted(list(set(Counter(string.whitespace).keys())))
characters.extend(digits)
characters.extend(whitespace[len(whitespace)-1])
letters = characters
num_classes = len(letters)
print(letters)
print(num_classes)

# dataset parameters 
img_height = 128
img_width = 128
num_channels = 1
annotation_train = 'annotation_train_50.txt'
relative_path = '../../mjsynth_dataset/'
batch_size = 10

# other parameters
debug_tensorflow = False
load_model = True
save_model = False
train_model = False
create_dataset = True
minArea = 128
maxArea = 6144

# training parameters
learning_rate = .0001
num_steps = 500
display_step = 2

# network parameters
num_input = img_height * img_width * num_channels
num_output = 16 # 16 output nodes so every letter can be output
conv_filter_size = 3
pool_filter_size = 2
conv_stride = 1
pool_stride = 2
dropout = .75 # dropout, probablility of keeping units

# Network Architecture
def ocr_cnn_net(x, kernels, biases, dropout):
    # Reshape it into [num_images, img_height, img_width]
    # 2ds convolutions can be used because it is assumed that the image is grayscale, thus channels is 1 
    input_layer = tf.reshape(x, shape=[-1, img_height, img_width, num_channels])
    conv1 = layers.conv2d(input_layer, kernels['conv1'], biases['conv1'], conv_stride)
    pool1 = layers.max_pool2d(conv1, pool_filter_size, pool_stride) 
    conv2 = layers.conv2d(pool1, kernels['conv2'], biases['conv2'], conv_stride)
    pool2 = layers.max_pool2d(conv2, pool_filter_size, pool_stride)
    shape = weights['dense1'].get_shape().as_list() 
    pool2_flat = tf.reshape(pool2, [-1, shape[0]])
    dense1 = layers.dense(pool2_flat, weights['dense1'], biases['dense1'], dropout=dropout)
    output_layer = layers.dense(dense1, weights['out'], biases['out'], use_dropout=True)

    print("Input shape: ")
    print(x.shape)
    print("Reshaped Input shape: ")
    print(input_layer.shape)
    print("Conv1 shape: ")
    print(conv1.shape)
    print("Pool1 shape: ")
    print(pool1.shape)
    print("Conv2 shape: ")
    print(conv2.shape)
    print("Pool2 shape: ")
    print(pool2.shape)
    print("Pool2_Flat shape: ")
    print(pool2_flat.shape)
    print("Dense1 shape: ")
    print(weights['dense1'].get_shape())
    print("output_layer shape: ")
    print(output_layer.shape)
    return output_layer

def train():
    # setting up for session     
    init = tf.global_variables_initializer()
     
    num_steps_per_epoch = math.ceil(dataset.labels.shape[0] / batch_size)
    num_epochs = 1
     
    print("Batch Size: " + str(batch_size))
    print("# of Samples: " + str(dataset.labels.shape[0]))
    print("# of Steps Per Epoch: " + str(num_steps_per_epoch))
    print("# of Epochs: " + str(num_epochs))
                   
    with tf.Session(config=tf.ConfigProto(log_device_placement=True)) as sess:
        sess.run(init)
        for epoch in range(num_epochs):
            for step in range(num_steps_per_epoch):   
                imgs_gray, imgs_rgb, labels = dataset.next_batch()
        #            for img_gray in imgs_gray:
        #                print("Grayscale:")
        #                shape = img_gray.shape
        #                img_gray = np.reshape(img_gray, (shape[0], shape[1]))
        #                print("Shape: ")
        #                print(shape)
        #                
        #                plt.imshow(img_gray, cmap='gray')
        #                plt.axis("off")
        #                plt.show()
                    
                print("Labels shape: ")
                print(Y.shape)
                print("Images shape: ")
                print(X.shape)
                
                feed_dict = {X: imgs_gray, Y: labels, dropout: 1.0}
                op, l, acc = sess.run([training_op, loss, accuracy], feed_dict=feed_dict) 
                pred = sess.run(prediction, feed_dict=feed_dict)
                logits = sess.run(logits_tensor, feed_dict=feed_dict)
             
                if step % display_step == 0 or step == 1:
                    print()
                    print("Epoch " + str(epoch) + ", Step " + str(step) + 
                          ", Loss= " + "{:.4f}".format(l) + 
                          ", Training Accuracy= " + "{:.3f}".format(acc) +
                          ", Network Prediction = ")
                    print(pred)
                    print("Raw Network Output = ")
                    print(logits)
                    print()
        print("Optimization Finished!")
        
        print("Saving Model")
        # Add ops to save and restore all the variables.
        saver = tf.train.Saver()
        save_path = saver.save(sess, "/tmp/model.ckpt")
        print("Model saved in path: %s" % save_path)

def restore():
    with tf.Session() as sess:
        saver = tf.train.Saver()
        saver.restore(sess, "/tmp/model.ckpt")
        # print("Model restored")
        # print()
        # print("Epoch " + str(epoch) + ", Step " + str(step) + 
        #       ", Loss= " + "{:.4f}".format(l) + 
        #       ", Training Accuracy= " + "{:.3f}".format(acc) +
        #       ", Network Prediction = ")
        # print(pred)
        # print("Raw Network Output = ")
        # print(logits)
        # print()
        return
        
# segmentation test
file = "../../mjsynth_dataset/500/7/139_ANTIPODEANS_3232.jpg"
# seg.segment(file
if load_model:
    restore()
    

if create_dataset:
    # training dataset
    dataset = D.Dataset(img_height, img_width, batch_size, output=letters, num_output=num_output)
    dataset.build_data_from_file(annotation_train, relative_path, segment=False)

if train_model:
    if dataset is None:
        dataset = D.Dataset(img_height, img_width, batch_size, output=letters, num_output=num_output)
        dataset.build_data_from_file(annotation_train, relative_path, segment=False)
        
    # Tensorflow graph input
    X = tf.placeholder(tf.float32, shape=(batch_size, img_width, img_height, num_channels), name="X")   # images
    Y = tf.placeholder(tf.float32, shape=(batch_size, num_output), name="Y")                            # samples 
    dropout = tf.placeholder(tf.float32, name="dropout") 
    
    # initialize weights & biases
    if load_model:
        # load the weights of the model
        print("Loading Model")
    else: 
        weights = {
            # 3x3 convolution, 1 input, 32 outputs
            'conv1': tf.Variable(tf.random_normal([conv_filter_size, conv_filter_size, 1, 32])),
            # 3x3 convolution, 32 inputs, 64 outputs
            'conv2': tf.Variable(tf.random_normal([conv_filter_size, conv_filter_size, 32, 64])),
            # fully connected (dense), 32*32*64 inputs, 1024 outputs
            'dense1': tf.Variable(tf.random_normal([64*32*32,1024])),
            # fully connected (dense), 1024 inputs, 16 outputs (classification of each letter)
            'out': tf.Variable(tf.random_normal([1024, num_output]))  
        }
         
        biases = {
            'conv1': tf.Variable(tf.random_normal([32])),
            'conv2': tf.Variable(tf.random_normal([64])),
            'dense1': tf.Variable(tf.random_normal([1024])),
            'out': tf.Variable(tf.random_normal([num_output]))  
        }
     
    # initialze network\
    logits = ocr_cnn_net(X, weights, biases, dropout)
    logits_tensor = tf.convert_to_tensor(logits, dtype=np.float32)
    print("logits shape: ")
    print(logits.shape)
    
    prediction = tf.nn.softmax(logits_tensor)
    print("prediction shape: ")
    print(prediction.shape)
    
#    decode = tf.argmax(prediction, axis=0)
    
    # loss    
    cross_entropy = tf.nn.softmax_cross_entropy_with_logits_v2(logits=prediction, labels=Y)
    loss = tf.reduce_mean(cross_entropy)
    optimizer = tf.train.AdamOptimizer(learning_rate=0.001)
    training_op = optimizer.minimize(loss)
     
    # accuracy
    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
    train()
             
             
