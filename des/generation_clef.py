import random

def recupererClefAleatoire():
    k = random.getrandbits(64)
    k = bin(k)[2:].zfill(64)
    return k

def recupererClefsDeRonde(clef):
    # Table de permutation CP1
    CP1 = [57, 49, 41, 33, 25, 17,  9,
            1, 58, 50, 42, 34, 26, 18,
           10,  2, 59, 51, 43, 35, 27,
           19, 11,  3, 60, 52, 44, 36,
           63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
           14,  6, 61, 53, 45, 37, 29,
           21, 13,  5, 28, 20, 12,  4]

    # Table de permutation CP2
    CP2 = [14, 17, 11, 24,  1,  5,
           3,  28, 15,  6, 21, 10,
           23, 19, 12,  4, 26,  8,
           16,  7, 27, 20, 13,  2,
           41, 52, 31, 37, 47, 55,
           30, 40, 51, 45, 33, 48,
           44, 49, 39, 56, 34, 53,
           46, 42, 50, 36, 29, 32]
           

    # Table de rotation
    TDR = [1, 1, 2, 2, 2, 2, 2, 2,
           1, 2, 2, 2, 2, 2, 2, 1]

    # Permutation et réduction de la clef initiale à 56 bits
    clef56 = ""
    for nombre in CP1:
        clef56 += clef[nombre - 1]
    
    # Division de la clef de 56 bits en deux
    g0 = clef56[:28]
    d0 = clef56[28:]

    # Rotation en utilisant la table de rotation
    clefs_g = []
    clefs_d = []
    for i in range(16):
        nombreRotation = TDR[i]

        temp = g0[0:nombreRotation]
        g0 = g0[nombreRotation:] + temp
        clefs_g.append(g0)

        temp = d0[0:nombreRotation]
        d0 = d0[nombreRotation:] + temp
        clefs_d.append(d0)
    
    # Génération des sous clefs en combinant les différents résultats de rotation
    # et en appliquant la table de permutation CP2
    clefs = []
    for i in range(16):
        concat = clefs_g[i] + clefs_d[i]
        clef_i = ""
        for nombre in CP2:
            clef_i += concat[nombre - 1]
        clefs.append(clef_i)
    
    return clefs