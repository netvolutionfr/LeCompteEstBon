import tirage

class Node:
    def __init__(self, numbers, objectif, parent=None, operation=None, used_numbers=None, result=0, depth=0):
        self.numbers = numbers        # Liste des nombres disponibles dans ce nœud
        self.objectif = objectif      # Nombre à atteindre
        self.parent = parent          # Référence au nœud parent
        self.operation = operation    # Opération utilisée pour atteindre ce nœud
        self.used_numbers = used_numbers  # Les nombres utilisés dans l'opération
        self.result = result          # Résultat de l'opération
        self.children = []            # Liste des nœuds enfants
        self.depth = 0                # Profondeur du nœud dans l'arbre
        if self.result == self.objectif:
            self.solution = True
        else:
            self.solution = False

    def __repr__(self):
        ### Construit la liste des opérations pour atteindre ce nœud
        operations = []
        used_numbers = []
        node = self
        while node.parent:
            operations.append(node.operation)
            used_numbers.append(node.used_numbers)
            node = node.parent
        operations.reverse()
        used_numbers.reverse()
        ### Construit la chaîne de caractères représentant ce nœud
        ### Une ligne par opération
        string = ''
        for i in range(len(operations)):
            n1 = used_numbers[i][0]
            n2 = used_numbers[i][1]
            match operations[i]:
                case '+':
                    string += f'{n1} + {n2} = {n1+n2}\n'
                case '-':
                    string += f'{n1} - {n2} = {n1-n2}\n'
                case '*':
                    string += f'{n1} * {n2} = {n1*n2}\n'
                case '/':
                    string += f'{n1} / {n2} = {n1/n2}\n'
        return string

    def add_child(self, child):
        self.children.append(child)

    def generate_children(self):
        for i in range(len(self.numbers)):
            for j in range(i+1, len(self.numbers)):
                # Addition
                numbers = self.numbers.copy()
                used_numbers = [numbers.pop(j), numbers.pop(i)]
                numbers.append(used_numbers[0] + used_numbers[1])
                child = Node(numbers, self.objectif, self, '+', used_numbers, numbers[-1], self.depth+1)
                self.add_child(child)
                if child.solution:
                    return True

                # Soustraction
                numbers = self.numbers.copy()
                used_numbers = [numbers.pop(j), numbers.pop(i)]
                if used_numbers[0] > used_numbers[1]:
                    numbers.append(used_numbers[0] - used_numbers[1])
                    child = Node(numbers, self.objectif, self, '-', used_numbers, numbers[-1], self.depth+1)
                    self.add_child(child)
                    if child.solution:
                        return True

                # Multiplication
                numbers = self.numbers.copy()
                used_numbers = [numbers.pop(j), numbers.pop(i)]
                numbers.append(used_numbers[0] * used_numbers[1])
                child = Node(numbers, self.objectif, self, '*', used_numbers, numbers[-1], self.depth+1)
                self.add_child(child)
                if child.solution:
                    return True

                # Division
                numbers = self.numbers.copy()
                used_numbers = [numbers.pop(j), numbers.pop(i)]
                if used_numbers[1] != 0 and used_numbers[0] % used_numbers[1] == 0:
                    numbers.append(used_numbers[0] // used_numbers[1])
                    child = Node(numbers, self.objectif, self, '/', used_numbers, numbers[-1], self.depth+1)
                    self.add_child(child)
                    if child.solution:
                        return True
        return False

    def generate_tree(self):
        self.generate_children()
        for child in self.children:
            child.generate_tree()

    def get_list_of_solutions(self):
        if self.solution:
            return [self]
        else:
            solutions = []
            for child in self.children:
                solutions.extend(child.get_list_of_solutions())
            return solutions

    def find_best_solution(self):
        diff = abs(self.result - self.objectif)
        if diff == 0:
            return self
        else:
            best = self
            for child in self.children:
                solution = child.find_best_solution()
                if solution:
                    if abs(solution.result - self.objectif) < diff:
                        diff = abs(solution.result - self.objectif)
                        best = solution
            return best

jeu = tirage.tirage()
parent_node = Node(jeu['tirage'], jeu['objectif'])

print(f'Tirage: {jeu['tirage']}')
print(f'Objectif : {jeu['objectif']}')

parent_node.generate_tree()
solutions = parent_node.get_list_of_solutions()
if len(solutions):
    print(f'Il y a {len(solutions)} solutions')

    ### Find minimal depth solution
    min = 0
    for i in range(len(solutions)):
        if solutions[i].depth < solutions[min].depth:
            min = i
    print(solutions[min])
else:
    print('Pas de solution')
    ### Parcourir l'arbre pour trouver la solution la plus proche
    solution = parent_node.find_best_solution()
    print(f'La solution la plus proche est {solution.result}')
    print(solution)
