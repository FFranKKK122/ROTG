import random
import tool
from CsimulatedAnnealing import SimulatedAnnealing
import pandas as pd
import numpy as np
import logging
import time



class MemeticAlgorithm:

    def __init__(self, file_path, csv_pd):
        print('init')
        self.test_data_path = file_path
        self.tool = tool.Tool()
        self.max_span_time = 10000
        self.span = self.tool.io(self.test_data_path)  # 測資
        self.job_len = len(self.span[0])
        self.population_len = 4
        self.search_alter = True #True 代表local search會把排列也更新， False則不會，只更新makespans
        self.need_search_num = 4
        self.min_makespan_each_gen_list = []

        #random.seed(0)
        init_jobs = []
        init_makespans = []
        for i in range(self.population_len):
            jobs_seq = [int(e) for e in range(0, self.job_len)]
            random.shuffle(jobs_seq)
            init_jobs.append(jobs_seq)

        self.population = pd.DataFrame()
        self.population['jobs'] = init_jobs
        self.population = self.evaluation(self.population)
        self.population.sort_values('makespans', ascending=True, inplace=True)
        self.population.reset_index(inplace=True)
        self.population.drop(labels=["index"], axis="columns", inplace=True)

        self.SA_init_temp = 15000
        self.SA_init_alpha = 0.95
        self.SA_init_epoch_len = 40
        #initial先local search
        for i in range(self.need_search_num):
            #print(self.population['jobs'][i], self.population['makespans'][i])
            SA_search = SimulatedAnnealing(
                self.SA_init_temp, self.SA_init_alpha, self.SA_init_epoch_len, self.population['jobs'][i], self.test_data_path)
            SA_search.search()
            if self.search_alter:
                self.population['jobs'][i] = SA_search.min_jobs_seq
            self.population.loc[i, 'makespans'] = SA_search.min_makespan
            #print(self.population['jobs'][i], self.population['makespans'][i])

        self.min_makespan = 999999999
        self.min_jobs = []
        self.find_min_makespan()
        

    def search(self):
        print('start search')
        epoch_len = 24

        for i in range(epoch_len):
            start = time.time()
            print('epoch', i)
            # self.population = self.evaluation(self.population)

            offspring_list = []
            span_list = []
            for p in range(0,self.population_len,2):
                df = self.mating_selection(self.population)
                offspring, span = self.reproduction(df)
                offspring_list += offspring
                span_list += span

            population = pd.DataFrame()
            population['jobs'] = offspring_list
            population['makespans'] = span_list
            population = self.evaluation(population)
            self.environmental_selection(self.population, population)

            self.population.sort_values('makespans', ascending=True, inplace=True)
            self.population.reset_index(inplace=True)
            self.population.drop(labels=["index"], axis="columns", inplace=True)

            for i in range(self.need_search_num):
                SA_search = SimulatedAnnealing(
                    self.SA_init_temp, self.SA_init_alpha, self.SA_init_epoch_len, self.population['jobs'][i], self.test_data_path)
                SA_search.search()
                if self.search_alter:
                    self.population['jobs'][i] = SA_search.min_jobs_seq
                self.population.loc[i, 'makespans'] = SA_search.min_makespan
            self.find_min_makespan()
            print('min_makespan:', self.min_makespan)
            #logging.info('min_makespan: %d' % self.min_makespan)

            self.min_makespan_each_gen_list.append(self.min_makespan)
            end = time.time()
            print("執行時間：%f 秒" % (end - start))

        print('end search')
        return self.min_makespan_each_gen_list


    def evaluation(self, df):
        size = len(df.index)
        for i in range(size):
            df.loc[i, 'makespans'] = tool.makespan(np.array(self.span), df['jobs'][i])

        return df

    def reproduction(self, Parents):
        # use 'linear order crossover'
        max_gene_fixed_len =  self.job_len - 2

        gene_fixed_len = random.randint(1,max_gene_fixed_len)
        gene_split_position = random.randint(0, self.job_len - gene_fixed_len)

        ParentA = Parents.iloc[0,0]
        ParentB = Parents.iloc[1,0]

        ParentA_fixed_gene = ParentA[ gene_split_position:gene_fixed_len ]
        ParentB_fixed_gene = ParentB[ gene_split_position:gene_fixed_len ]

        front_len = len(ParentA[ 0:gene_split_position ])
        back_len  = self.job_len - front_len - len(ParentA_fixed_gene)

        ParentA_front = []
        ParentB_front = []

        ParentA_back = []
        ParentB_back = [] 

        for i in ParentA:
            if i not in ParentB_fixed_gene:
                if len(ParentB_front) < front_len:
                    ParentB_front.append(i)
                else:
                    ParentB_back.append(i)

        for i in ParentB:
            if i not in ParentA_fixed_gene:
                if len(ParentA_front) < front_len:
                    ParentA_front.append(i)
                else:
                    ParentA_back.append(i)

        childA =  ParentA_front + ParentA_fixed_gene + ParentA_back
        childB =  ParentB_front + ParentB_fixed_gene + ParentB_back

        #child = pd.DataFrame()
        #child['jobs'] = [childA,childB]
        #child['makespans'] = [0,0]

        return [childA, childB], [0, 0]

    def mating_selection(self, df):
        span_list = []
        jobs_list = []

        size = len(df.index)

        for i in range(2):
            a = random.randint(0, size - 1)
            b = random.randint(0, size - 1)

            while (a == b):
                b = random.randint(0, 3)

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



    def environmental_selection(self, parent, offspring):
        parent_min = self.find_min_from_df(parent)
        offspring_min = self.find_min_from_df(offspring)
        self.population['jobs'] = parent_min[0] + offspring_min[0]
        self.population['makespans'] = parent_min[1] + offspring_min[1]

    def find_min_from_df(self, df):
        df = df.sort_values('makespans',ascending=True)
        df.reset_index(inplace=True)
        df.drop(labels=["index"], axis="columns", inplace=True)
        jobs = []
        makespans = []
        for i in range(self.population_len//2):
            jobs.append(df['jobs'][i])
            makespans.append(df['makespans'][i])
        return [jobs, makespans]
        
    def find_min_makespan(self):
        df = self.population.sort_values('makespans', ascending=True)
        df.reset_index(inplace=True)
        df.drop(labels=["index"], axis="columns", inplace=True)

        if df['makespans'][0] < self.min_makespan:
            self.min_makespan = df['makespans'][0]
            self.min_jobs = df['jobs'][0]
