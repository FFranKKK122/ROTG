from tool import Tool
import copy
import random
import threading
import multiprocessing as mp

class IterativeImprovement:

    def __init__(self):
        self.test_data_path = './PFSP_benchmark_data_set/tai50_20_1.txt'
        self.tool = Tool()
        self.max_span_time = 10000
        self.span = self.tool.io(self.test_data_path)  # 測資
        self.job_len = len(self.span[0])
        self.eval_time = 20

    def generateNeighborList(self, jobs_seq):
        ret = []

        ret.append(jobs_seq)

        for i in range(len(jobs_seq)):
            for j in range(i, len(jobs_seq)):
                if (i != j):
                    tmp_seq = copy.deepcopy(jobs_seq)
                    tmp_seq[i], tmp_seq[j] = tmp_seq[j], tmp_seq[i]
                    ret.append(tmp_seq)

        return ret

    def run(self, jobs_seq):
        min_span = self.tool.makespan(self.span, jobs_seq)  # 起始min值
        span_list = []
        count = 0
        while (count < self.max_span_time):

            nb_list = self.generateNeighborList(jobs_seq)

            for i in range(len(nb_list)):
                span = self.tool.makespan(self.span, nb_list[i])
                count += 1
                if (span < min_span):
                    min_span = span
                    jobs_seq = nb_list[i]

            if (jobs_seq == nb_list[0]):
                return min_span

            span_list.append(min_span)

        return min_span



    def average(self, lst):
        return sum(lst) / len(lst)

    def search(self):

        pool = mp.Pool(mp.cpu_count())

        random.seed(0)
        init_list = []
        for i in range(self.eval_time):
            jobs_seq = [int(e) for e in range(0, self.job_len)]
            random.shuffle(jobs_seq)
            init_list.append(jobs_seq)

        pool_out = pool.map_async(self.run, init_list)

        pool.close()
        pool.join()

        result_list = pool_out.get()

        print(result_list)
        print('min', min(result_list))
        print('max', max(result_list))
        print('avg', self.average(result_list))




if __name__ == "__main__":
    ii = IterativeImprovement()
    ii.search()
