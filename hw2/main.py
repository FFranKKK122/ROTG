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
        ma = MA.MemeticAlgorithm()
        print(ma.population)
        
