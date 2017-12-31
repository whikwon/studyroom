from model import Model
import numpy as np
from data_util import load_data, generator
from config import Config
import tensorflow as tf
import os

## 변수로 할당된 값 불러오기 (hyperparameter, data dir, ...)
config = Config()
## data 불러오기
char_set, X_train, X_test, Y_train, Y_test = load_data(config.data_dir, config.seq_length)
## 모델을 불러오기
model = Model(config)
## session 불러오기
sess = tf.Session()
sess.run(tf.global_variables_initializer())


## saver 생성
saver = tf.train.Saver(max_to_keep=config.num_checkpoints)
save_path = os.path.join(config.save_path, config.save_filename)
step = 0


## for loop을 통해 train 과정하기
for epoch_i in range(config.num_epochs):
    data_generator = generator(X_train, Y_train, config.batch_size)
    data_generator2 = generator(X_test, Y_test, config.batch_size)
    for batch_i, (X_batch_train, Y_batch_train) in enumerate(data_generator):
        model.train(sess, X_batch_train, Y_batch_train)
        step += 1
        if (batch_i + 1) % 100 == 0:
            (X_batch_test, Y_batch_test) = next(data_generator2)
            test_loss, test_accuracy, results = model.eval(sess, X_batch_test, Y_batch_test)
            train_loss, train_accuracy, results = model.eval(sess, X_batch_train, Y_batch_train)

            for epoch_i, j, result in enumerate(results):
                index = np.argmax(result, axis=1)
                print(epoch_i, j, ''.join([char_set[t] for t in index]), 1)

                ##if j is 0:
                ##    print(''.join([char_set[t] for t in index]), end='')
                ##else:
                ##    print(char_set[index[-1]], end='')
    if  epoch_i % config.checkpoint_every== 0:
        saver.save(sess, save_path, global_step=step)