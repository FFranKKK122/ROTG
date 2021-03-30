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

    def reproduction(Parents):
        # use 'linear order crossover'
        max_gene_fixed_len =  self.job_len - 2

        gene_fixed_len = random.randint(1,gene_fixed_len)
        gene_split_position = random.randint(0,self.job_len - gene_fixed_len)

        ParentA = Parents.iloc[0,0]
        ParentB = Parents.iloc[1,1]

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

        child = pd.DataFrame()
        child['job'] = [childA,childB]
        child['makespans'] = [0,0]

        return child
        
    def environmental_selection():
        pass
    