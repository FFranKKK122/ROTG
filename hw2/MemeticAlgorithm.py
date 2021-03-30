import random
import tool
import simulatedAnnealing as SA
import pandas as pd


class MemeticAlgorithm:

    def __init__(self, file_path = './PFSP_benchmark_data_set/tai20_5_1.txt'):
        self.test_data_path = file_path
        self.tool = tool.Tool()
        self.max_span_time = 10000
        self.span = self.tool.io(self.test_data_path)  # 測資
        self.job_len = len(self.span[0])
        '''
        random.seed(0)
        init_jobs = []
        init_makespans = []
        for i in range(4):
            jobs_seq = [int(e) for e in range(0, self.job_len)]
            random.shuffle(jobs_seq)
            SA_search = SA.SimulatedAnnealing(
                100, 0.95, 40, jobs_seq, self.test_data_path)
            SA_search.search()
            init_jobs.append(SA_search.min_jobs_seq)
            init_makespans.append(SA_search.min_makespan)

        self.population = pd.DataFrame()
        self.population['jobs'] = init_jobs
        self.population['makespans'] = init_makespans
        
'''
    def search(self):
        pass

    def evaluation(self, df):
        size = len(df.index)
        for i in range(size):
            df['makespans'][i] = self.tool.makespan(self.span, df['jobs'][i])

        return df


    def mating_selection(self, df):
        random.seed(0)
        span_list = []
        jobs_list = []

        for i in range(2):
            a = random.randint(0, 3)
            b = random.randint(0, 3)

            while (a == b):
                b = random.randint(0, 3)
            print(a, b)

            if (df['makespans'][a] <= df['makespans'][b]):
                jobs_list.append(df['jobs'][a])
                span_list.append(df['makespans'][a])
            else:
                jobs_list.append(df['jobs'][b])
                span_list.append(df['makespans'][b])
        ret = pd.DataFrame()

        ret['jobs'] = jobs_list
        ret['makespans'] = span_list

        return ret

    def reproduction(self):
        pass

    def environmental_selection(self):
        pass

