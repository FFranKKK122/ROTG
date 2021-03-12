import matplotlib.pyplot as plt

class Tool:
    def __init__(self):
        pass

    def plot(self, x_array, y_array):
        plt.plot(x_array, y_array)
        plt.xlabel('iteration')
        plt.ylabel('makespan')
        plt.show()