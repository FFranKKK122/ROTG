import tool
import math
import random
import copy
import simulatedAnnealing as SA

class MemeticAlgorithm:

    def __init__():
        self.test_data_path = './PFSP_benchmark_data_set/tai50_20_1.txt'
        self.tool = Tool()
        self.max_span_time = 10000
        self.span = self.tool.io(self.test_data_path)  # 測資
        self.job_len = len(self.span[0])
        random.seed(0)

        for i in range(4):
            jobs_seq = [int(e) for e in range(0, self.job_len)]
            random.shuffle(jobs_seq)
            init_list.append(jobs_seq)

        df = pd.DataFrame()
        df['jobs'] = init_list
        df['makespans'] = init_list
        pass

    def search():
        pass

    def evaluation():
        pass

    def mating_selection():
        pass

    def reproduction():
        pass

    def environmental_selection():
        pass
    