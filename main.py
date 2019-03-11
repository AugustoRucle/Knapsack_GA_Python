import pygubu
import random
import numpy as np
import tkinter as tk 
import matplotlib.pyplot as plt
from tkinter import messagebox as msg
import matplotlib.pyplot as plt

sumador = []

class Application:
    def __init__(self, master):

        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('UI.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('AG', master)
        
        builder.connect_callbacks(self)

    def start(self):
        size_chromosome = int(self.builder.get_variable('size_knapsack').get())
        main_weight = int(self.builder.get_variable('main_weight').get())
        amoun_population = int(self.builder.get_variable('amount_population').get())  

        if(self.get_values_main(size_chromosome, main_weight, amoun_population)):
            msg.showerror("Error", "Valores faltantes")
        else:
            if(main_weight >= 300 ):
                self.start_generic_algorithms(size_chromosome, main_weight, amoun_population)
            else:
                msg.showwarning("Warning","Ingresa una cantidad mayor a 100")

    def get_values_main(self, size_chromosome, main_weight, amoun_population):
        if(size_chromosome == 0 or main_weight == 0 or amoun_population == 0):
            return True
        else:
            return False

    def create_population(self, size_chromosome, main_weight):
        return np.random.randint(low=1, high=main_weight*0.5, size=size_chromosome)

    def create_individuals(self, size_chromosome, amoun_population):
        flag, exit_zero = True, False
        array = []
        while (flag):
            array =  np.random.randint(2, size=(amoun_population, size_chromosome))
            exit_zero = False
            for i in range(len(array)):
                sum_array = sum(array[i])
                if(sum_array == 0):
                    exit_zero = True
            if(exit_zero):
                flag = True
            else:
                flag = False
                    
        return array

    def get_individuals_converted(self, population, individuals):
        amount_indivuals = len(individuals)
        lenght_population = len(population)
        individuals_converted_list = []

        for i in range(amount_indivuals):
            individual_converted = []
            for j in range(lenght_population):
                gen = individuals[i][j]
                if(gen == 1):
                    individual_converted.append(population[j])
            individuals_converted_list.append(( individuals[i], individual_converted ))
        return individuals_converted_list
        
    def start_generic_algorithms(self, size_chromosome, main_weight, amoun_population):
        bandera, generation = True, 0
        list_fitness = []
        #Initial population
        population = self.create_population(size_chromosome, main_weight)
        individuals = self.create_individuals(size_chromosome, amoun_population)

        while (bandera):
            generation += 1
            #Fitness function
            individuals = self.get_individuals_converted(population, individuals)
            individuals = self.get_fitness(individuals, main_weight, sum(population))
            individuals.sort(key = lambda x: x[2], reverse=True)   

            list_fitness.append(individuals[0][2])

            if(individuals[0][2] >= 0.8):
                bandera = False
            else:
                # print('Indivuals')
                # print(individuals)

                #Selection
                individuals = individuals[:3]

                # print('\n\nSeleccition')
                # print(individuals)
                
                #Crossover
                aux_indivuals = self.crossover(individuals)

                #Crossover 
                individuals = self.mutation(individuals[2][0], aux_indivuals)

                # print('Indivuals select:')
                # print(individuals)

                #Get fitness of next generations
                # individuals = self.get_individuals_converted(population, individuals)
                # individuals = self.get_fitness(individuals, main_weight, sum(population))

                # print('Indivuals fitness')
                # print(individuals)
        
        self.draw_chart(list_fitness, generation)
        print('Generacions: {}'.format(generation))
        print('Termine')

    def get_fitness(self, indivuals, main_weight, sum_population):
        amount_indivuals = len(indivuals)
        individuals_fitness = []
        for i in range(amount_indivuals):
            sum_indivuals = sum(indivuals[i][1])
            #print(sum_indivuals)
            sumador.append(sum_indivuals)
            if(sum_indivuals <= main_weight):
                fitness = 1 - (((main_weight - sum_indivuals) / main_weight)**0.5)
            else:
                dividend = sum_indivuals - main_weight
                divisor = max(main_weight, (sum_population - main_weight))
                quotient = ((dividend / divisor) ** 0.0625)
                fitness = 1 - quotient     

            individuals_fitness.append((indivuals[i][0], indivuals[i][1], fitness))
            #print(indivuals[i][1])
            #print(sumador)
        return individuals_fitness
    
    def crossover(self, indivuals):
        aux_indivuals = []
        first_indivual = indivuals[0][0]
        second_indivual = indivuals[1][0]
        third_indivual = np.concatenate((first_indivual[:8], second_indivual[8:]), axis = 0)

        aux_indivuals.append(first_indivual)
        aux_indivuals.append(third_indivual)

        return aux_indivuals

    def mutation(self, least_value, indivuals):
        
        #print('\n\nIndivuals actuales')
        #print(indivuals)

        for i in range(len(least_value)):
            if(random.random() < 0.6):
                if(least_value[i] == 0):
                    least_value[i] = 1
                else:
                    least_value[i] = 0

        for i in range(len(indivuals)):
            for j in range(len(least_value)):
                if(random.random() > 0.5):
                    if(indivuals[i][j] == 0):
                        indivuals[i][j] = 1
                    else:
                        indivuals[i][j] = 0

        indivuals.append(least_value)

        return indivuals

    def draw_chart(self, list_fitness, amount_generation):
        amount_generation = len(list_fitness)
        list_generation = []

        for i in range(amount_generation):
            list_generation.append(i+1)

        valor_minimo = min(list_media_mejor + list_media_peor + list_media)
        valor_maximo = max(list_media_mejor + list_media_peor + list_media)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.title('Valor de la media')
        plt.xlabel('Generaciones')
        plt.ylabel('Fitness')
        ax.set_ylim(bottom=value_min, top=value_max)
        plt.plot(list_generation, list_fitness, 'go-')
        plt.legend(loc='upper left')
        plt.show()

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()