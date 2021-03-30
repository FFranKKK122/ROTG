import tool
import MemeticAlgorithm as MA
import pandas as pd
from os import listdir
from os.path import isfile, join

if __name__ == "__main__":
    print('1. MemeticAlgorithm')

    choice = input('請輸入要用哪種演算法訓練：')
    while choice not in ['1']:
        choice = input('輸入錯誤，請輸入要用哪種演算法訓練：')

    if choice == '1':
        ma = MA.MemeticAlgorithm(file_path='./PFSP_benchmark_data_set/tai20_5_1.txt')
        df = ma.search()
        min = 999999999
        ind = 0
        
        for i in range(len(df.index)):
            if(df['makespans'][i] < min):
                min = df['makespans'][i]
                ind = i

        # 001 011 021 031 041
        file = open("./TA001.txt", 'w+')
        ans_list = df['jobs'][ind]
        for i in ans_list:
            print("{0} ".format(i), end="", file=file)



        
