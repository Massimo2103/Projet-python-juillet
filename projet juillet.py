from ftplib import FTP
import os
import sys
import shutil


# connexion au serveur FTP

ftp_host = '127.0.0.1'
ftp_login = 'MARSEILLE'
ftp_password = 'Marseille'
path_ftp = "C:/REMOTE_PROJET/MARSEILLE"
print("Avant connexion")
connexion = FTP (ftp_host, ftp_login, ftp_password)
print("Après connexion")
print(connexion.getwelcome()) # Récupérer le message

#connexion.quit()

def copier_fichier_dossier():
     print("\n Copie FICHIER/DOSSIER ")
     
     while True :
          try:  
               choix = input("Souhaitez-vous copier un fichier (1) ou un dossier (2) ? : ")
               if choix not in ("1", "2"):
                    raise ValueError("La valeur saisie n'est pas 1 ou 2 ! ") # Arrêt de l'éxecution et déclaration de valueError.
               source = input("Entrez le chemin COMPLET du fichier ou du dossier à copier (ex : C/Massimo/Paris.txt): ").strip()
               if not os.path.exists(source):
                    raise ValueError("Le chemin SOURCE est incorrect ! ") # Arrêt de l'éxecution et déclaration de valueError.
               destination = input("Entrez le chemin COMPLET où coller le fichier ou le dossier avec le nom du fichier (ex : C/Massimo/Juillet/Paris.txt) : ").strip()
               dossier_parent = os.path.dirname(destination)
               if not os.path.isdir(dossier_parent):
                    raise ValueError("Le chemin de DESTINATION est incorrect ! ") # Arrêt de l'éxecution et déclaration de valueError.

               if choix == "1":
                    shutil.copy2(source, destination)
                    print(f"Fichier copié avec succès vers : {destination}")
               elif choix == "2":
                    shutil.copytree(source, destination)
                    print(f"Dossier copié avec succès vers : {destination}")
               
          except ValueError as e:
               message_erreur = str(e) # Convertir l'erreur en chaîne de caractère.
               print(f"Erreur : {message_erreur}") # Afficher le message d'erreur lié à l'erreur rencontrée.
               
          except Exception as e:
               print(f"Erreur lors de la copie : {e}")

          finally:
               break

def renommer_fichier_dossier():
     print("\n Renommer FICHIER/DOSSIER ")
     
     while True :
          try:  
               choix = input("Souhaitez-vous renommer un fichier (1) ou un dossier (2) ? : ")
               if choix not in ("1", "2"):
                    raise ValueError("La valeur saisie n'est pas 1 ou 2 ! ") # Arrêt de l'éxecution et déclaration de valueError.
               ancien_nom = input("Entrez le chemin COMPLET du fichier ou du dossier à renommer (ex : C/Massimo/Paris): ").strip()
               if not os.path.exists(ancien_nom):
                    raise ValueError("Le chemin est incorrect ! ") # Arrêt de l'éxecution et déclaration de valueError.
               nouveau_nom = input("Entrez le chemin COMPLET du fichier ou du dossier à renommer (ex : C/Massimo/Juillet/Paris) : ").strip()
               dossier_parent = os.path.dirname(nouveau_nom)
               if not os.path.isdir(dossier_parent):
                    raise ValueError("Le chemin est incorrect ! ") # Arrêt de l'éxecution et déclaration de valueError.
               
               os.rename(ancien_nom, nouveau_nom)

               if choix == "1":
                    print(f"Fichier renommé avec succès : {ancien_nom} ==> {nouveau_nom}")
               elif choix == "2":
                    print(f"Dossier renommé avec succès : {ancien_nom} ==> {nouveau_nom}")
               
          except ValueError as e:
               message_erreur = str(e) # Convertir l'erreur en chaîne de caractère.
               print(f"Erreur : {message_erreur}") # Afficher le message d'erreur lié à l'erreur rencontrée.
               
          except Exception as e:
               print(f"Erreur lors de la renommée : {e}")
               continue

          else :
               break

def creer_fichier_dossier():
    print("\n Créer FICHIER/DOSSIER ")

    while True:
        try:
            choix = input("Souhaitez-vous créer un fichier (1) ou un dossier (2) ? : ")
            if choix not in ("1", "2"):
                raise ValueError("La valeur saisie n'est pas 1 ou 2 !")
            localisation = input("Entrez le chemin COMPLET où créer le fichier ou dossier (ex : C:/Massimo/Projet ; C:/Massmo/Projet.txt) : ").strip()
            if not localisation:
                 raise ValueError("La localisation n'a pas été renseignée !")
            dossier_parent = os.path.dirname(localisation)
            if not os.path.isdir(dossier_parent):
                raise ValueError("Le dossier parent n'existe pas !")

            if choix == "1":
                with open(localisation, 'x') as f:  # 'x' pour créer uniquement s'il n'existe pas
                    pass
                print(f"Fichier créé avec succès : {localisation}")

            elif choix == "2":
                os.makedirs(localisation, exist_ok=False)  # erreur si existe déjà
                print(f"Dossier créé avec succès : {localisation}")

        except ValueError as e:
            print(f"Erreur : {e}")
        except FileExistsError:
            print("Erreur : Le fichier ou dossier existe déjà.")
        except Exception as e:
            print(f"Erreur lors de la création : {e}")
            continue
        else:
            break

def deplacer_fichier_dossier():
    print("\n Déplacer FICHIER/DOSSIER ")

    while True:
        try:
            choix = input("Souhaitez-vous déplacer un fichier (1) ou un dossier (2) ? : ")
            if choix not in ("1", "2"):
                raise ValueError("La valeur saisie n'est pas 1 ou 2 !")
            ancien_chemin = input("Entrez le chemin COMPLET du fichier ou dossier à déplacer (ex : C:/Massimo/Paris ou C:/Massimo/projet.txt : ").strip()
            if not os.path.exists(ancien_chemin):
                raise ValueError("Le chemin est incorrect !")
            nouveau_chemin = input("Entrez le chemin COMPLET de destination (ex : C:/Massimo/Juillet/Paris ou C:/Massimo/projet.txt) : ").strip()
            dossier_parent = os.path.dirname(nouveau_chemin)
            if not os.path.isdir(dossier_parent):
                raise ValueError("Le chemin de DESTINATION est incorrect !")

            shutil.move(ancien_chemin, nouveau_chemin)

            if choix == "1":
                print(f"Fichier déplacé avec succès : {ancien_chemin} ==> {nouveau_chemin}")
            elif choix == "2":
                print(f"Dossier déplacé avec succès vers : {ancien_chemin} ==> {nouveau_chemin}")

        except ValueError as e:
            print(f"Erreur : {e}")
        except Exception as e:
            print(f"Erreur lors du déplacement : {e}")
        else:
            break


def supprimer_fichier_dossier2():
    print("\n== Supprimer FICHIER/DOSSIER ")
    
    while True:
        try:
            choix = input("Souhaitez-vous supprimer un fichier (1) ou un dossier (2) ? : ")
            if choix not in ("1", "2"):
                raise ValueError("La valeur saisie n'est pas 1 ou 2 !")
            chemin = input("Entrez le chemin COMPLET du fichier ou du dossier à supprimer (ex : C:/Massimo/Paris.txt ou C:/Massimo/MonDossier) : ").strip()
            if not os.path.exists(chemin):
                raise ValueError("Le chemin spécifié n'existe pas !")

            if choix == "1":
                if os.path.isfile(chemin):
                    os.remove(chemin)
                    print(f"Fichier supprimé avec succès : {chemin}")
                else:
                    raise ValueError("Le chemin spécifié n'est pas un fichier !")

            elif choix == "2":
                if os.path.isdir(chemin):
                    shutil.rmtree(chemin)
                    print(f" Dossier supprimé avec succès : {chemin}")
                else:
                    raise ValueError("Le chemin spécifié n'est pas un dossier !")

        except ValueError as e:
            print(f" Erreur : {e}")
        except Exception as e:
            print(f"Erreur lors de la suppression de l'élément ! : {e}")
            continue
        else:
            break

def supprimer_fichier_dossier():
    print("\n== Supprimer FICHIER/DOSSIER ")
    
    while True:
        try:
            choix = input("Souhaitez-vous supprimer un fichier (1) ou un dossier (2) ? : ")
            if choix not in ("1", "2"):
               raise ValueError("La valeur saisie n'est pas 1 ou 2 !")
            chemin = input("Entrez le chemin COMPLET du fichier ou du dossier à supprimer (ex : C:/Massimo/Paris.txt ou C:/Massimo/MonDossier) : ").strip()
            if not os.path.exists(chemin):
               raise ValueError("Le chemin spécifié n'existe pas !")
            #if not os.path.isfile(chemin):
               raise ValueError("Le chemin renseigné ne renvoie pas un fichier !")
            if not os.path.isdir(chemin):
               raise ValueError("Le chemin renseigné ne renvoie pas un dossier !")

            if choix == "1":
                    os.remove(chemin)
                    print(f"Fichier supprimé avec succès : {chemin}")

            elif choix == "2":
                    os.rmdir(chemin)
                    print(f" Dossier supprimé avec succès : {chemin}")

        except ValueError as e:
            print(f" Erreur : {e}")
        except Exception as e:
            print(f"Erreur lors de la suppression de l'élément ! : {e}")
            continue
        else:
            break





def gestion_fichier():

 while True : # Tant que c'est vrai.
        
        print("============================================================") # Afficher le choix.
        print("Que souhaitez-vous faire ?") # Afficher le choix.
        print("")
        print("1 : COPIER un fichier ou un dossier.") # Afficher le choix.
        print("2 : RENOMMER un fichier ou un dossier.") # Afficher le choix.
        print("3 : CRÉER un fichier ou un dossier.") # Afficher le choix.
        print("4 : DÉPLACER un fichier ou un dossier.") # Afficher le choix.
        print("5 : SUPPRIMER un fichier ou un dossier.") # Afficher le choix.
        print("6 : SAUVEGARDER un fichier ou un dossier (depuis le client).") # Afficher le choix.
        print("7 : RESTAURER un fichier ou un dossier (depuis le serveur).") # Afficher le choix.
        print("8 : QUITTER.") # Afficher le choix.

        choix = input("Selectionner l'action que vous souhaitez faire : ") # Demander le choix.

        if choix == "1" : # Scanner un port specifique.
             copier_fichier_dossier()
        elif choix == "2" : # Scanner une plage de port.
             renommer_fichier_dossier()
        elif choix == "3" : # Scanner tous les ports simultanement.
             creer_fichier_dossier()
        elif choix == "4" : # Scanner tous les ports simultanement.
             deplacer_fichier_dossier()
        elif choix == "5" : # Scanner tous les ports simultanement.
             supprimer_fichier_dossier()
        elif choix == "6" : # Scanner tous les ports simultanement.

        #elif choix == "7" : # Scanner tous les ports simultanement.

        #elif choix == "8" : # Quitter le module.

          break
             
#if __name__ == "__main__":
gestion_fichier()

     


