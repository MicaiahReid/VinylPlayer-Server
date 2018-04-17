import tensorflow as tf
# Network Layers
 
# Convolutional wrapper
# x: [batch size, height, width, # of channels]
# kernel: [height filter, width filter, # of input channels, # of output channels]
# bias: equivalent to number of filters
def conv2d(x, kernels, biases, stride):
    print("Conv2D Filter Size: ")
    print(kernels.get_shape())
    print("Conv2D Stride: " + str(stride))
    print()
    layer = tf.nn.conv2d(
        input=x,
        filter=kernels,
        strides=[1,stride,stride,1],
        padding="SAME")
    layer = tf.nn.bias_add(layer, biases) 
    return tf.nn.relu(layer)
 
# Max pooling wrapper
# x: [batch size, height, width, # of channels]
# ksize: size of the window for each dimension of the input tensor
# strides: the stride of the sliding window for each dimension of the input tensor
# padding: padding algorithm
def max_pool2d(x, k, stride):
    print("Max Pool Filter Size: " + str(k))
    print("Max Pool Stride: " + str(stride))
    print()
    layer = tf.nn.max_pool(
        value=x,
        ksize=[1,k,k,1],
        strides=[1,stride,stride,1],
        padding="SAME",
        data_format='NHWC')
    return layer
 
# Dense/Fully-Connected Layer Wrapper
# x: [batch_size, 1, 1, width*height*num_channels]
# weights
def dense(x, weights, biases, use_dropout=True, dropout=1):
    # not currently using bias?
    units = weights.get_shape().as_list()[1]
    print("Dense layer # of nuerons: " + str(units))
    print("Dense layer dropout probability: " + str(use_dropout))     
    
    dense = tf.layers.dense(
            inputs=x, 
            units=units, 
            activation=tf.nn.relu,
            use_bias=True)
    if use_dropout:
        print("Dense layer dropout probability: " + str(dropout))
        dense = tf.nn.dropout(
            x=dense, 
            keep_prob=dropout)
    # layer = tf.add(tf.matmul(x, weights), biases)
    # layer = tf.nn.relu(layer)
    print()
    return dense
 
