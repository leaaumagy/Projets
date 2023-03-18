import random

# On demande à l'utilisateur de saisir le nombre d'états
num_states = int(input("Entrez le nombre d'états: "))

# On demande à l'utilisateur de saisir la distribution initiale
print("Entrez la distribution initiale(telle qu'une liste de probabilités sans séparateur):")
init_dist = [float(x) for x in input().strip().split()]

# On vérifie que la somme des probabilités de la distribution initiale est égale à 1
while sum(init_dist) != 1:
    print("Erreur:La somme des probabilités doit être égale à 1")
    init_dist = [float(p) for p in input(
        "Entrez la nouvelle distribution initiale: ").strip().split()]


# On demande à l'utilisateur de saisir la matrice de transition
print("Entrez la matrice de transition (comme une liste de vecteurs en lignes):")
transition_matrix = []
for i in range(num_states):
    row = [float(x) for x in input().strip().split()]
    transition_matrix.append(row)

# On vérifie que chaque ligne de la matrice de transition est une probabilité conditionnelle valide
for i in range(num_states):
    while sum(transition_matrix[i]) != 1:
        print("Erreur: la ligne {} de la matrice de transition ne représente pas une probabilité conditionnelle valide.".format(i))
        print("Entrez la nouvelle matrice de transition:")
        transition_matrix = []
        for i in range(num_states):
            row = [float(x) for x in input().strip().split()]
            transition_matrix.append(row)

# La longueur de la chaîne
chain_length = int(input("Entrez la longueur de la chaîne: "))

# On génére une chaîne de Markov en utilisant les paramètres définis par l'utilisateur
state = random.choices(range(num_states), weights=init_dist, k=1)[0]
chain = [state]
for i in range(chain_length - 1):
    state = random.choices(
        range(num_states), weights=transition_matrix[state], k=1)[0]
    chain.append(state)

# On affiche la chaîne générée
print("La chaîne générée est:", chain)

# On compte le nombre de passages dans chaques états
state_counts = [chain.count(i) for i in range(num_states)]
print("Nombre de passages par états:", state_counts)

# On définit le calcul de la puissance matriciel, puis on calcule la puissance 50 de la matrice de transition pour vérifier la régularité de la chaîne


def matrix_power(matrix, power):
    result = [[0 for j in range(len(matrix))] for i in range(len(matrix))]
    for i in range(len(matrix)):
        result[i][i] = 1
    while power > 0:
        if power % 2 == 1:
            result = matrix_mult(result, matrix)
        matrix = matrix_mult(matrix, matrix)
        power = power // 2
    return result


def matrix_mult(a, b):
    result = [[0 for j in range(len(b[0]))] for i in range(len(a))]
    for i in range(len(a)):
        for j in range(len(b[0])):
            for k in range(len(b)):
                result[i][j] += a[i][k] * b[k][j]
    return result


result = matrix_power(transition_matrix, 50)
is_regular = True
for row in result:
    for value in row:
        if value == 0:
            is_regular = False
            break
    if not is_regular:
        break
if is_regular:
    print("La chaîne de Markov est régulière")
else:
    print("La chaîne de Markov n'est pas régulière")


# On regarde si la chaîne est irréductible
reachable = [[False for j in range(num_states)] for i in range(num_states)]

for i in range(num_states):
    reachable[i][i] = True
    for j in range(num_states):
        if transition_matrix[i][j] > 0:
            reachable[i][j] = True

for k in range(num_states):
    for i in range(num_states):
        for j in range(num_states):
            reachable[i][j] |= reachable[i][k] & reachable[k][j]

is_irreducible = True
for i in range(num_states):
    for j in range(num_states):
        if not reachable[i][j]:
            is_irreducible = False
            break
    if not is_irreducible:
        break

if is_irreducible:
    print("La chaîne de Markov est irréductible.")
else:
    print("La chaîne de Markov n'est pas irréductible.")

# On vérifie si la chaîne est absorbante
absorbing = [False for i in range(num_states)]

for i in range(num_states):
    reachable[i][i] = True
    for j in range(num_states):
        if transition_matrix[i][j] > 0:
            reachable[i][j] = True

for k in range(num_states):
    for i in range(num_states):
        for j in range(num_states):
            reachable[i][j] |= reachable[i][k] & reachable[k][j]

for i in range(num_states):
    for j in range(num_states):
        if reachable[j][i] and not reachable[i][j]:
            absorbing[i] = True

is_absorbing = False
for i in range(num_states):
    if absorbing[i]:
        is_absorbing = True
        break

if is_absorbing:
    print("La chaîne de Markov est absorbante.")
else:
    print("La chaîne de Markov n'est pas absorbante.")


# On cherche le nombre d'états absorbants, quel état absorbe la chaîne et à quelle position la chaîne est absorbée
if is_absorbing:
    absorbing_states = []
    for i in range(num_states):
        is_absorbing = True
        for j in range(num_states):
            if i != j and transition_matrix[i][j] > 0:
                is_absorbing = False
                break
        if is_absorbing:
            absorbing_states.append(i)

    print("Les états absorbants sont les états :", absorbing_states)

    first_absorbing_state = None
    first_absorbing_state_occurrence = None
    for i, state in enumerate(chain):
        if state in absorbing_states:
            first_absorbing_state = state
            first_absorbing_state_occurrence = i
            break

    print("L'état absorbant la chaîne est l'état :", first_absorbing_state)
    print("L'état absorbant apparaît à la position:",
          first_absorbing_state_occurrence)

# On simule la chaîne 10000 fois afin d'avoir le nombre de passages moyen par états.

total_counts = [0 for i in range(num_states)]
for i in range(10000):
    # Générer une chaîne de Markov
    state = random.choices(range(num_states), weights=init_dist, k=1)[0]
    chain = [state]
    for i in range(chain_length - 1):
        state = random.choices(
            range(num_states), weights=transition_matrix[state], k=1)[0]
        chain.append(state)

    # Compter le nombre de passages pour chaque état
    state_counts = [chain.count(i) for i in range(num_states)]

    # Ajouter les comptes à la somme totale
    for i in range(num_states):
        total_counts[i] += state_counts[i]

# Afficher le nombre moyen de passages pour chaque état
mean_counts = [count / 10000 for count in total_counts]
print("Le nombre moyen de passages par état est:", mean_counts)

# On simule la chaine 10000 fois pour savoir en moyenne à quelle position la chaîne est absorbée

if is_absorbing:
    total_counts = [0 for i in range(num_states)]
    first_absorption = []
    for i in range(10000):
        # Générer une chaîne de Markov
        state = random.choices(range(num_states), weights=init_dist, k=1)[0]
        chain = [state]
        for j in range(chain_length - 1):
            state = random.choices(
                range(num_states), weights=transition_matrix[state], k=1)[0]
            chain.append(state)

            # Compter le nombre de passages pour chaque état
            state_counts = [chain.count(i) for i in range(num_states)]

            # Ajouter les comptes à la somme totale
            for i in range(num_states):
                total_counts[i] += state_counts[i]

            # Vérifier si c'est l'état d'absorption
            if state == num_states - 1:
                first_absorption.append(j + 1)
                break

# Calculer la position moyenne d'absorption
    mean_absorption = sum(first_absorption) / len(first_absorption)
    print("La position moyenne d'absorption est :", mean_absorption)
