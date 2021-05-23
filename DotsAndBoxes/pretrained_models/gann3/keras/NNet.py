from .DotsAndBoxesNNet import DotsAndBoxesNNet as onnet
from NeuralNet import NeuralNet
from utils import *
import argparse
import os
import shutil
import time
import random
import numpy as np
import math
import sys
import pygad.kerasga
import pygad
import tensorflow.keras

sys.path.append('../..')


# 可以使用dot的dictionary
args = dotdict({
    'lr': 0.001, # 0.001
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': True,
    'num_channels': 32
})

data_inputs = any
data_outputs =any
keras_ga = any
model = any

class NNetWrapper(NeuralNet):
    def __init__(self, game):
        self.nnet = onnet(game, args)  # 把遊戲和args傳進DotsAndBoxesNNet裡
        self.board_x, self.board_y = game.getBoardSize()  # 取得盤面大小並初始化
        self.action_size = game.getActionSize()  # 取得走步種數
        self.game = game

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        input_boards, target_pis, target_vs = list(zip(*examples))
        input_boards = np.asarray(input_boards)
        # print(target_pis)
        # decode
        input_decode_boards = []
        input_decode_p = []
        for i in range(0, len(input_boards)):
            input_decode_boards.append(self.game.boardDecode(input_boards[i]))
            input_decode_p.append(self.pDecode(target_pis[i]))
        input_decode_boards = np.array(input_decode_boards, dtype='int8')
        # input_decode_p = np.array(input_decode_p , dtype = 'float32')

        target_pis = np.asarray(input_decode_p)
        target_vs = np.asarray(target_vs)
    
        # self.nnet.model.fit(x = input_decode_boards, y = [target_pis, target_vs], batch_size = args.batch_size, epochs = args.epochs)
        global data_inputs, data_outputs, model
        model = self.nnet.model
        data_inputs = input_decode_boards
        data_outputs = [target_pis, target_vs]
        train_by_gann()

    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        # preparing input
        board = board[np.newaxis, :, :]

        # run
        pi, v = self.nnet.model.predict(board)

        #print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return pi[0], v[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print(
                "Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise("No model in path {}".format(filepath))
        self.nnet.model.load_weights(filepath)

    def pEncode(self, p):
        index = []
        value = []
        index.append(len(p))
        value.append(0)
        for i in range(len(p)):
            if p[i] != 0:
                index.append(i)
                value.append(float(p[i]))
        index = np.array(index, dtype="uint8")
        value = np.array(value, dtype="float32")
        re = []
        re.append(index)
        re.append(value)
        re = np.array(re, dtype=object)
        return re

    def pDecode(slef, p):
        re = [0.0 for i in range(p[0][0])]
        for i in range(1, len(p[0])):
            re[p[0][i]] = p[1][i]

        return re

def train_by_gann():
    global data_inputs, data_outputs, keras_ga, model
    # pygad train
    # Create an instance of the pygad.kerasga.KerasGA class to build the initial population.
    keras_ga = pygad.kerasga.KerasGA(
        model=model, num_solutions=30)

    # Prepare the PyGAD parameters. Check the documentation for more information: https://pygad.readthedocs.io/en/latest/README_pygad_ReadTheDocs.html#pygad-ga-class
    num_generations = 200  # Number of generations.
    # Number of solutions to be selected as parents in the mating pool.
    num_parents_mating = 25
    # Initial population of network weights.
    initial_population = keras_ga.population_weights
    parent_selection_type = "tournament"  # Type of parent selection.
    K_tournament = 12
    crossover_type = "uniform"  # Type of the crossover operator.
    mutation_type = "swap"  # Type of the mutation operator.
    # Percentage of genes to mutate. This parameter has no action if the parameter mutation_num_genes exists.
    mutation_percent_genes = 50
    # Number of parents to keep in the next population. -1 means keep all parents and 0 means keep nothing.
    keep_parents = 0

    # Create an instance of the pygad.GA class
    ga_instance = pygad.GA(num_generations=num_generations,
                            num_parents_mating=num_parents_mating,
                            initial_population=initial_population,
                            fitness_func=fitness_func,
                            parent_selection_type=parent_selection_type,
                            K_tournament=K_tournament,
                            crossover_type=crossover_type,
                            mutation_type=mutation_type,
                            mutation_percent_genes=mutation_percent_genes,
                            keep_parents=keep_parents,
                            on_generation=callback_generation)
    # Start the genetic algorithm evolution.
    ga_instance.run()

    # Returning the details of the best solution.
    solution, solution_fitness, solution_idx = ga_instance.best_solution()

    # Fetch the parameters of the best solution.
    best_solution_weights = pygad.kerasga.model_weights_as_matrix(model=model,
                                                                weights_vector=solution)
    model.set_weights(best_solution_weights)
    predictions = model.predict(data_inputs)
    # print("Predictions : \n", predictions)

    # Calculate the categorical crossentropy for the trained model.
    cce = tensorflow.keras.losses.CategoricalCrossentropy()
    mse = tensorflow.keras.losses.MeanSquaredError()
    print("Categorical Crossentropy : ", cce(data_outputs[0], predictions[0]).numpy())
    print("MeanSquaredError : ", mse(data_outputs[1], predictions[1]).numpy())

    # Calculate the classification accuracy for the trained model.
    ca = tensorflow.keras.metrics.CategoricalAccuracy()
    ca.update_state(data_outputs[0], predictions[0])
    accuracy = ca.result().numpy()
    print("Accuracy : ", accuracy)

def fitness_func(solution, sol_idx):
    global data_inputs, data_outputs, keras_ga, model

    model_weights_matrix = pygad.kerasga.model_weights_as_matrix(model=model,
                                                                weights_vector=solution)

    model.set_weights(weights=model_weights_matrix)

    predictions = model.predict(data_inputs)

    cce = tensorflow.keras.losses.CategoricalCrossentropy()
    mse = tensorflow.keras.losses.MeanSquaredError()
    solution_fitness = 1.0 / (cce(data_outputs[0], predictions[0]).numpy() + 0.00000001 + mse(data_outputs[1], predictions[1]))

    return solution_fitness

def callback_generation(ga_instance):
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))