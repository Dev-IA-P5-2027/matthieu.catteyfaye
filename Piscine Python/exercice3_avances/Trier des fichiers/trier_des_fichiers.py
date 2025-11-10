import os
import shutil

current_directory = os.getcwd()

# Je n'arrive pas à faire fonctionner avec os.getcwd()
# Fonctionne, mais uniquement avec mes dossiers

def trie_du_fichier(fichier):
    if fichier.endswith('.jpg') or fichier.endswith('.jpeg') or fichier.endswith('.png') or fichier.endswith('.gif'):
        shutil.move("exercice3_avances\Trier des fichiers"+fichier, "exercice3_avances\Trier des fichiers\Images"+fichier)

    elif fichier.endswith('.pdf'):
        shutil.move("exercice3_avances\Trier des fichiers"+fichier, "exercice3_avances\Trier des fichiers\Documents"+fichier)
    
    elif fichier.endswith('.mp3'):
        shutil.move("exercice3_avances\Trier des fichiers"+fichier, "exercice3_avances\Trier des fichiers\Musiques"+fichier)

    elif fichier.endswith('.mp4'):
        shutil.move("exercice3_avances\Trier des fichiers"+fichier, "exercice3_avances\Trier des fichiers\Videos"+fichier)

    else:
        print("Extansion inconnue.")


fichier1 = "\Court_metrage.mp4"
fichier2 = "\Despacito.mp3"
fichier3 = "\Facture.pdf"
fichier4 = "\Tour_eiffel.jpg"

trie_du_fichier(fichier1)
trie_du_fichier(fichier2)
trie_du_fichier(fichier3)
trie_du_fichier(fichier4)