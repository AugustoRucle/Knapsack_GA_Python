import pygubu
import random
import numpy as np
import tkinter as tk 
import matplotlib.pyplot as plt
from tkinter import messagebox as msg

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
        amount_generation = int(self.builder.get_variable('amount_generation').get())  

        if(self.get_values_main(size_chromosome, main_weight, amoun_population)):
            msg.showerror("Error", "Valores faltantes")
        else:
            if(main_weight >= 300 ):
                self.start_generic_algorithms(size_chromosome, main_weight, amoun_population, amount_generation)
            else:
                msg.showwarning("Warning","Ingresa una cantidad mayor a 100")

    def get_values_main(self, size_chromosome, main_weight, amoun_population):
        if(size_chromosome == 0 or main_weight == 0 or amoun_population == 0):
            return True
        else:
            return False

    def create_population(self, size_chromosome, main_weight):
        return np.random.randint(low=10, high=main_weight-100, size=size_chromosome)

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
                # print('ALL GENE: {}'.format(individuals))
                # print('\n')
                # print('ALL-GENE-2: {}'.format(individuals[i]))
                # print('\n')
                gen = individuals[i][j]
                # print('Gen: {} \n'.format(gen))
                if(gen == 1):
                    individual_converted.append(population[j])
            individuals_converted_list.append(( individuals[i], individual_converted ))
        return individuals_converted_list
        
    def start_generic_algorithms(self, size_chromosome, main_weight, amoun_population, amount_generation = 100):
        flag, generation, i = True, 0, 0
        list_fitness = []
        #Initial population
        population = self.create_population(size_chromosome, main_weight)

        
        individuals = self.create_individuals(size_chromosome, amoun_population)

        while(flag and (i < amount_generation)):
            i += 1
            #Fitness function
            individuals = self.get_individuals_converted(population, individuals)
            individuals = self.get_fitness(individuals, main_weight, sum(population))
            individuals.sort(key = lambda x: x[1], reverse=True)   

            # print('Indivuals')
            # # self.print_indivuals(individuals)
            # print(individuals)
            # print('\n\n')

            #Crossover
            children = self.crossover(individuals)

            # print('\n\nHijos')
            # print(children)

            #Mutacion
            children = self.mutacion(children, 0.8, 0.8)
            
            # print('\n\nHijos-mutados')
            # print(children)

            children = self.get_individuals_converted(population, children)
            children = self.get_fitness(children, main_weight, sum(population))

            # print('Hijos con fitness')
            # # self.print_indivuals(children)
            # print(children)
            # print('\n\n')

            individuals = individuals + children

            individuals.sort(key = lambda x: x[1], reverse=True)   

            individuals = individuals[:10]

            list_fitness.append(individuals[0][1])
            
            if(individuals[0][1] >= 0.8):
                flag = False
            else:
                individuals = list(map(lambda x: x[0], individuals))

            # print('\nPoblacion con fitness-ordenados')
            # # self.print_indivuals(individuals)
            # print(individuals)

        print('Better fitness: {}'.format(max(list_fitness)))
        print('Generacions: {}'.format(generation))
        print('s: {}'.format(len(list_fitness)))
        print('Termine')
        self.draw_chart(list_fitness, generation)
    def get_fitness(self, indivuals, main_weight, sum_population):
        amount_indivuals = len(indivuals)
        individuals_fitness = []
        for i in range(amount_indivuals):
            sum_indivuals = sum(indivuals[i][1])
            if(sum_indivuals <= main_weight):
                fitness = 1 - (((main_weight - sum_indivuals) / main_weight)**0.5)
            else:
                dividend = sum_indivuals - main_weight
                divisor = max(main_weight, (sum_population - main_weight))
                quotient = ((dividend / divisor) ** 0.0625)
                fitness = 1 - quotient     

            # individuals_fitness.append((indivuals[i][0], indivuals[i][1], fitness))
            individuals_fitness.append((indivuals[i][0], fitness))
        return individuals_fitness
    
    def crossover(self, list_individuals):
        LENGTH_LIST = len(list_individuals)
        children = []

        for i in range (LENGTH_LIST-1):
            binaries_father, fitness_father = list_individuals[i]

            j = i + 1

            while j < LENGTH_LIST:
                probability_random = random.random()
                if(fitness_father > probability_random):
                    # print('\nApareamiento')
                    binaries_mother, fitness_mother = list_individuals[j]
                    # print('P_f:{} , F_f: {}'.format(binaries_father, fitness_father))
                    # print('P_m:{} , F_m: {}'.format(binaries_mother, fitness_mother))
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

    def mutacion(self, _lista_hijos_binarios, probabilidad_mutar_individuo, probabilidad_mutar_gen):
        lista_hijos_binarios, TAMANIO_LISTA_HIJOS, lista_hijos_binarios_mutados = np.copy(_lista_hijos_binarios), len(_lista_hijos_binarios), []

        for i in range(TAMANIO_LISTA_HIJOS):
            random_probabilidad_mutacion = random.random()
            if(probabilidad_mutar_individuo > random_probabilidad_mutacion):
                #print("Hm: {}".format(lista_hijos_binarios[i]))
                list_individuo = list(map(lambda individuo: self.mutar_gen(individuo, probabilidad_mutar_gen), lista_hijos_binarios[i]))
                # print('LHC: {}'.format(list_individuo))
                list_individuo = ''.join(str(individuo) for individuo in list_individuo)
                list_individuo = list(map(int, list_individuo))
                lista_hijos_binarios_mutados.append(np.asarray(list_individuo))
                #print('LHC: {}'.format(lista_hijos_binarios_mutados))
            else:
                list_individuo = list(map(int, lista_hijos_binarios[i]))
                lista_hijos_binarios_mutados.append(np.asarray(list_individuo))

        #print("Mutados: {}".format(lista_hijos_binarios_mutados))

        return lista_hijos_binarios_mutados
    
    def mutar_gen(self, individuo, probabilidad_mutar_gen):
        random_probabilidad = random.random()
        #print('Individuo:{}'.format(individuo))
        #print("PG:{}, RP:{}".format(probabilidad_mutar_gen, random_probabilidad))
        individuo = int(individuo)
        if(probabilidad_mutar_gen > random_probabilidad):
            if individuo == 0:
                #print("Ahora es: 1")
                return 1
            else: 
                #print("Ahora es: 0")
                return 0
        #print("Lo mismo: {}".fomat(individuo))
        return individuo   

    def mutation(self, least_value, indivuals):
        
        # print('\n\nIndivuals actuales')
        # print(indivuals)

        for i in range(len(least_value)):
            if(random.random() > 0.6):
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

    def print_indivuals(self, indivuals):
        length_indivuals = len(indivuals)
        for i in range(length_indivuals):
            binaries, fitness = indivuals[i]
            # print('P:{}, F: {}'.format(binaries, fitness))

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

if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root)
    root.mainloop()