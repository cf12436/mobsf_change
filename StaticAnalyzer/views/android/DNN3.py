import tensorflow as tf

n_input = 1092
n_hidden1 = 1000
n_hidden2 = 500
n_hidden3 = 100
n_classes = 2

def inference(input_x, drop=1.0):
    weights = {'h1': tf.Variable(tf.random_normal([n_input, n_hidden1])),
               'h2': tf.Variable(tf.random_normal([n_hidden1, n_hidden2])),
               'h3': tf.Variable(tf.random_normal([n_hidden2, n_hidden3])),
               'out': tf.Variable(tf.random_normal([n_hidden3, n_classes]))}

    biases = {'b1': tf.Variable(tf.random_normal([n_hidden1])),
              'b2': tf.Variable(tf.random_normal([n_hidden2])),
              'b3': tf.Variable(tf.random_normal([n_hidden3])),
              'out': tf.Variable(tf.random_normal([n_classes]))}

    layer_1 = tf.nn.relu(tf.matmul(input_x, weights['h1']) + biases['b1'])

    layer_2 = tf.nn.relu(tf.matmul(layer_1, weights['h2']) + biases['b2'])
    full_drop2 = tf.nn.dropout(layer_2, keep_prob=drop)

    layer_3 = tf.nn.relu(tf.matmul(full_drop2, weights['h3']) + biases['b3'])
    full_drop3 = tf.nn.dropout(layer_3, keep_prob=drop)

    out_layer = tf.matmul(full_drop3, weights['out']) + biases['out']
    return out_layer

