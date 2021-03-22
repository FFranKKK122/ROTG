import tool
import simulatedAnnealing as SA
import tabuSearch as Tabu
import pandas as pd
from os import listdir
from os.path import isfile, join

if __name__ == "__main__":
    print('1. iterative improvement')
    print('2. simulated annealing')
    print('3. tabu search')
    print('4. simulated annealing 以選擇之參數每個測資跑20次最小makesspan')
    print('5. simulated annealing 使用tai20_5_1.txt 計算各種參數組合的最小makesspan')

    choice = input('請輸入要用哪種演算法訓練：')
    while choice not in ['1', '2', '3', '4', '5']:
        choice = input('輸入錯誤，請輸入要用哪種演算法訓練：')

    if choice == '1':
        pass
    elif choice == '2':
        
        SA_search = SA.SimulatedAnnealing(
            100, 0.95, 40, 0, './PFSP_benchmark_data_set/tai20_5_1.txt')
        SA_search.search()
        _tool = tool.Tool()
        # 畫出此次search makespan的收斂圖
        _tool.plot([int(e) for e in range(
            len(SA_search.makespan_array))], SA_search.makespan_array)


    elif choice == '3':
        mypath = './PFSP_benchmark_data_set/'
        benchmarks = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        df_experiment_result = pd.DataFrame()
        for benchmark in benchmarks:
            Tabu_search = Tabu.TabuSearch(benchmark_path = mypath + benchmark)
            Tabu_search.experiment()
            benchmark = benchmark.replace('.txt', '')
            df_experiment_result[benchmark] = Tabu_search.experiment_result

        df_experiment_result.to_csv('Tabu_experiment_result.csv', header=True, index=False)


        

    elif choice == '4':
        mypath = './PFSP_benchmark_data_set'
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
        rand_seeds = [int(e) for e in range(20)]
        df = pd.DataFrame()
        df['rand_seed'] = rand_seeds
        for file_name in onlyfiles:
            min_makespam = []
            for rand_seed in rand_seeds:
                print(file_name, rand_seed)
                SA_search = SA.SimulatedAnnealing(
                    100, 0.95, 40, rand_seed, mypath+'/'+file_name)
                SA_search.search()
                min_makespam.append(SA_search.min_makespan)
            df[file_name] = min_makespam
        df.to_csv('SA_diff_file_test_20_times.csv', header=True, index=False)

    elif choice == '5':
        temperture = [50, 100, 150, 200, 250]
        alpha = [0.8, 0.85, 0.9, 0.95, 0.99]
        epoch_len = [20, 30, 40, 50, 60]
        df = pd.DataFrame()
        df['alpha'] = alpha
        for T in temperture:
            for EL in epoch_len:
                min_makespam = []
                for A in alpha:
                    print(T, E, A)
                    SA_search = SA.SimulatedAnnealing(
                        T, A, EL, 0, './PFSP_benchmark_data_set/tai20_5_1.txt')
                    SA_search.search()
                    min_makespam.append(SA_search.min_makespan)
                df[str(T)+'_'+str(EL)] = min_makespam
        df.to_csv('SA_diff_params.csv', header=True, index=False)
