from tool import Tool
import copy
import random
import threading

class IterativeImprovement:

    class SearchThread(threading.Thread):

        def __init__(self, result_list, jobs_seq, data_path, lock):

            threading.Thread.__init__(self)
            self.lock = lock
            self.jobs_seq = jobs_seq
            self.test_data_path = data_path
            self.tool = Tool()
            self.span = self.tool.io(self.test_data_path)  # 測資
            self.job_len = len(self.span[0])
            self.result_list = result_list

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

        def run(self):
            min_span = self.tool.makespan(self.span, self.jobs_seq)  # 起始min值
            span_list = []

            while (True):

                nb_list = self.generateNeighborList(self.jobs_seq)

                for i in range(len(nb_list)):
                    span = self.tool.makespan(self.span, nb_list[i])
                    if (span < min_span):
                        min_span = span
                        self.jobs_seq = nb_list[i]
                        # print(jobs_seq)

                if (self.jobs_seq == nb_list[0]):
                    self.lock.acquire()
                    self.result_list.append(min_span)
                    self.lock.release()
                    break

                span_list.append(min_span)



    def __init__(self):
        self.result_list = []
        self.test_data_path = './PFSP_benchmark_data_set/tai50_20_1.txt'
        self.tool = Tool()
        self.span = self.tool.io(self.test_data_path)  # 測資
        self.job_len = len(self.span[0])

    def average(self, lst):
        return sum(lst) / len(lst)

    def search(self):

        lock = threading.Lock()
        threads = []

        random.seed(0)
        for cot in range(20):
            jobs_seq = [int(e) for e in range(0, self.job_len)]
            random.shuffle(jobs_seq)
            threads.append(self.SearchThread(self.result_list, jobs_seq, self.test_data_path, lock))

        for i in threads:
            i.start()

        for i in threads:
            i.join()

        print(self.result_list)
        print('min', min(self.result_list))
        print('max', max(self.result_list))
        print('avg', self.average(self.result_list))
        #self.tool.plot([int(e) for e in range(len(result_list))], result_list)





if __name__ == "__main__":
    ii = IterativeImprovement()
    ii.search()
