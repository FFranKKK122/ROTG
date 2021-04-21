import tool
import numpy as np

if __name__ == "__main__":
    array = np.array([[5, 2, 1], [3, 5, 3], [4, 2, 2]])
    b = [0, 1, 2]
    re = tool.makespan(array, b)
    print(re)