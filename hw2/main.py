import pandas as pd
import MemeticAlgorithm as MA
from os import listdir
from os.path import isfile, join
import random
import logging
import multiprocessing as mp


# ================================================
def task(seed, fpath):
    csv_pd = pd.DataFrame()

    random.seed(seed)
    logging.info('seed: %d' % seed)

    ma = MA.MemeticAlgorithm(file_path=fpath, csv_pd=csv_pd)

    print('min_jobs:', ma.min_jobs)
    print('min_makespan:', ma.min_makespan)

    min_makespan_each_gen_list = ma.search()
    csv_pd[str(seed)] = min_makespan_each_gen_list
    print('min_jobs:', ma.min_jobs)
    print('min_makespan:', ma.min_makespan)
    return csv_pd
# ================================================

if __name__ == "__main__":
    # loggin format
    FORMAT = '%(asctime)s %(levelname)s: %(message)s'
    logging.basicConfig(level=logging.INFO, filename='rotg.log', filemode='w', format=FORMAT)

    print('1. MemeticAlgorithm')

    choice = '3'
    while choice not in ['1', '2', '3']:
        choice = input('輸入錯誤，請輸入要用哪種演算法訓練：')

    if choice == '1':

        mypath = './PFSP_benchmark_data_set/'
        benchmarks = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        print(benchmarks)
        benchmarks.reverse()


        for benchmark in benchmarks:
            logging.info('benchmark: ' + benchmark)

            for seed in range(20):

                random.seed(seed)
                logging.info('seed: %d' % seed)

                ma = MA.MemeticAlgorithm(file_path=mypath + benchmark)


                print('min_jobs:', ma.min_jobs)
                print('min_makespan:', ma.min_makespan)
                logging.info('min_makespan: %d' % ma.min_makespan)

                ma.search()
                print('min_jobs:', ma.min_jobs)
                print('min_makespan:', ma.min_makespan)

                # 001 011 021 031 041
                file = open("./TA021.txt", 'w+')
                ans_list = ma.min_jobs
                for i in ans_list:
                    print("{0} ".format(i), end="", file=file)

    if choice == '2':

        mypath = './PFSP_benchmark_data_set/'
        random.seed(11)
        ma = MA.MemeticAlgorithm(file_path=mypath + 'tai20_10_1.txt')

        print('min_jobs:', ma.min_jobs)
        print('min_makespan:', ma.min_makespan)

        ma.search()

        print('min_jobs:', ma.min_jobs)
        print('min_makespan:', ma.min_makespan)

        # 001 011 021 031 041
        # file = open("./TA021.txt", 'w+')
        # ans_list = ma.min_jobs
        # for i in ans_list:
        #     print("{0} ".format(i), end="", file=file)

    if choice == '3':

        mypath = './PFSP_benchmark_data_set/'
        benchmarks = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        print(benchmarks)
        benchmarks.reverse()

        for benchmark in benchmarks:

            logging.info('benchmark: ' + benchmark)
            pool = mp.Pool(mp.cpu_count())
            csv_pd = pd.DataFrame()

            seed_range = 20
            input_list = [(seed, str(mypath + benchmark)) for seed in range(seed_range)]

            results = pool.starmap_async(task, input_list)
            pool.close()
            pool.join()
            results = results.get()

            results_df = pd.concat(results, sort=True, axis=1)
            results_df.to_csv(benchmark[:-3] + 'csv', index=False)





        
