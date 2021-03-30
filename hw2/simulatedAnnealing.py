import tool
import math
import random
import copy


class SimulatedAnnealing:
    def __init__(self, temperture, alpha, epoch_len, initial_jobs, file='./PFSP_benchmark_data_set/tai20_5_1.txt'):
        self.temperture = temperture  # 初始溫度
        self.alpha = alpha  # temperture減少倍率
        self.count_time = 1  # 計算的數量
        self.max_count_time = 5000  # 總計算數
        self.epoch_len = epoch_len

        self.tool = tool.Tool()
        self.span = self.tool.io(file)  # 測資
        self.job_len = len(initial_jobs)
        self.min_jobs_seq = initial_jobs  # job初始排序
        self.min_makespan = self.tool.makespan(
            self.span, self.min_jobs_seq)  # 計算初始makespan
        self.makespan_array = [self.min_makespan]  # 儲存所有makespan

    def search(self):
        # print(self.min_jobs_seq)
        jobs_seq = copy.deepcopy(self.min_jobs_seq)
        makespan = self.min_makespan
        # search
        while self.count_time < self.max_count_time:
            for l in range(self.epoch_len):
                if self.count_time >= self.max_count_time:
                    break

                temp_jobs_seq = self.generateNewJobSeq(jobs_seq)
                temp_makespan = self.tool.makespan(self.span, temp_jobs_seq)

                self.count_time += 1
                # print('已搜索', self.count_time, '次')

                if temp_makespan < self.min_makespan:
                    self.min_jobs_seq = copy.deepcopy(temp_jobs_seq)
                    self.min_makespan = makespan

                if temp_makespan < makespan:
                    jobs_seq = temp_jobs_seq
                    makespan = temp_makespan
                    # self.makespan_array.append(temp_makespan)
                # 如果溫度計算出的機率足夠大的話，更新排序
                elif math.exp((makespan - temp_makespan) / self.temperture) > random.random():
                    jobs_seq = temp_jobs_seq
                    makespan = temp_makespan
                self.makespan_array.append(makespan)

            # if self.count_time >= self.max_count_time:
            #     break
            self.calculateEpoch()
            self.calculateTemperture()

        # print('最低makespan的job_seq')
        # print(self.min_jobs_seq)
        # print('最低makespan')
        # print(self.min_makespan)

    def generateNewJobSeq(self, jobs_seq):
        temp_jobs_seq = copy.deepcopy(jobs_seq)
        # 取得第一個隨機數
        first_elememt = random.randint(0, self.job_len-1)

        # 取得第二個隨機數且不與第一個重複
        second_elememt = random.randint(0, self.job_len-1)
        while second_elememt == first_elememt:
            second_elememt = random.randint(0, self.job_len-1)

        # 以兩者作為index的job_seq交換
        temp_jobs_seq[first_elememt], temp_jobs_seq[second_elememt] = temp_jobs_seq[second_elememt], temp_jobs_seq[first_elememt]

        return temp_jobs_seq

    def calculateEpoch(self):
        self.epoch_len = self.epoch_len

    def calculateTemperture(self):
        self.temperture *= self.alpha
