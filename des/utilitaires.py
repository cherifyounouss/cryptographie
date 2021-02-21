# Conversion ASCII vers binaire
def asciiVersBin(chaine):
    binaire = ""
    for lettre in chaine:
        binaire += bin(ord(lettre))[2:].zfill(8);
    # Remplissage du bloc avec des 0 si nécessaire
    for i in range(64 - len(binaire)):
        binaire += "0"
    return binaire

def binVersAscii(binaire64):
    chaine = ""
    for i in range(0, 64, 8):
        chaine += chr(int(binaire64[i:i+8], 2))
    return chaine