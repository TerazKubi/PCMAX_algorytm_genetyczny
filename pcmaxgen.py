import random
import time

class PCmaxGen:
    def __init__(self, file_name, pop_count, m_prob, a):
        self.task_times = []
        self.pop_count = pop_count #ile osobnikow w populacji
        #self.max_gen = max_gen #ile generacji

        with open(file_name, 'r') as plik:
            self.proc_num = int(plik.readline())#liczba procesorow
            self.task_num = int(plik.readline())#liczba taskow/procesow

            for line in plik:
                self.task_times.append(int(line))#lista z dlugosciami procesow

        self.a = a

        #ile najlepszych osobnikow jest wybierane jako parents
        self.num_of_best = int(self.pop_count * self.a) #20%

        self.mutate_prob = m_prob #%

        self.first_pop_count = 10000

    def show_info(self):
        print("Informacje: ")
        print("Lista zadan: ", self.task_times)
        print("Liczba procesorow: ", self.proc_num)
        print("Liczba procesow/zadan: ", self.task_num)
        print("Liczba wybieranych rodzicow: ", self.a * 100, "%")
        print("Liczba osobników w populacji: ", self.pop_count)

        print("\n")

    def solution_generator(self): #losowo generuje rozwiązanie problemu
        coded_solution = [random.randint(1, self.proc_num) for x in range(0, len(self.task_times))]

        return self.evaluate(coded_solution)

    def first_pop(self):
        pop = {}
        for x in range(0, self.first_pop_count):
            pcmax, cod_sol = self.solution_generator()
            pop.update({str(x): [pcmax, cod_sol]})

        #print(sorted(pop.values()))
        return sorted(pop.values())

    def next_gen(self, parents):
        next_gen = []

        for x in range(0, int(self.pop_count / 2)):
            p1 = random.randint(0, len(parents) - 1)
            p2 = random.randint(0, len(parents) - 1)
            k1, k2 = self.cross_parents(parents[p1][1], parents[p2][1])

            k1 = self.evaluate(k1)
            k2 = self.evaluate(k2)
            next_gen.append(k1)
            next_gen.append(k2)

        return sorted(next_gen)

    def cross_parents(self, parent1, parent2):
        #wybranie indexu crosowania rodzicow l = np srodek
        #l = int(len(parent1) / 2)
        l = random.randint(1, len(parent1)-2)
        c1 = parent1[:l] + parent2[l:]
        c2 = parent2[:l] + parent1[l:]

        #l2 = random.randint(1, len(parent1)-2)
        #c1 = c1[:l2] + c2[l2:]
        #c2 = c2[:l2] + c1[l2:]
        #====== mutate childs =========
        #wybranie indexow do zamiany genow
        c1 = self.mutate(c1)
        c2 = self.mutate(c2)

        # first child
        x = random.randint(0,100)
        if x < self.mutate_prob:
            c1 = self.mutate(c1)

        # second child
        x = random.randint(0, 100)
        if x < self.mutate_prob:
            c2 = self.mutate(c2)


        return c1, c2

    def mutate(self, child):
        g1 = random.randint(0, len(child) - 1)
        #g2 = random.randint(0, len(child) - 1)
        #temp = child[g1]
        #child[g1] = child[g2]
        #child[g2] = temp
        child[g1] = random.randint(1, self.proc_num)
        return child

    def evaluate(self, coded_sol): #oblicza pcmax z zakodowanego rozwiązania
        solution = {}

        # przygotowanie procesorow / slownika / dictionary
        for x in range(1, self.proc_num + 1):
            solution.update({str(x): 0})

        for x in range(0, len(coded_sol)):
            solution[str(coded_sol[x])] += self.task_times[x]

        return [max(solution.values()), coded_sol]

    def algo(self):
        pop = self.first_pop()
        best_solution = pop[0][0]

        gen_count = 1
        end = int(time.time()) + 300
        while(time.time() <= end):
            parents = pop[:self.num_of_best]
            pop = self.next_gen(parents)

            if gen_count % 100 == 0:
                print(gen_count)

            if pop[0][0] < best_solution:
                best_solution = pop[0][0]
                print(str(gen_count) + ": " + str(best_solution))
            gen_count += 1

        print("Koncowe najlepsze rozwiazanie: ", best_solution)
