import generation_clef
import chiffrement
import dechiffrement
import utilitaires

def recupererChaineChiffre(chaineBinaire):
    mChiffreClair = ""
    for i in range(0, len(chaineBinaire), 64):
        mChiffreClair += utilitaires.binVersAscii(chaineBinaire[i:i+64])
    return mChiffreClair

if __name__ == "__main__":
    messageClair = input("Entrer une chaine à chiffrer: ")
    clef = generation_clef.recupererClefAleatoire()
    clefsRonde = generation_clef.recupererClefsDeRonde(clef)
    mChiffreBinaire = chiffrement.chiffrer(messageClair, clefsRonde)
    print("Clef: " + recupererChaineChiffre(clef))
    print("Message chiffré: " + recupererChaineChiffre(mChiffreBinaire))
    print("Message déchiffré: " + dechiffrement.dechiffrer(mChiffreBinaire, clefsRonde))
