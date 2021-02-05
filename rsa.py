def pgcd(a, b):
    if (b == 0):
        return a
    else:
        return pgcd(b, a % b)

# Test de primalité usuel
def estPremier(n):
    if (n <= 1):
        return False
    if (n == 2):
        return True
    if (n % 2 == 0):
        return False
    for i in range(3, int(n**0.5), 2):
        if (n % i == 0):
            return False
    return True

# Test de primalité en utilisant l'observation que tous les nombres premiers s'écrivent sous la forme 6k+1 ou 6k-1
# Sauf 2 et 3
def estPremierOptimise(n):
    if (n <= 1):
        return False
    if (n <= 3):
        return True
    if (n % 2 == 0 or n % 3 == 0):
        return False
    i = 5
    while(i*i < n):
        if (n % i == 0 or n % (i + 2) == 0):
            return False
        i += 6
    return True

# Test de primalité en utilisant le petit théorème de Fermat
# NB: méthode probabiliste
def estPremierFermat(n):
    if (n <= 1):
        return False
    if (n <= 3):
        return True
    essaiMax = 10
    i = essaiMax
    while(i > 0):
        a = random.randint(2, n - 2)
        if (pgcd(a, n) != 1):
            return False
        if (exponentiationModulaire(a, n - 1, n) != 1):
            return False
        i -= 1
    return True


def exponentiationModulaire(a, b, n):
    c = 0
    d = 1
    repBinaireB = bin(b)[2:]
    for i in repBinaireB:
        c = 2 * c
        d = (d ** 2) % n
        if (i == "1"):
            c += 1
            d = (d * a) % n
    return d


def estDivisiblePar2Ou3(n):
    return n % 2 == 0 or n % 2 == 3

def recupererSEtD(n):
    repBinaire = bin(n)[2:]
    s = 0
    d = 0
    while True:
        i = repBinaire[len(repBinaire)-1]
        if (i == "0"):
            s += 1
            repBinaire = repBinaire[:-1]
        else:
            d = int(repBinaire, 2)
            break
    return s, d



def temoinMiller(n, a, s, d):
    x = exponentiationModulaire(a, d, n)
    if (x == 1 or x == n - 1):
        return False
    for i in range(1, s):
        x = (x ** 2) % n
        if (x == n - 1):
            return False
    return True

# Test de primalité en utilisant le test de Miller-Rabin
# NB: méthode probabiliste
def estPremierMillerRabin(n):
    if (n <= 1):
        return False
    if (n <= 3):
        return True
    s, d = recupererSEtD(n - 1)
    essaiMax = 10
    i = essaiMax
    while(i > 0):
        a = random.randint(2, n - 2)
        if (temoinMiller(n, a, s, d)):
            return False
        i -= 1
    return True

        
# Générer un candidat pour être nombre premier
def genererCandidat(nombreDeBits):
    nbr = random.getrandbits(nombreDeBits)
    # Ajuster le nombre pour mettre les bits aux extrémités à 1
    nbr |= (1 << nombreDeBits - 1) | 1
    return nbr

def genererNombrePremier(nombreDeBits = 1024):
    p = 4
    while not estPremierMillerRabin(p):
        p = genererCandidat(nombreDeBits)
    return p

def euclideEtendu(a, b):
    if (b == 0):
        return a, 1, 0
    p, q, r = euclideEtendu(b, a % b)
    d, x, y = p, r, q  - ((a // b )* r)
    return d, x, y


def genererClefRSA():
    # Etape de generation des nombres premiers
    p = genererNombrePremier(10)
    q = genererNombrePremier(10)
    if (p == q):
        raise ValueError("p et q ne peuvent pas être égaux")
    
    # Calcul de n et de phi
    n = p * q
    phi = (p - 1) * (q - 1)

    # Génération aléatoire d'un entier e premier avec phi
    e = random.randrange(1, phi)
    g = pgcd(e, phi)
    while(g != 1):
        e = random.randrange(1, phi)
        g = pgcd(e, phi)
    
    # Utilisation d'euclide etendu pour trouver l'inverse modulaire de e
    d = euclideEtendu(e, phi)[1]

    # Clef publique (e, n), Clef privé (d, n)
    return ((e, n), (d, n))

def chiffrerAvecRSA(clefPublique, messageClair):
    clef, n = clefPublique
    # Conversion de chaque caractère en nombre, ensuite calcul de m^e mod n
    messageChiffre = [exponentiationModulaire(ord(car), clef, n) for car in messageClair]
    return messageChiffre

def dechiffrerAvecRSA(clefPrive, messageChiffre):
    clef, n = clefPrive
    # Calcul de c^d mod n, ensuite conversion du nombre obtenu en caractère
    messageClair = [chr((car ** clef) % n) for car in messageChiffre]
    return ''.join(messageClair)

def simulerRSA():
    # Generation des clefs
    clefPublique, clefPrive = genererClefRSA()
    print ("\nVotre clef publique est {} et votre clef privé est {}\n".format(clefPublique, clefPrive))
    messageClair = input("Entrer un message à chiffrer avec votre clef publique: ")
    messageChiffre = chiffrerAvecRSA(clefPublique, messageClair)
    print ("Votre message chiffré est: {}".format(''.join(map(lambda x:str(x), messageChiffre))))
    print ("\nDéchiffrement du message chiffré avec votre clef privée ", clefPrive ," . . .")
    print ("\nVotre message est: {}\n\n".format(dechiffrerAvecRSA(clefPrive, messageChiffre)))