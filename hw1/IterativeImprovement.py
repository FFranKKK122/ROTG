from tool import Tool
import copy

class IterativeImprovement:

    def __init__(self):

        self.test_data_path = './PFSP_benchmark_data_set/tai20_5_1.txt'

        self.tool = Tool()
        self.span = self.tool.io(self.test_data_path)  # 測資
        self.job_len = len(self.span[0])


    def search(self):
        jobs_seq = [int(e) for e in range(0, self.job_len)]

        # search
        min_span = self.tool.makespan(self.span, jobs_seq) # 起始min值
        span_list = []

        while(True):

            nb_list = self.generateNeighborList(jobs_seq)

            for i in range(len(nb_list)):
                span = self.tool.makespan(self.span, nb_list[i])
                if(span < min_span):
                    min_span = span
                    jobs_seq = nb_list[i]

            if (jobs_seq == nb_list[0]):
                break

            span_list.append(min_span)


        self.tool.plot([int(e) for e in range(len(span_list))], span_list)

        return min_span



    def generateNeighborList(self, jobs_seq):
        ret = []

        ret.append(jobs_seq)

        for i in range(len(jobs_seq)):
            for j in range(i, len(jobs_seq)):
                if(i != j):
                    tmp_seq = copy.deepcopy(jobs_seq)
                    tmp_seq[i], tmp_seq[j] = tmp_seq[j], tmp_seq[i]
                    ret.append(tmp_seq)

        return ret


if __name__ == "__main__":
    ii = IterativeImprovement()
    print(ii.search())