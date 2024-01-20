import random

def tirage():
    """Tirage du jeu "Le Compte est bon" """
    # Construction des tuiles
    tuiles = []
    for i in range(1, 10):
        tuiles.append(i)
        tuiles.append(i)
    for i in [25, 50, 75, 100]:
        tuiles.append(i)
    # Tirage des 6 tuiles
    tirage = []
    for i in range(6):
        tirage.append(tuiles.pop(random.randint(0, len(tuiles)-1)))

    # Tirage de l'objectif
    objectif = random.randint(100, 999)
    return {'tirage' : tirage, 'objectif' : objectif}

if __name__ == '__main__':
    print(tirage())



