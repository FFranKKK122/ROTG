import tool
class SimulatedAnnealing:
    def __init__(self):
        self.temperture = 0.9
        self.iter = 0

        self.tool = tool.Tool()
        self.span = self.tool.io('./PFSP_benchmark_data_set/tai20_5_1.txt')
        
    def train(self):
        self.jobs = [int(e) for e in range(0,20)]
        print(self.span)
        while self.iter <= 10000:

            self.iter += 1
        