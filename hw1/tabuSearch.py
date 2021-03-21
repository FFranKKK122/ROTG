import tool
import math
import random
import copy
import queue
import collections 
from itertools import combinations




class TabuSearch:
    def __init__(self):
        
        self.ffe_count = 0
        self.ffe_max   = 10000    #todo
        self.generation_count = 0
        self.generation_max   = 100
        
        self.job_len = 20         #預設測資 tai20_5_1.txt

        self.neighbor_job_seqs = [] 
        self.neighbor_job_fitness = []

        self.length_of_tabu_list = 7 #magic number 
        self.tabu_list = collections.deque(maxlen = self.length_of_tabu_list)
        self.tabu_work_times = 0        #有幾次因為某 job_seq 已在tabu list 中,不得選擇該 job_seq


        self.tool = tool.Tool()        
        self.span = self.tool.io(file_path='./hw1/PFSP_benchmark_data_set/tai20_5_1.txt')  # 測資
        self.min_jobs_seq = [int(e) for e in range(0, self.job_len)]  # job初始排序
        self.min_makespan = self.tool.makespan(self.span, self.min_jobs_seq)  # 計算初始makespan
        self.experiment_result = [self.min_makespan]    #todo df 儲存所有makespan

    def search(self):
        #todo generation 代數 終止條件
        while (self.generation_count < self.generation_max):
            self.neighbor_job_seqs, self.neighbor_job_fitness = self.neighbor(self.min_jobs_seq)

            if self.ffe_count >= self.ffe_max:
                break

            sorted_neighbor_job_seqs = [seq for fitness , seq  in sorted(zip(self.neighbor_job_fitness,self.neighbor_job_seqs))]
            sorted_neighbor_job_fitness = sorted(self.neighbor_job_fitness)

            for seq in sorted_neighbor_job_seqs:
                index = sorted_neighbor_job_seqs.index(seq)
                if(not self.isInTabuList(seq)):
                    self.min_jobs_seq = sorted_neighbor_job_seqs[index]
                    self.min_makespan = sorted_neighbor_job_fitness[index]
                    self.putInTabuList(seq)
                    break
            
            print('第 ', self.generation_count, ' 代')
            self.generation_count +=1

        print('最低 makespan 的 job_seq ', self.min_jobs_seq)
        print('最低 makespan ',self.min_makespan)
        print('tabu list 禁止的次數 ', self.tabu_work_times)

    def neighbor(self, job_seq):
        job_len = len(job_seq)
        job_seq_tuple = tuple(job_seq)

        swap_order = list(combinations(range(0,job_len),2))
        neighbor_job_seqs = []
        neighbor_job_fitness = []

        for position1 , position2 in swap_order:
            neighbor_job_seq = list(job_seq_tuple)
            neighbor_job_seq[position1] ,neighbor_job_seq[position2] = neighbor_job_seq[position2] ,neighbor_job_seq[position1]

            neighbor_fitness = self.tool.makespan(self.span, neighbor_job_seq)

            if self.ffe_count >= self.ffe_max:
                break
            else:
                self.ffe_count+=1
                print('已評估', self.ffe_count, '次')

            neighbor_job_seqs.append(neighbor_job_seq)
            neighbor_job_fitness.append(neighbor_fitness)

        return neighbor_job_seqs,neighbor_job_fitness
        

    # 判斷某個 job_seq 是否已在 Tabu list
    def isInTabuList(self,jobs_seq):
        flag = False   
        for seq in self.tabu_list:
            if(jobs_seq == seq):
                flag = True
                self.tabu_work_times+=1
                return flag   
        
        return flag

    def putInTabuList(self,jobs_seq):
        self.tabu_list.append(jobs_seq)



if __name__ == '__main__':
    tabu = TabuSearch()
    tabu.search()

