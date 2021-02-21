from utilitaires import asciiVersBin, binVersAscii
from feistel import f

def chiffrer(texte, clefs):
    
    # Division du texte en des blocs de 64 bits
    blocs = []
    for i in range(0, len(texte), 8):
        blocs.append(texte[i:i + 8])
    blocsChiffres = []
    for bloc in blocs:
        blocsChiffres.append(chiffrerBloc(asciiVersBin(bloc), clefs))
    texteChiffre = ""
    for bc in blocsChiffres:
        texteChiffre += bc
    return texteChiffre

def chiffrerBloc(binaire64, clefs):
    # Table de permutation initiale
    PI = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17,  9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]
    # Table de permutation finale, permutation inverse
    PF = [40,  8, 48, 16, 56, 24, 64, 32,
          39,  7, 47, 15, 55, 23, 63, 31,
          38,  6, 46, 14, 54, 22, 62, 30,
          37,  5, 45, 13, 53, 21, 61, 29,
          36,  4, 44, 12, 52, 20, 60, 28,
          35,  3, 43, 11, 51, 19, 59, 27,
          34,  2, 42, 10, 50, 18, 58, 26,
          33,  1, 41,  9, 49, 17, 57, 25]

    # Application de la permutation initiale
    p = ""
    for nombre in PI:
        p += binaire64[nombre - 1]

    # Division du bloc en deux parties
    g = p[:32]
    d = p[32:]

    # Application des 16 rondes
    for i in range(16):
        temp = d
        d = bin(int(g, 2) ^ int(f(d, clefs[i]), 2))[2:].zfill(32)
        g = temp
    concat = g + d
    blocChiffre = ""
    for nombre in PF:
        blocChiffre += concat[nombre - 1]
    
    return blocChiffre