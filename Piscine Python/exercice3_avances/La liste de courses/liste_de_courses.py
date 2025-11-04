import os
import json

json_path = "exercice3_avances\La liste de courses\liste.json"


affichage = """
Choisissez une option:
\t1: Ajouter un élément
\t2: Enlever un élément
\t3: Afficher la liste
\t4: Vider la liste
\t5: Sauvegarder la liste
\t6: Quitter
"""

        
with open(json_path, "r") as json_file:
    liste_de_courses = json.load(json_file)


while True:
    print(affichage)
    option_choisie = input("Choisir une option : ")
    
    if option_choisie == "1":
        nouvel_element = input("Quel élément ajouter ? ")
        liste_de_courses.append(nouvel_element)

    elif option_choisie == "2":
            if liste_de_courses == []:
                print("La liste est déjà vide. ")
            else:
                n = 1
                for i in liste_de_courses:
                    print(f"{n}: {i}")
                    n += 1
                try:
                    id_element_supr = int(input("Quel élément suprimer ? "))
                    del liste_de_courses[id_element_supr-1]
                except IndexError:
                    print("Erreur : l'index n'est pas dans la liste. ")
    
    elif option_choisie == "3":
        print("Actuelle liste de courses : ")
        for i in liste_de_courses:
            print("\t-", i)

    elif option_choisie == "4":
        liste_de_courses = []
        print("Liste vidée. ")
    
    elif option_choisie == "5":
        with open(json_path, "w") as json_file:
            json.dump(liste_de_courses, json_file)
        print("Sauvegarde effectuée ! ")

    elif option_choisie == "6":
        print("Au revoir ! ")
        break

    else:
        print("Erreur de saisie ! ")