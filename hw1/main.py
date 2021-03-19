import tool
import simulatedAnnealing as SA
import pandas as pd 

if __name__ == "__main__":
    print('1. iterative improvement')
    print('2. simulated annealing')
    print('3. tabu search')

    choice = input('請輸入要用哪種演算法訓練：')
    while choice not in ['1', '2', '3']:
        choice = input('輸入錯誤，請輸入要用哪種演算法訓練：')

    if choice == '1':
        pass
    elif choice == '2':
        temperture = [50, 100, 150, 200, 250]
        alpha = [0.8, 0.85, 0.9, 0.95, 0.99]
        alpha = [0.8]
        epoch_len = [20, 30, 40, 50, 60]
        for T in temperture:
            for EL in epoch_len:
                min_makespam = []
                for A in alpha:
                    SA_search = SA.SimulatedAnnealing(T, A, EL, 0)
                    SA_search.search()
                    min_makespam.append(SA_search.min_makespan)
                df = pd.DataFrame()
                df['alpha'] = alpha
                df['makespan'] = min_makespam
                df.to_csv('SA_test/'+str(T)+'_'+str(EL)+'.csv',header=False,index=False)

    elif choice == '3':
        pass
