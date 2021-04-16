import random
import tool
import simulatedAnnealing as SA
import pandas as pd


class MemeticAlgorithm:

    def __init__(self, file_path='./PFSP_benchmark_data_set/tai20_5_1.txt'):
        print('init')
        self.test_data_path = file_path
        self.tool = tool.Tool()
        self.max_span_time = 10000
        self.span = self.tool.io(self.test_data_path)  # 測資
        self.job_len = len(self.span[0])

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
        self.min_makespan = 999999999
        self.min_jobs = []
        self.find_min_makespan()
        

    def search(self):
        print('start search')
        for i in range(2):
            self.population = self.evaluation(self.population)
            df = self.mating_selection(self.population)
            df2 = self.mating_selection(self.population)

            offspring, span = self.reproduction(df)
            offspring1, span1 = self.reproduction(df2)
            offspring += offspring1
            span += span1

            population = pd.DataFrame()
            population['jobs'] = offspring
            population['makespans'] = span
            population = self.evaluation(population)
            self.environmental_selection(self.population, population)

            for i in range(len(self.population.index)):
                SA_search = SA.SimulatedAnnealing(
                    100, 0.95, 40, self.population['jobs'][i], self.test_data_path)
                SA_search.search()
                self.population['makespans'][i] = SA_search.min_makespan
            self.find_min_makespan()
        print('end search')

    def evaluation(self, df):
        size = len(df.index)
        for i in range(size):
            df['makespans'][i] = self.tool.makespan(self.span, df['jobs'][i])

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
        random.seed(0)
        span_list = []
        jobs_list = []

        for i in range(2):
            a = random.randint(0, 3)
            b = random.randint(0, 3)

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
        df = df.sort_values('makespans',ascending=False)
        return [[df['jobs'][0], df['jobs'][1]], [df['makespans'][0], df['makespans'][1]]]
        
    def find_min_makespan(self):
        df = self.population.sort_values('makespans', ascending=True)
        if df['makespans'][0] < self.min_makespan:
            self.min_makespan = df['makespans'][0]
            self.min_jobs = df['jobs'][0]
