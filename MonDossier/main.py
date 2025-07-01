import os
import operations
from connexion import connexion  # import de la fonction connexion du module connexion.py
from ftp_client import acceder_ftp  # import de la fonction d'accès FTP du module ftp_client.py
import scan_utils # import du module de scan
import logger  # import du logger si jamais besoin de logger dans main
from operations import (
    copier_fichier_dossier,
    renommer_fichier_dossier,
    creer_fichier_dossier,
    deplacer_fichier_dossier,
    supprimer_fichier_dossier,
    naviguer_arborescence,
    lister_arborescence,
    lister_dossier_fichier,
    sauvegarder_fichier_dossier,
    restaurer_fichier_dossier
)
        
fichiercsvusers = "users.csv"  # Nom du fichier
chemin_complet = os.path.abspath(fichiercsvusers)  # Chemin absolu du fichier
print("Fichier CSV utilisé :", chemin_complet) # Afficher le message.

identifiant, motdepasse = connexion(chemin_complet) # Appel de la définition de connexion.
operations.identifiant = identifiant
operations.motdepasse = motdepasse
ftp = acceder_ftp(identifiant, motdepasse)  # Connexion FTP une fois connecté

def gestion_fichier(): # Définition de la gestion des fichiers.

 while True : # Tant que c'est vrai.
        
        print("============================================================") # Afficher le choix.
        print("Que souhaitez-vous faire ?") # Afficher le choix.
        print("")
        print("1 : COPIER un fichier ou un dossier.") # Afficher le choix.
        print("2 : RENOMMER un fichier ou un dossier.") # Afficher le choix.
        print("3 : CRÉER un fichier ou un dossier.") # Afficher le choix.
        print("4 : DÉPLACER un fichier ou un dossier.") # Afficher le choix.
        print("5 : SUPPRIMER un fichier ou un dossier.") # Afficher le choix.
        print("6 : NAVIGUER.") # Afficher le choix.
        print("7 : LISTER arboresence.") # Afficher le choix.
        print("8 : LISTER les fichiers-dossiers.") # Afficher le choix.
        print("9 : SAUVEGARDER un fichier ou un dossier (depuis le client).") # Afficher le choix.
        print("10 : RESTAURER un fichier ou un dossier (depuis le serveur).") # Afficher le choix.
        if identifiant == "admin_paris":
            print("11 : MODULE SCAN (réseau et ports).")
        print("0 : QUITTER.") # Afficher le choix.

        choix = input("\nSelectionner l'action que vous souhaitez faire ? : ") # Demander le choix.

        if choix == "1":  # Copier un fichier ou un dossier
            copier_fichier_dossier()  # Appelle la fonction de copie
        elif choix == "2":  # Renommer un fichier ou un dossier
            renommer_fichier_dossier()  # Appelle la fonction de renommage
        elif choix == "3":  # Créer un fichier ou un dossier
            creer_fichier_dossier()  # Appelle la fonction de création
        elif choix == "4":  # Déplacer un fichier ou un dossier
            deplacer_fichier_dossier()  # Appelle la fonction de déplacement
        elif choix == "5":  # Supprimer un fichier ou un dossier
            supprimer_fichier_dossier()  # Appelle la fonction de suppression
        elif choix == "6":  # Naviguer dans l'arborescence
            naviguer_arborescence()  # Appelle la fonction de navigation
        elif choix == "7":  # Lister arborescence d'un chemin donné
            lister_arborescence()  # Appelle la fonction de listag
        elif choix == "8":  # Lister dossiers, sous-dossiers et fichiers
            lister_dossier_fichier()  # Appelle la fonction de listing complet
        elif choix == "9":  # Sauvegarder un fichier ou dossier vers le FTP
            sauvegarder_fichier_dossier(ftp, identifiant)  # Appelle la fonction de sauvegarde FTP
        elif choix == "10":  # Restaurer un fichier ou dossier depuis le FTP
            restaurer_fichier_dossier()  # Appelle la fonction de restauration FTP
        elif identifiant== "admin_paris" and choix == "11":  # Lancer le module de scan réseau et ports
            scan_utils.menu_scan()  # Appelle le menu du module scan
            #logger_action("LOCAL", identifiant, "SCAN MODULE", "non concerné", "non concerné")  # Log du lancement du scan
        elif choix == "0":  # Quitter le programme
            break  # Sort de la boucle de gestion
        else:  # Cas d'un choix invalide
            print("Le choix est invalide !")  # Informe l'utilisateur


print("Utilisateur connecté :", identifiant) # Afficher le message.
gestion_fichier()  # Démarre la boucle principale de gestion des fichiers
