# 학습에 필요한 변수를 다 모아놓았다.
class Config():
    def __init__(self):
        self.learning_rate = 0.001
        self.num_epochs = 5
        self.batch_size = 100
        self.num_units = 500
        self.num_classes = 10
        self.data_dir = '../Examples/MNIST_data'
        self.num_checkpoints = 3
        self.checkpoint_every = 1
        self.save_path = '../Examples/MNIST_data/runs/'
        self.save_filename = 'mnist_model'
