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
        builder.add_from_file('UI_3.ui')

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
        return np.random.randint(low=1, high=main_weight-100, size=size_chromosome)

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
        bandera, generation, i = True, 0, 0
        list_fitness, list_fiteness_wrong, list_fitness_mean = [], [], []
        #Initial population
        population = self.create_population(size_chromosome, main_weight)
        individuals = self.create_individuals(size_chromosome, amoun_population)

        while (bandera and i < 100):
            generation += 1
            #Fitness function
            individuals = self.get_individuals_converted(population, individuals)
            individuals = self.get_fitness(individuals, main_weight, sum(population))
            individuals.sort(key = lambda x: x[2], reverse=True)   

            #Selection
            better_indivuals, wrong_indivuals =  self.selection(individuals)

            #Crossover better
            children = self.crossover(better_indivuals)

            if(len(children) > 0):
                children = self.get_individuals_converted(population, children)
                children = self.get_fitness(children, main_weight, sum(population))
            

            if(len(wrong_indivuals) > 0):
                wrong_indivuals = self.mutation(wrong_indivuals)
                wrong_indivuals = self.get_individuals_converted(population, wrong_indivuals)
                wrong_indivuals = self.get_fitness(wrong_indivuals, main_weight, sum(population))
            

            
            better_indivuals = better_indivuals + children
            individuals = better_indivuals + wrong_indivuals
            individuals.sort(key = lambda x: x[2], reverse=True)   
            aux_individuals = list(map(lambda x: x[2], individuals))

            # print('Better: {}'.format(better_indivuals))
            # print('Wrong: {}'.format(wrong_indivuals))

            list_fitness.append(max(aux_individuals))
            list_fiteness_wrong.append(min(aux_individuals))
            list_fitness_mean.append(sum(aux_individuals)/len(aux_individuals))

            individuals = individuals[0:20]

            if(individuals[0][2] >= 0.8):
                print('Better: {}'.format(individuals[0]))
                bandera = False
            else:
                individuals = list(map(lambda x: x[0], individuals))

            i += 1

        self.draw_chart_all(list_fitness_mean, list_fitness, list_fiteness_wrong, generation)
        print('Generacions: {}'.format(generation))
        print('Termine')

    def get_fitness(self, indivuals, main_weight, sum_population):
        amount_indivuals = len(indivuals)
        individuals_fitness = []
        for i in range(amount_indivuals):
            sum_indivuals = sum(indivuals[i][1])
            #print(sum_indivuals)
            if(sum_indivuals <= main_weight):
                fitness = 1 - (((main_weight - sum_indivuals) / main_weight)**0.5)
            else:
                dividend = sum_indivuals - main_weight
                divisor = max(main_weight, (sum_population - main_weight))
                quotient = ((dividend / divisor) ** 0.0625)
                fitness = 1 - quotient     

            individuals_fitness.append((indivuals[i][0], indivuals[i][1], fitness))
        return individuals_fitness
    
    def selection(self, indivuals):
        cantidad_indivios = len(indivuals)
        better_indivuals, wrong_indivuals = [], []
        
        for i in range(cantidad_indivios-3):
            
            better, wrongs = self.selection_three_indivuals(indivuals, i)

            better_indivuals.append(better)

            for i in range(len(wrongs)):
                wrong_indivuals.append(wrongs[i])

            i += 3
        # print('Better: {}\n'.format(better_indivuals))
        # print('Wrong: {}'.format(wrong_indivuals))

        return better_indivuals, wrong_indivuals

    def selection_three_indivuals(self, indivuals, i ):

        aux_individuals, iteratior = [], i

        for j in range (3):
            aux_individuals.append(indivuals[iteratior])
            iteratior += 1

        aux_individuals.sort(key = lambda x: x[2], reverse=True)


        # print('Better: {}'.format(aux_individuals[0]))
        # print('Wronger: {}'.format(aux_individuals[1:]))
        # print('\n')

        return aux_individuals[0], aux_individuals[1:]

    def crossover(self, list_individuals):
        LENGTH_LIST, j = len(list_individuals), 0
        children = []

        for i in range (LENGTH_LIST-1):
            
            binaries_father, _, fitness_father = list_individuals[i]
            j = i + 1

            while j < LENGTH_LIST:
                if(fitness_father > random.random()):
                    binaries_mother, _, _ = list_individuals[j]
                    first_children, second_children = self.get_children(binaries_father, binaries_mother)
                    children.append(first_children); children.append(second_children)
                j += 1
        
        return children

    def get_children(self, binarie_father, binarie_mother):
        first_children, second_children, counter, i = [], [], 0, 0
        list_point_crossover = self.get_point_crossover(len(binarie_father))
        leght_size_pc = len(list_point_crossover) + 1

        while i < leght_size_pc:
            j = 0
            if(i == ( leght_size_pc - 1 )):
                part_father, part_mother = binarie_father[counter:], binarie_mother[counter:]
                j = 1
            else:
                jump = counter + list_point_crossover[i]
                part_father, part_mother = binarie_father[counter:jump], binarie_mother[counter:jump]
            
            counter = counter + list_point_crossover[i - j]

            # print('c1: {}, c2: {}'.format(part_father, part_mother))

            if(((i+1) % 2) != 0):
                # first_children, second_children = first_children + self.convert(part_father), second_children + self.convert(part_mother) 
                # first_children += part_father; second_children += part_mother
                first_children = np.append(first_children, part_father); second_children = np.append(second_children, part_mother)
            if(((i+1) % 2) == 0):
                # first_children, second_children = first_children + self.convert(part_mother), second_children + self.convert(part_father) 
                # first_children += part_mother; second_children += part_father
                first_children = np.append(first_children, part_mother); second_children = np.append(second_children, part_father)
            i = i + 1

        # print("Hijos:")
        # print('uno: {}, dos: {} '.format(first_children, second_children))

        return first_children, second_children

    def get_point_crossover(self, AMOUNT_CROMOSOMA):
        amount_point_crossover, counter_cut, i = random.randint(1, 5), 0, 0

        list_point_crossover = []

        while i < amount_point_crossover:
            length_cut = random.randint(3, AMOUNT_CROMOSOMA-10)
            # print('Lenght_cut: {}'.format(length_cut))
            counter_cut = counter_cut + length_cut
            difference = AMOUNT_CROMOSOMA - counter_cut

            if(difference > 0 and i < amount_point_crossover):
                list_point_crossover.append(length_cut)
            else:
                i = amount_point_crossover
            
            i = i + 1

        # print('# cruzes: {}'.format(amount_point_crossover))
        # print('Cantidad de cruza: {}'.format(list_point_crossover))

        return list_point_crossover

    def mutation(self, indivuals):

        aux_individuals = []

        for i in range(len(indivuals)):
            binarios, _, fitness = indivuals[i]
            size_candidato = len(binarios)
            for j in range(size_candidato):
                position = random.randint(0,size_candidato-1)
                if(0.6 > random.random()):
                    if(binarios[position] == 0):
                        binarios[position] = 1
                    else:
                        binarios[position] = 0

            aux_individuals.append(binarios)

        return aux_individuals

    def draw_chart(self, list_fitness, amount_generation):
        amount_generation = len(list_fitness)
        list_generation = []

        for i in range(amount_generation):
            list_generation.append(i+1)

        value_min = min(list_fitness)
        value_max = max(list_fitness)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.title('Valor de la media')
        plt.xlabel('Generaciones')
        plt.ylabel('Fitness')
        ax.set_ylim(bottom=value_min, top=value_max)
        plt.plot(list_generation, list_fitness, 'go-')
        plt.legend(loc='upper left')
        plt.show()

    def draw_chart_all(self, list_media, list_media_mejor, list_media_peor, CANTIDAD_GENERACIONES):
        lista_generaciones = []

        #print('Cantidad:{}, CANTIDAD_MEDIA: {} '.format(CANTIDAD_GENERACIONES, CANTIDAD_MEDIA))

        for i in range(CANTIDAD_GENERACIONES):
            lista_generaciones.append(i+1)

        # print('CG: {}'.format(lista_generaciones))

        #print('Min: {}'.format(min(list_media_mejor + list_media_peor + list_media)))
        #print('Max: {}'.format(max(list_media_mejor + list_media_peor + list_media)))

        valor_minimo = min(list_media_peor)
        valor_maximo = max(list_media_mejor)

        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.title('Valor de la media')
        plt.xlabel('Generaciones')
        plt.ylabel('Fitness')
        ax.set_ylim(bottom=valor_minimo, top=valor_maximo)
        plt.plot(lista_generaciones, list_media_peor, 'ro-', label='Peores individuos')
        plt.plot(lista_generaciones, list_media_mejor, 'go-', label='Mejores individuos')
        plt.plot(lista_generaciones, list_media,'bo-', label='Promedios individuos')
        plt.legend(loc='upper left')
        plt.show()

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()