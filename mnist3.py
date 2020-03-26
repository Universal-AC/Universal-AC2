import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Conv2D
import datetime

mnist = tf.keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
#summary_writer = tf.summary.create_file_writer('/tmp/summaries')


class MyModel(tf.keras.Model):
  def __init__(self):
    super(MyModel, self).__init__()
    self.d1 = Flatten()
    self.d2 = Dense(50, activation = 'elu')
    self.d3 = Dense(30, activation = 'elu')
    self.d4 = Dense(10, activation = 'softmax')

  def call(self, x):
    x = self.d1(x)
    x = self.d2(x)
    x = self.d3(x)
    return self.d4(x)
    
def train(x, y, model):
    with tf.GradientTape as tape:
        prediction = model(x)
        loss = tf.keras.metrics.SparseCategoricalAccuracy(name = 'train_accuracy',y, prediction)
    
    gradients = tape.gradient(loss, model.trainable_variables)
    
def test(x, y, model):
    prediction = model(x)
    loss = tf.keras.metrics.SparseCategoricalAccuracy(name = 'train_accuracy',y, prediction)
    
    test_loss = tf.keras.metrics.Mean(name='test_loss', loss)
    #logdir = os.path.join("logs", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    #tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq=1)

def main():
    data = tf.data.Dataset.from_tensor_slices((x_train,y_train))
    data = data.shuffle(len(x_train)).batch(50)
    model = MyModel()
    
    epochs = 5
    for epoch in range(epochs):
        for i, images, labels in enumerate(data):
            train(images, labels, model)
            
            if (i%5 == 0):
                test(x_test, y_test, model)
            

if __name__ == '__main__':
    main()
