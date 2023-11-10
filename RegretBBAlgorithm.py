import numpy as np
import pandas as pd
import math

import stack

class RegretAlgorithm:

    def __init__(self, random_input:bool):
        self.Cmax = 0
        self.L = 1
        self.infinity = math.inf
        self.error = 0
        self.seq = []
        self.random_matrix = random_input
        
        if self.random_matrix == True:
            print('Random NxN Matrix')
            self.matrix_size = int(input('Input N Size: '))
            self.matrix = np.random.uniform(low=1, high=30, size=(self.matrix_size, self.matrix_size))
        elif self.random_matrix == False:
            print('Given NxN Matrix')
            self.matrix = np.array(pd.read_csv(input('Input csv file: '), header = None))
            self.matrix_size = min(len(self.matrix),len(self.matrix[1:]))
            self.matrix = self.matrix[:self.matrix_size,self.matrix_size]
        else:
            print("ERROR: please give bool value")
            self.error = 1
            
        if self.error == 0:
            self.matrix = np.rint(self.matrix)
            self.m = [[[j, i] for i in range(self.matrix_size)] for j in range(self.matrix_size)]
            np.fill_diagonal(self.matrix, self.infinity)
            init_matrix = pd.DataFrame(self.matrix)
            print("\nInitial Matrix:")
            print(init_matrix)
            print("-" * 30)

    def row_col_reduction(self):
        for i in range(0, len(self.matrix[0][:])):
            self.Cmax += min(self.matrix[i, :])
            self.matrix[i, :] -= min(self.matrix[i, :])
        for j in range(0, len(self.matrix[0][:])):
            self.Cmax += min(self.matrix[:, j])
            self.matrix[:, j] -= min(self.matrix[:, j])

        matrix_df = pd.DataFrame(self.matrix)
        print("\nAfter Reduction:")
        print(matrix_df)

    def regret_cal(self):
        list_regret = []
        xy = np.argwhere(self.matrix == 0)

        for i in range(0, len(xy)):
            k = xy[i]
            xx = self.matrix[k[0]][:]
            xx = np.delete(xx, k[1])
            yy = self.matrix[:, k[1]]
            yy = np.delete(yy, k[0])
            r = min(xx)
            c = min(yy)
            list_regret.append(r + c)

        z = np.argmax(list_regret)
        aa = self.m[xy[z][0]][xy[z][1]]

        print(f"\n{self.L}th Job Sequence is Job{aa[0]} -> Job{aa[1]}.")
        print(
            f"When the sequence is assigned, Cmax is {self.Cmax}, and if not, lower bound is {self.Cmax + list_regret[z]}.")

        bb = self.sequencing(aa[0], aa[1])
        self.L += 1

        if not self.L == self.matrix_size:
            print(f"The current sequence is : {self.seq}")
            print(f"\nSubtour {bb} should be prohibited")
            c1, c2 = -1, -1
            for i in range(len(self.m)):
                for j in range(len(self.m)):
                    if (self.m[i][j][0] == bb[0]) and (self.m[i][j][1] == bb[1]):
                        c1 = i
                        c2 = j
            if c1 != -1 and c2 != -1:
                self.matrix[c1][c2] = self.infinity

            matrix_df = pd.DataFrame(self.matrix)
            print("\nAfter Subtour Prohibition:")
            print(matrix_df)

            self.matrix = np.delete(self.matrix, xy[z][0], axis=0)
            self.matrix = np.delete(self.matrix, xy[z][1], axis=1)
            self.m = np.delete(self.m, xy[z][0], axis=0)
            self.m = np.delete(self.m, xy[z][1], axis=1)
            # self.L += 1
            matrix_df = pd.DataFrame(self.matrix)
            print("\nAfter Row/Column Elimination:")
            print(matrix_df)

    def sequencing(self, a_0, a_1):
        front_index = self.matrix_size
        end_index = self.matrix_size

        for i in range(len(self.seq)):
            if self.seq[i][len(self.seq[i]) - 1] == a_0:
                front_index = i
            if self.seq[i][0] == a_1:
                end_index = i

        if front_index != self.matrix_size and end_index != self.matrix_size:
            self.seq[front_index].append(a_1)
            for j in range(len(self.seq[end_index])):
                if j != 0:
                    self.seq[front_index].append(self.seq[end_index][j])
            if end_index < front_index:
                front_index -= 1
            del self.seq[end_index]
            return [self.seq[front_index][len(self.seq[front_index]) - 1], self.seq[front_index][0]]

        if front_index != self.matrix_size and end_index == self.matrix_size:
            self.seq[front_index].append(a_1)
            return [self.seq[front_index][len(self.seq[front_index]) - 1], self.seq[front_index][0]]

        if front_index == self.matrix_size and end_index != self.matrix_size:
            self.seq[end_index].insert(0, a_0)
            return [self.seq[end_index][len(self.seq[end_index]) - 1], self.seq[end_index][0]]

        if front_index == self.matrix_size and end_index == self.matrix_size:
            self.seq.append([a_0, a_1])
            return [a_1, a_0]

    def run(self):
        if self.error == 0:
            while self.L < self.matrix_size:
                print(f"<<Iteration {self.L}>>")
                self.row_col_reduction()
                self.regret_cal()
                print("-" * 50)


class RegretBBAlgorithm(RegretAlgorithm):
    
    def __init__(self, random_input:bool):
        super().__init__(random_input)
        self.stack = stack.StackLink()
        self.read_stack = stack.StackLink()

    def regret_cal(self):
        list_regret = []
        xy = np.argwhere(self.matrix == 0)

        for i in range(0, len(xy)):
            k = xy[i]
            xx = self.matrix[k[0]][:]
            xx = np.delete(xx, k[1])
            yy = self.matrix[:, k[1]]
            yy = np.delete(yy, k[0])
            r = min(xx)
            c = min(yy)
            list_regret.append(r + c)

        z = np.argmax(list_regret)
        aa = self.m[xy[z][0]][xy[z][1]]

        print(f"\n{self.L}th Job Sequence is Job{aa[0]} -> Job{aa[1]}.")
        print(
            f"When the sequence is assigned, Cmax is {self.Cmax}, and if not, lower bound is {self.Cmax + list_regret[z]}.")

        bb = self.sequencing(aa[0], aa[1])
        self.L += 1

        self.branch(list_regret[z]) # branching

        if not self.L == self.matrix_size:
            print(f"The current sequence is : {self.seq}")
            print(f"\nSubtour {bb} should be prohibited")
            c1, c2 = -1, -1
            for i in range(len(self.m)):
                for j in range(len(self.m)):
                    if (self.m[i][j][0] == bb[0]) and (self.m[i][j][1] == bb[1]):
                        c1 = i
                        c2 = j
            if c1 != -1 and c2 != -1:
                self.matrix[c1][c2] = self.infinity

            matrix_df = pd.DataFrame(self.matrix)
            print("\nAfter Subtour Prohibition:")
            print(matrix_df)

            self.matrix = np.delete(self.matrix, xy[z][0], axis=0)
            self.matrix = np.delete(self.matrix, xy[z][1], axis=1)
            self.m = np.delete(self.m, xy[z][0], axis=0)
            self.m = np.delete(self.m, xy[z][1], axis=1)
            # self.L += 1
            matrix_df = pd.DataFrame(self.matrix)
            print("\nAfter Row/Column Elimination:")
            print(matrix_df)

    def branch(self, regret):
        self.stack.push(self.Cmax + regret)
        self.stack.push(self.Cmax)
        self.read_stack.push(self.stack.pop())

    def optimality_check(self):
        clock = True
        for i in range(self.stack.size):
            temp = self.stack.pop()
            self.read_stack.push(temp)
            if self.Cmax > temp:
                print(f"There is a lower bound {temp} smaller than {self.Cmax}.\nMore branching required.")
                clock = False

        seq_stack = stack.StackLink()
        for i in range(self.read_stack.size):
            seq_stack.push(self.read_stack.pop())
        print("Searched : ", end='')
        seq_stack.print_stack()

        if clock:
            print(f"No lower bound smaller than the final value of Cmax : {self.Cmax}")
            print(f"The Final Sequence is {self.seq}, with Cmax {self.Cmax}")

    def run(self):
        super().run()
        if self.L == self.matrix_size:
            self.optimality_check()


if __name__ == "__main__":
    
    print("\n<<Branch & bound method with regret-based bounding technique>>")
    RegretBB = RegretBBAlgorithm(random_input=True)
    RegretBB.run()
    print("-" * 50)

    ##
    #print("<<Regret-based Algorithm>>")
    #Regret = RegretAlgorithm(random_input=True)
    #Regret.run()
    #print(f"The Final Sequence is {Regret.seq}, with Cmax {Regret.Cmax}")
    #print("-" * 50)
    
