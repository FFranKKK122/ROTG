# distutils: language=c++
import matplotlib.pyplot as plt
import pandas as pd 
import queue
import numpy
cimport numpy
from libcpp.deque cimport deque

cpdef int makespan(numpy.ndarray array, list order = [0, 1, 2] ):
        # job 數量
        cdef int machine_count = len(array)
        # 機器數量
        cdef int jobs = len(array[0])
        #print(jobs, machine_count)

        #起始時間
        cdef int time = 0
        #完成時間Queue
        cdef deque[int] end_time_q
        
        cdef int i  
        cdef int j
        #起始上一階段完成時間皆為0
        for i in range(jobs):
            end_time_q.push_back(0)

        for i in range(machine_count):

            for j in order:
                # 取得該job在上一階段的完成時間
                job_last_end = end_time_q.front()
                end_time_q.pop_front()
                # 如果時間超過前一個job在這個階段的完成時間，直接將現在時間設為該job在上一階段的完成時間
                if(job_last_end > time):
                    time = job_last_end
                # job在機器i中的執行時間
                time += array[i][j]

                end_time_q.push_back(time)
                #print(time)

            time = end_time_q.front()

        return end_time_q.back()

class Tool:
    def __init__(self):
        pass

    def plot(self, x_array, y_array):
        plt.plot(x_array, y_array)
        plt.xlabel('FFE')
        plt.ylabel('makespan')
        plt.show()
    
    
    
    def io(self , file_path='./PFSP_benchmark_data_set/tai20_5_1.txt'):
        df = pd.read_fwf(file_path,skiprows=[0],header=None)
        df = df.add_prefix('M')
        df = df.set_index('J' + df.index.astype(str))
        #print(df)
        return df.to_numpy()



if __name__ == '__main__':  # For test Class
    array = [[5, 2, 1], [3, 5, 3], [4, 2,  2]]
    tool = Tool()
    print(tool.io())


