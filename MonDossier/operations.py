import os
import shutil
import socket
import time
import datetime
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from logger import logger_action
from scan_utils import ip_input
from ftp_client import acceder_ftp
identifiant = None
motdepasse = None


def copier_fichier_dossier(): # Définition pour copier un fichier ou dossier.

    print("\nCopie FICHIER/DOSSIER ") # Afficher le message.
     
    while True : # Tant que c'est vrai
        try: # Essayer
                choix_server_hote = input("sur ftp (1) ou client (2) ? ") # Demande de connexion au FTP ou au client.
                if choix_server_hote == "1" : # Si le choix est 1.
                    acceder_ftp(identifiant, motdepasse) # Lancer la définition acceder au FTP.
                elif choix_server_hote == "2" : # Si le choix est 2.
                    Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
                    ip_input(Hote) # Lancer la définition ip_input.
                if choix_server_hote not in ("1", "2"): # Si le choix n'est ni 1 et 2.
                    raise ValueError("La valeur saisie n'est pas 1 ou 2 ! ") # Arrêt de l'éxecution.
                choix = input("Souhaitez-vous copier un fichier (1) ou un dossier (2) ? : ") # Demander s'il faut coper un fichier ou dossier.
                if choix not in ("1", "2"): # Si le choix n'est ni 1 ni 2.
                    raise ValueError("La valeur saisie n'est pas 1 ou 2 ! ") # Arrêt de l'éxecution.
                source = input("Entrez le chemin COMPLET du fichier ou du dossier à copier (ex : C/Massimo/Paris.txt ou /remote_projet/ville/...): ").strip() # Demander le chemin source en retirant les espaces.
                if not os.path.exists(source): # Si le chemin n'existe pas.
                    raise ValueError("Le chemin SOURCE est incorrect ! ") # Arrêt de l'éxecution.
                destination = input("Entrez le chemin COMPLET où coller le fichier ou le dossier avec le nom du fichier (ex : C/Massimo/Juillet/Paris.txt ou /remote_projet/ville/...)) : ").strip() # Demander le chemin destination en retirant les espaces.
                dossier_parent = os.path.dirname(destination) # Extraire le chemin dossier.
                if not os.path.isdir(dossier_parent): # Si le dossier n'existe pas.
                    raise ValueError("Le chemin de DESTINATION est incorrect ! ") # Arrêt de l'éxecution.

                if choix == "1": # Si le choix est 1.
                    shutil.copy2(source, destination) # Copie le fichier source en conservant la date...
                    if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", identifiant, "COPIE FICHIER", source, destination) # Créer le log suivant.
                    elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, identifiant, "COPIE FICHIER", source, destination) # Créer le log suivant.
                    print(f"Fichier copié avec succès vers : {destination} !") # Afficher le message.
                elif choix == "2": # Si le choix est 2.
                    shutil.copytree(source, destination) # Copie le dossier source en conservant la date...
                    if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", identifiant, "COPIE DOSSIER", source, destination) # Créer le log suivant.
                    elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, identifiant, "COPIE FICHIER", source, destination) # Créer le log suivant.
                    print(f"Dossier copié avec succès vers : {destination} !") # Affciher le message.
               
        except ValueError as e: # En cas de Value Error.
               message_erreur = str(e) # Convertir l'erreur en chaîne de caractère.
               print(f"Erreur : {message_erreur}") # Afficher le message d'erreur.
               
        except Exception as e: # En cas d'erreur.
               print(f"Erreur lors de la copie : {e}") # Afficher le message d'erreur.

        else: # Sinon
            break # Continuer

def renommer_fichier_dossier(): # Définition renommer un fichier ou un dossier.
    print("\nRenommer FICHIER/DOSSIER ") # Affichage de la fonction.
     
    while True : # Tant que c'est vrai.
        try: # Essayer
                choix_server_hote = input("sur ftp (1) ou client (2) ? ") # Demande de connexion au FTP ou au client.
                if choix_server_hote == "1" : # Si le choix est 1.
                    acceder_ftp(identifiant, motdepasse) # Lancer la définition acceder au FTP.
                elif choix_server_hote == "2" : # Si le choix est 2.
                    Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
                    ip_input(Hote) # Lancer la définition ip_input.
                if choix_server_hote not in ("1", "2"): # Si le choix n'est ni 1 et 2.
                    raise ValueError("La valeur saisie n'est pas 1 ou 2 ! ") # Arrêt de l'éxecution.
                choix = input("Souhaitez-vous renommer un FICHIER (1) ou un DOSSIER (2) ? : ") # Demander si renommer un fichier ou un dossier.
                if choix not in ("1", "2"): # Si le choix n'est ni 1 ni 2.
                    raise ValueError("La valeur saisie n'est pas 1 ou 2 ! ") # Arrêt de l'éxecution.
                source = input("Entrez le chemin COMPLET du fichier ou du dossier à renommer (ex : C/Massimo/Paris): ").strip() # Demander le chemin du fichier/dossier.
                if not os.path.exists(source): # Si le chemin n'existe pas.
                    raise ValueError("Le chemin est incorrect ! ") # Arrêt de l'éxecution.
                
                destination = input("Entrez le chemin COMPLET du NOUVEAU fichier ou du dossier à renommer (ex : C/Massimo/Juillet/Paris) : ").strip() # Demander le chemin avec le nouveau nom.
               
                dossier_parent = os.path.dirname(destination) # Extraire le chemin dossier.
                if not os.path.isdir(dossier_parent): # Si le dossier n'existe pas.
                    raise ValueError("Le chemin est incorrect ! ") # Arrêt de l'éxecution.
                              
                os.rename(source, destination) # Renommer le fichier.

                if choix == "1":# Si le choix est 1.
                    if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", identifiant, "RENOMMER FICHIER", source, destination) # Créer le log suivant.
                    elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, identifiant, "RENOMMER FICHIER", source, destination) # Créer le log suivant.
                    print(f"Fichier renommé avec succès : {source} ==> {destination}") # Afficher le message.
                elif choix == "2": # Si le choix est 2.
                    if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", identifiant, "RENOMMER DOSSIER", source, destination) # Créer le log suivant.
                    elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, identifiant, "RENOMMER DOSSIER", source, destination) # Créer le log suivant.
                    print(f"Dossier renommé avec succès : {source} ==> {destination}") # Afficher le message.
               
        except ValueError as e: # En cas de Value Error.
               message_erreur = str(e) # Convertir l'erreur en chaîne de caractère.
               print(f"Erreur : {message_erreur}") # Afficher le message d'erreur.
        except Exception as e: # En cas d'erreur.
               print(f"Erreur lors de la renommée : {e}") # Afficher le message d'erreur.
        else: # Sinon
            break # Quiter la boucle

def creer_fichier_dossier(): # Définition créer un fichier ou dossier.
    print("\nCréer FICHIER/DOSSIER ") # Afficher la définition.

    while True: # Tant que c'est vrai.
        try: # Essayer
            choix_server_hote = input("sur ftp (1) ou client (2) ? ") # Demande de connexion au FTP ou au client.
            if choix_server_hote == "1" : # Si le choix est 1.
                acceder_ftp(identifiant, motdepasse) # Lancer la définition acceder au FTP.
            elif choix_server_hote == "2" : # Si le choix est 2.
                Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
                ip_input(Hote) # Lancer la définition ip_input.
            if choix_server_hote not in ("1", "2"): # Si le choix n'est ni 1 et 2.
                raise ValueError("La valeur saisie n'est pas 1 ou 2 ! ") # Arrêt de l'éxecution.
            choix = input("Souhaitez-vous créer un fichier (1) ou un dossier (2) ? : ") # Demander si on créer un fichier ou un dossier.
            if choix not in ("1", "2"): # Si le choix n'est ni 1 ni 2.
                raise ValueError("La valeur saisie n'est pas 1 ou 2 !") # Arrêt de l'éxecution.
            destination = input("Entrez le chemin COMPLET où créer le fichier ou dossier (ex : C/Massimo/Juillet/Paris/test.txt ou /REMOTE_PROJET/MARSEILLE/Projet.txt) : ").strip() # Demander le chemin.
            if not destination: # Si ce n'est pas source.
                 raise ValueError("La localisation n'a pas été renseignée !")
            dossier_parent = os.path.dirname(destination) # Extraire le chemin dossier.
            if not os.path.isdir(dossier_parent): # Si le dossier n'existe pas.
                raise ValueError("Le chemin est incorrect ! ") # Arrêt de l'éxecution.

            if choix == "1": # Si le choix est 1.
                with open(destination, 'x') as f:  # Ouvrir le fichier uniquement s'il n'existe pas.
                    pass # Passer (ne rien écrire dans le fichier).
                if choix_server_hote == "1": # Si le choix est 1.
                    logger_action("Serveur FTP", identifiant, "CREER FICHIER", "non concerne", destination) # Créer le log suivant.
                elif choix_server_hote == "2": # Si le choix est 2.
                    logger_action(Hote, identifiant, "CREER FICHIER", "non concerne", destination) # Créer le log suivant.
                print(f"Fichier créé avec succès : {destination}") # Afficher le message.

            elif choix == "2": # Si le choix est 2.
                os.makedirs(destination, exist_ok=False)  # Créer le dossier uniquement s'il n'existe pas.
                if choix_server_hote == "1": # Si le choix est 1.
                    logger_action("Serveur FTP", identifiant, "CREER DOSSIER", "non concerne", destination,) # Créer le log suivant.
                elif choix_server_hote == "2": # Si le choix est 2.
                    logger_action(Hote, identifiant, "CREER DOSSIER", "non concerne", destination) # Créer le log suivant.
                print(f"Dossier créé avec succès : {destination}") # Afficher le message.

        except ValueError as e: # En cas de Value Error.
            message_erreur = str(e) # Convertir l'erreur en chaîne de caractère.
            print(f"Erreur : {message_erreur}") # Affichier le message d'erreur.
        except FileExistsError: # Si le fichier existe déjà.
            print("Erreur : Le fichier ou dossier existe déjà.") # Afficher le message d'errreur.
        except Exception as e: # En cas d'erreur.
            print(f"Erreur lors de la création : {e}") # Afficher le message d'erreur.
            continue # Continuer.
        else: # Sinon.
            break # Quitter la boucle.

def deplacer_fichier_dossier(): # Définition déplacer un fichier ou dossier.    
    print("\\Déplacer FICHIER/DOSSIER ") # Afficher la définition

    while True: # Tant que c'est vrai
        try: # Essayer
            choix_server_hote = input("sur ftp (1) ou client (2) ? ") # Demande de connexion au FTP ou au client.
            if choix_server_hote == "1" : # Si le choix est 1.
                acceder_ftp(identifiant, motdepasse) # Lancer la définition acceder au FTP.
            elif choix_server_hote == "2" : # Si le choix est 2.
                Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
                ip_input(Hote) # Lancer la définition ip_input.
            if choix_server_hote not in ("1", "2"): # Si le choix n'est ni 1 et 2.
                raise ValueError("La valeur saisie n'est pas 1 ou 2 ! ") # Arrêt de l'éxecution.
            choix = input("Souhaitez-vous déplacer un fichier (1) ou un dossier (2) ? : ") # Demander si déplacer un fichier ou dossier.
            if choix not in ("1", "2"): # Si le choix n'est ni 1 ni 2.
               raise ValueError("La valeur saisie n'est pas 1 ou 2 !") # Arrêt de l'éxecution.
            source = input("Entrez le chemin COMPLET du fichier ou dossier à déplacer (ex : C:/Massimo/Paris ou /REMOTE_PROJET/VILLE/...) : ").strip() # Demander le chemin du ficher ou dossier.
            if not os.path.exists(source): # Si le chemin n'existe pas.
               raise ValueError("Le chemin spécifié n'existe pas !") # Arrêt de l'éxecution.
           
            destination = input("Entrez le chemin COMPLET de destination (ex : C:/Massimo/Juillet/Paris ou /REMOTE_PROJET/VILLE/... : ").strip() # Demander le nouveau chemin.
            dossier_parent = os.path.dirname(destination) # Extraire le chemin dossier.
            if not os.path.isdir(dossier_parent): # Si le dossier n'existe pas.
                raise ValueError("Le chemin de DESTINATION est incorrect !") # Arrêt de l'éxecution.

            confirmation = input("Êtes-vous certain de vouloir déplacé cet élément et son contenu ? (o/n): ") # Demander la confirmation.
            if confirmation not in ("o", "n"): # Si ce n'est pas o ou n.
               raise ValueError("La valeur saisie n'est pas o ou n !") # Arrêt de l'éxecution.

            shutil.move(source, destination) # Déplacer l'élément de l'ancien vers le nouveau chemin.

            if choix == "1": # Si le choix est 1.
                if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", identifiant, "DEPLACER FICHIER", source, destination) # Créer le log suivant.
                elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, identifiant, "DEPLACER FICHIER", source, destination) # Créer le log suivant.
                print(f"Fichier déplacé avec succès : {source} ==> {destination}") # Afficher le message.
            elif choix == "2": # Si le choix est 2.
                if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", identifiant, "DEPLACER DOSSIER", source, destination) # Créer le log suivant.
                elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, identifiant, "DEPLACER DOSSIER", source, destination) # Créer le log suivant.
                print(f"Dossier déplacé avec succès vers : {source} ==> {destination}") # Afficher le message.

        except ValueError as e: # En cas de Value Error.
            print(f" Erreur : {e}") # Afficher le message d'erreur.
        except Exception as e: #En cas d'erreur.
            print(f"Erreur lors de la suppression de l'élément ! : {e}") # Affiche le message d'erreur.
            continue # Continuer.
        else: # Sinon
            break # Sortir de la boucle
        
        
def supprimer_fichier_dossier(): # Définition supprimer un fichier ou dossier.
    print("\\Supprimer FICHIER/DOSSIER ") # Afficher le message de définition.

    while True: # Tant qeu c'est vrai.
        try: # Essayer
            choix_server_hote = input("sur ftp (1) ou client (2) ? ") # Demande de connexion au FTP ou au client.
            if choix_server_hote == "1" : # Si le choix est 1.
                acceder_ftp(identifiant, motdepasse) # Lancer la définition acceder au FTP.
            elif choix_server_hote == "2" : # Si le choix est 2.
                Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
                ip_input(Hote) # Lancer la définition ip_input.
            if choix_server_hote not in ("1", "2"): # Si le choix n'est ni 1 et 2.
                raise ValueError("La valeur saisie n'est pas 1 ou 2 ! ") # Arrêt de l'éxecution.
            choix = input("Souhaitez-vous supprimer un fichier (1) ou un dossier (2) ? : ") # Demander si fichier ou dossier à supprimer.
            if choix not in ("1", "2"): # Si le choix n'est ni 1 ni 2.
               raise ValueError("La valeur saisie n'est pas 1 ou 2 !") # Arrêt de l'éxecution.
            source = input("Entrez le chemin COMPLET du fichier ou du dossier à supprimer (ex : C:/Massimo/Paris.txt ou /REMOTE_PROJET/VILLE/...) : ").strip() # Demander le chemin en supprimant les espaces.
            if not os.path.exists(source): # Si le chemin n'existe pas.
               raise ValueError("Le chemin spécifié n'existe pas !") # Afficher le message d'erreur.

            confirmation = input("Êtes-vous certain de vouloir supprimé cet élément et son contenu ? (o/n): ") # Demander la confirmation.
            if confirmation not in ("o", "n"): # Si ce n'est pas o ou n.
               raise ValueError("La valeur saisie n'est pas o ou n !") # Arrêt de l'éxecution.
            
            if confirmation == "o" : # Si  c'est o.
                if choix == "1": # Si c'est un fichier.
                    if not os.path.isfile(source): # Si l'élement n'est pas un fichier.
                        raise ValueError("Le chemin renseigné ne renvoie pas un fichier !") # Arrêt de l'éxecution.
                    os.remove(source) # Supprime le fichier.
                    if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", identifiant, "SUPPRESSION FICHIER", source, "non concerne") # Créer le log suivant.
                    elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, identifiant, "SUPPRESSION FICHIER", source, "non concerne") # Créer le log suivant.
                    print(f"Fichier supprimé avec succès : {source}") # Afficher le message.

                elif choix == "2": # Si c'est un dossier.
                    if not os.path.isdir(source): # Si l'élément n'est pas un dossier.
                        raise ValueError("Le chemin renseigné ne renvoie pas un dossier !") # Arrêt de l'éxecution.
                    shutil.rmtree(source) # Supprimé le dossier.
                    if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", identifiant, "SUPPRESSION DOSSIER", source, "non concerne") # Créer le log suivant.
                    elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, identifiant, "SUPPRESSION DOSSIER", source, "non concerne") # Créer le log suivant.
                    print(f"Dossier supprimé avec succès : {source}") # Affichier le message.
            elif confirmation == "n" :  # Si la réponse est n.
                print("La suppression a été annulée !") # Afficher le message.

        except ValueError as e: # En cas de Value Error.
            print(f" Erreur : {e}") # Afficher le message d'erreur.
        except Exception as e: # En cas d'erreur.
            print(f"Erreur lors de la suppression de l'élément ! : {e}") # Afficher l'erreur.
            continue # Continuer.
        else: # Sinon.
            break # Sortir de la boucle


def lister_arborescence(chemin=None, prefixe=""):  # Parcourt récursivement et affiche l’arborescence d’un dossier

    choix_server_hote = input("sur ftp (1) ou client (2) ? : ") # Demander le choix client/FTP.
    if choix_server_hote == "1" : # Si le choix est FTP.
        acceder_ftp(identifiant, motdepasse) # Appeler la défintion.
        Hote = "SERVEUR FTP"
    elif choix_server_hote == "2" : # Si le choix est client.
        Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
        ip_input(Hote) # Appeler la définition avec la valeur HOTE.
    chemin = input("Saisissez le chemin (ex : C:/Massimo/Paris ou /remote_projet/marseille/) : ").strip() # Demander le chemin en supprimant les espaces.
    if not os.path.isdir(chemin): # Si ce n'est pas un dossier.
        raise ValueError("Le chemin indiqué n'existe pas ou n'est pas un dossier !") # Message d'erreur.
    print(f"Contenu de : {chemin}") # Afficher le contenu du chemin.

    logger_action(Hote, identifiant, "LISTE ARBORESCENCE", chemin, "non concerné")  # Log du listage

    try:  # Tente d’exécuter le bloc de code
        for element in os.listdir(chemin):  # Liste les éléments (fichiers et dossiers) du chemin donné
            chemin_complet = os.path.join(chemin, element)  # Construit le chemin complet de l’élément
            if os.path.isdir(chemin_complet):  # Vérifie si le chemin complet est un dossier
                print(f"{prefixe}[D] {element}/")  # Affiche le nom du dossier avec un indicateur [D]
            else:  # Si ce n’est pas un dossier
                print(f"{prefixe}[F] {element}")  # Affiche le nom du fichier avec un indicateur [F]
    except Exception as e:  # Intercepte toute exception
        print(f"Erreur : {e}")  # Affiche le message d’erreur rencontré
    

def naviguer_arborescence(): # Définition naviguer.
    print("\nNaviguer dans l'arborescence des répertoires ") # Afficher la définition.

    while True: # Tant que c'est vrai.
        try:  # Essayer.
            choix_server_hote = input("sur ftp (1) ou client (2) ? ") # Demander le choix client/FTP.
            if choix_server_hote == "1" : # Si le choix est FTP.
                acceder_ftp(identifiant, motdepasse) # Appeler la défintion.
                Hote = "SERVEUR FTP"
            elif choix_server_hote == "2" : # Si le choix est client.
                Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
                ip_input(Hote) # Appeler la définition avec la valeur HOTE.
            chemin = input("Saisissez le chemin (ex : C:/Massimo/Paris ou /remote_projet/marseille/) : ").strip() # Demander le chemin en supprimant les espaces.
            if not os.path.isdir(chemin): # Si ce n'est pas un dossier.
                raise ValueError("Le chemin indiqué n'existe pas ou n'est pas un dossier !") # Message d'erreur.
            print(f"Contenu de : {chemin}") # Afficher le contenu du chemin.

            while True: # Tant que c'est vrai.
                try: # Essayer.
                    contenu = os.listdir(chemin) # Lister les fichiers/dossiers.

                    fichiers = [] # Création liste fichiers.
                    dossiers = [] #Création liste dossiers.

                    for element in contenu: # Pour chaque élement qui se trouve dans contenu
                        chemin_complet = os.path.join(chemin, element) # chemin complet correspond au chemin de départ jusqu'à élément sélectionner.
                        if os.path.isfile(chemin_complet): # Si c'est un fichier, alors on l'ajoute à la liste "fichiers".
                            fichiers.append(element) # Ajout de l'élément à la liste.
                        elif os.path.isdir(chemin_complet): # Si c'est un dossier, alors on l'ajoute à la liste "dossiers".
                            dossiers.append(element) # Ajout de l'élément à la liste.

                    print(f"\\Contenu de : {chemin}") # Affichage ligne d'information.
                    print("\n========== DOSSIERS ==========") # Affichage ligne d'information.
                    for index, nom_dossier in enumerate(dossiers): # Boucle for pour chaque dossier, les numérotés.
                        print(f"  {index + 1}. {nom_dossier}") # Afficher le numéro associé au dossier.

                    print("\n========== FICHIERS ==========") # Affichage ligne d'information.
                    for nom_fichier in fichiers: # Boucle for pour afficher chaque nom de fichier de la liste fichier.
                        print(f"  - {nom_fichier}") # Afficher le nom du fichier.

                    print("\n========== OPTIONS ==========") # Affichage ligne d'information.
                    print("  numéro : Aller dans un sous-dossier") # Afficher l'option.
                    print("    r   : Revenir au dossier précédent") # Afficher l'option.
                    print("    q    : Fermer l'explorateur") # Afficher l'option.

                    choix = input("Que souhaitez-vous faire ? ").strip() # Demander l'action.

                    if choix.isdigit(): # Si la valeur saisie est un chiffre entier positif.
                        numero = int(choix) # Convertir la valeur par un entier.
                        if 1 <= numero <= len(dossiers): # Si le numéro saisi est présent dans la liste énumérée.
                            sous_dossier = dossiers[numero - 1] # Récupérer le nom du sous-dossier en retirant 1.
                            chemin = os.path.join(chemin, sous_dossier) # Former le nouveau chemin.
                        else: # Sinon
                            print("NUMÉRO de dossier invalide !") # Afficher le message d'erreur.
                    
                    elif choix == "r": # Si le choix est r.
                        dossier_parent = os.path.dirname(chemin) # Récupérer le chemin du dossier parent.
                        if os.path.isdir(dossier_parent): # Si le dossier existe.
                            chemin = dossier_parent # Chemin égla le dossier parent.
                        else: # Sinon.
                            continue # Continuer.

                    elif choix == "q": # Si le choix est q.
                        print("Au revoir !") # Afficher le message.
                        break   # Quitte la boucle.
 
                    if choix not in ("r", "q"):
                        raise ValueError("Veuillez saisir r pour remonter ou q pour quitter ") # Arrêt de l'éxecution.
                
                except ValueError as erreur: # En cas de Value Error.
                    print(f"Une erreur s'est produite : {erreur}") # Afficher le message d'erreur.
                except Exception as erreur: # En cas d'erreur.
                    print(f"Une erreur est survenue ! : {erreur}") # Afficher le message d'erreur.
            logger_action(Hote, identifiant, "NAVIGATION ARBORESCENCE", chemin, "non concerné")  # Log de la navigation
        except ValueError as erreur: # En cas de Value Error.
                print(f"Une erreur s'est produite : {erreur}") # Afficher le message d'erreur.
        break # Quitter.


def lister_dossier_fichier(): # Définition lister dossier fichier.
    print("\nLister les DOSSIERS, les SOUS-DOSSIERS et les FICHIERS") # Afficher le message de la définition.
    
    while True: # Tant que c'est vrai.
        try: # Essayer.
            choix_server_hote = input("sur ftp (1) ou client (2) ? ") # Demande de connexion au FTP ou au client.
            if choix_server_hote == "1" : # Si le choix est 1.
                acceder_ftp(identifiant, motdepasse) # Lancer la définition acceder au FTP.
                Hote = "SERVEUR FTP"
            elif choix_server_hote == "2" : # Si le choix est 2.
                Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
                ip_input(Hote) # Lancer la définition ip_input.
            if choix_server_hote not in ("1", "2"): # Si le choix n'est ni 1 et 2.
                raise ValueError("La valeur saisie n'est pas 1 ou 2 ! ") # Arrêt de l'éxecution.
            chemin = input("Saisissez le chemin à lister (ex : C:/Massimo/Paris) ou /remote_projet/ville/...) : ").strip() # Demander le chemin 
            if not os.path.isdir(chemin): # Vérifier si le chemin existe.
                raise ValueError("Le chemin est incorrect ou n'existe pas !") # Arrêt de l'éxecution.

            dossiers = [] # création de la liste dossier
            sous_dossiers = [] # création de la liste sous-dossier
            fichiers = [] # création de la liste fichier
            
            logger_action(Hote, identifiant, "LISTE DOSSIER/FICHIERS", chemin, "non concerné")  # Log du listing

            # Parcours récursif de l'arborescence
            for racine, dirs, files in os.walk(chemin): # Parcourt récursivement le dossier et les sous-dossiers.
                if racine == chemin: # Si racine est égal au chemin.
                    for d in dirs: # Pour chaque dossier dans dirs.
                        dossiers.append(os.path.join(racine, d)) # Ajouter le chemin complet à la liste dossier.
                else: # Sinon.
                    for d in dirs: # Pour chaque sous dossier dans dirs.
                        sous_dossiers.append(os.path.join(racine, d)) # Ajoute les sous-dossiers dans la liste sous-dossiers.
                for f in files: # Pour chaque fichier présent.
                    fichiers.append(os.path.join(racine, f)) # Ajouter le chemin compler à la lsite fichiers.

            print(f"\n===DOSSIERS dans {chemin} :") # Afficher le la rubrique DOSSIERS avec le chemin.
            for d in dossiers: # Pour chaque dossier dans la liste dossier.
                print(f" - {d}") # Afficher le chemin complet avec un tiert.

            print(f"\n===SOUS-DOSSIERS :") # Afficher le la rubrique SOUS-DOSSIERS avec le chemin.
            for sd in sous_dossiers: # Pour chaque sous dossier dans la liste sous dossier.
                print(f" - {sd}") # Afficher le chemin complet avec un tiert.

            print(f"\n===FICHIERS :") # Afficher le la rubrique FICHIERS avec le chemin.
            for f in fichiers: # Pour chaque fichier dans la liste fichiers.
                print(f" - {f}") # Afficher le chemin complet avec un tiert.
    
        except ValueError as e: # En cas de Value Error.
            print(f"Erreur : {e}") # Afficher le message d'erreur.

        except Exception as e: # En cas d'erreur 
            print(f"Erreur inattendue lors du listage : {e}") # Afficher le message d'erreur.
            continue # Continuer
        else: # Sinon
            break #  Quitter la boucle



def sauvegarder_fichier_dossier(ftp, identifiant): # Définition sauvergader les fochiers et dossiers.
    print("\nSauvegarder FICHIER/DOSSIER du client vers le serveur FTP") # Afficher le message de la définition.

    ftp = acceder_ftp(identifiant, motdepasse) # lancer la définition de connexion au FTP.
    if ftp is None: # Si FTP ne renvoie rien.
        raise ValueError("Impossible de se connecter au serveur FTP.") # Arrêt de l'éxecution.
    
    Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
    ip_input(Hote)  # Vérifier l'adresse IP.

    try: # Essayer.
        choix = input("Souhaitez-vous sauvegarder un (1) ou plusieurs fichiers (2) ? :") # Demander si sauvergarder un ou plusieur fichier.
        if choix not in ("1", "2"): # Si ce n'est pas égal à 1 ou 2.
            raise ValueError("La valeur saisie n'est pas 1 ou 2 !") # Arrêt de l'éxecution.

        source = input("Entrez le chemin COMPLET LOCAL du fichier ou dossier à envoyer vers le serveur FTP : ").strip() # Demander le chemin local en retirant les espaces.
        destination = input("Entrez le chemin COMPLET de destination sur le serveur FTP depuis le dossier de votre ville : ").strip() # Demander la destination en retirant les espaces.
        try: # Essayer 
            ftp.cwd(destination) # Se déplacer dans le dossier de destination.
        except Exception: # En cas d'erreur
            print(f" Dossier FTP non trouvé. Création de : {destination}") # Afficher le message d'erreur.
            try: # Essayer.
                for part in destination.strip("/").split("/"): # Pour chaque dossiers, retirer les /
                    if part not in ftp.nlst(): # Si le dossier n'existe pas.
                        ftp.mkd(part) # Créer le dossier.
                    ftp.cwd(part) # Entrer dans le dossier nouvellement créé.
            except Exception as e: # En cas d'erreur.
                raise Exception(f"Impossible de créer le chemin FTP : {e}") # Arrêt de l'éxecution.

        if choix == "1": # Si le choix est 1.
            nom_fichier = os.path.basename(source) # Extrait le nom du fichier.

            print(f"Envoi du fichier '{source}' vers '{destination}/{nom_fichier}' ...") # Affichage du message.
            with open(source, "rb") as f: # Ouvir le fichier en mode retry binari pour le lire.
                ftp.storbinary(f"STOR {nom_fichier}", f) # Sauvegarder le fichier dans le serveur FTP.
            logger_action("Serveur FTP", identifiant, "SAUVEGARDE FICHIER", source, destination) # Créer le log suivant.
            print(f"Fichier importé avec succès vers : {destination}/{nom_fichier}") # Afficher le message.

        elif choix == "2": # Si le choix est 2.
            if not os.path.isdir(source): # Si le chemin n'est pas un dossier.
                raise ValueError("Le chemin fourni n'est pas un dossier valide.") # Arrêt de l'éxecution.

            fichiers = os.listdir(source) # Lister les fichiers 

            for fichier in fichiers: #Pour chaque fichier dans la liste fichiers.
                chemin_fichier = os.path.join(source, fichier) # Former le chemin complet pour accéder au fichier.

                if os.path.isfile(chemin_fichier): # Si c'est un fichier.
                    print(f"Envoi de '{chemin_fichier}' vers '{destination}/{fichier}' en cours !") # Afficher le message.
                    with open(chemin_fichier, "rb") as f: # Ouvrir le fichier en retry binary.
                        ftp.storbinary(f"STOR {fichier}", f) # Sauvegarde vers le serveur FTP.
                    print(f"Sauvegardé : {fichier}") # Afficher le message.
                else: # Sinon
                    continue # Continuer
                
            logger_action(Hote, identifiant, "SAUVEGARDE DOSSIER", source, destination) # Créer le log suivant.
            print(f"Tous les fichiers de '{source}' ont été sauvegardés dans '{destination}'.") # Affichage du message.

    except Exception as e: # En cas d'erreur.
        print(f" Erreur : {e}") # Afficher le message d'erreur.


def restaurer_fichier_dossier(): # Définition restauration fichier ou dossier.
    print("\nRestaurer FICHIER/DOSSIER du serveur FTP vers le CLIENT") # Afficher le message de la définition.

    ftp = acceder_ftp(identifiant, motdepasse) # Lancer la connexion FTP.
    if ftp is None: # Si FTP ne renvoie rien.
        raise ValueError(" Impossible de se connecter au serveur FTP.") # Arre^t de l'éxecution.
    
    Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
    ip_input(Hote)  # Vérifie l'adresse IP.

    try: # Essayer

        choix = input("Souhaitez-vous restaurer un (1) ou plusieurs fichiers d'un dossier (2) ? :") # Demander le choix
        if choix not in ("1", "2"): # Si le choix n'est ni 1 ni 2.
            raise ValueError("La valeur saisie n'est pas 1 ou 2 !") # Arrêt de l'éxecution.

        source = input("Entrez le chemin COMPLET du fichier ou dossier à restaurer sur le serveur FTP (depuis le dossier de votre ville): ").strip() # Demander la source.
        destination = input("Entrez le chemin COMPLET LOCAL de destination sur le PC distant : ").strip() # Demander la destination.
  
        if not os.path.exists(destination): # Si la destination n'existe pas
            os.makedirs(destination) # On crée le dossier          

        if choix == "1" : # Si le choix est 1.
            nom_fichier = os.path.basename(source) # Extrait le nom du fichier.
            dossier_ftp = os.path.dirname(source) # Extrait le nom du dossier.

            ftp.cwd(dossier_ftp) # Aller au répertoire où se trouve le fichier

            destination = os.path.join(destination, nom_fichier) # Définition du chemin distant avec le nom du fichier
            print(f"Récupération du fichier '{nom_fichier}' vers '{destination}' ...") # Afficher message de confirmation

            with open(destination, "wb") as f: # Ouverture du fichier
                    ftp.retrbinary(f"RETR {nom_fichier}", f.write) # Transformation du fichier en binaire
                    
            logger_action(Hote, identifiant, "RESTAURATION FICHIER", source, destination) # Créer le log suivant.
            print(f"Fichier restauré avec succès vers : {destination}") # Afficher le message de confirmation avec la destination

        elif choix == "2":  # Si le choix est 2.
            ftp.cwd(source)  # On s'assure que c'est un dossier FTP.
            fichiers = ftp.nlst()  # Liste les fichiers et sous-dossiers.

            for fichier in fichiers:  # Pour chaque fichier dans la liste.
                try: # Essayer.
                    ftp.size(fichier) # Si pas d'erreur rencontrée, c'est un fichier.
                    chemin_destination = os.path.join(destination, os.path.basename(fichier)) # Défini la destiantion avec me nom du fichier + la destination locale.
                    print(f"Téléchargement de '{fichier}' vers '{chemin_destination}' ...") # Affichage du message.

                    with open(chemin_destination, "wb") as f:# Ouvrir le fichier de la variable destination en write binary.
                        ftp.retrbinary(f"RETR {fichier}", f.write) # Télcharger le fichier en mode binaire et son contenu.
                    print(f" Téléchargé : {fichier}") # Affichage du message.
                    logger_action(Hote, identifiant, "RESTAURATION FICHIER", source, chemin_destination) # Logger l'action.

                except Exception as e: # Exception en cas d'erreur.
                    print(f" Ignoré (dossier ou erreur) : {fichier} — {e}") # Message d'erreur.

            print(f"\nTous les fichiers du dossier '{source}' ont été restaurés dans '{destination}'.") # Afficher message de fin.

    except Exception as e: # Exception.
        print(f" Erreur : {e}") # Afficher l'erreur.


def sauvegarde_automatique(): # Définition sauvegarde automatique.
    date_execution = "2025-06-28 14:51:00" # Définition de la date et l'heure.
    hote = "192.168.1.53" # Adresse IP du client.
    source = r"C:/Users/Massi/Music/A IMPRIMER/test.txt" # Chemin source depuis le client.
    destination = "/massimo2/" # Chemin destiantion depuis le serveur.

    date_exec = datetime.datetime.strptime(date_execution, "%Y-%m-%d %H:%M:%S") # Attente jusqu'à l'heure d'exécution
    now = datetime.datetime.now()
    delai = (date_exec - now).total_seconds()# Le delai est égal la date d'execution - date actuelle.
    if delai > 0: # Si le délai est supérieur à 0.
        time.sleep(delai) # Attendre le créneau.
    
    elif delai <= 0: # Si le délai est supérieur à 0.
        return # annuler la sauvegarde

    ftp = acceder_ftp(identifiant, motdepasse) # Lancer la défintion connexion au ftp.
    if not ftp:
        return # Retourner FTP.

    try: # Essayer.
        ftp.cwd(destination)  # Aller dans le dossier destination.
    except Exception as e: # Exception
        print(f"Erreur pour se déplacer dans le dossier FTP : {e}")

    def sauvegarder_fichier_versionne(chemin_local): # Définition sauvegarde avec version.
        fichiers_distant = ftp.nlst() # Lister les fichiers présent sur le FTP.
        nom_fichier = os.path.basename(chemin_local) # Extraire le nom du fichier à partir du chemin.
        nom, ext = os.path.splitext(nom_fichier) # Séparer le nom et l'extension.

        if 'v' in nom: # Si la lettre V est présente dans le nom.
            prefixe, version = nom.rsplit('v', 1) # Séparer le nom à partir du dernier v.
            if version.isdigit(): # Si le charactère qui suit le v est un chiffre.
                numero_version = int(version) # C'est le numéro de version.
            else: # Sinon.
                prefixe = nom # Préfixe = nom du fichier
                numero_version =  1 # Version commence à 1.
        else: # Sinon.
            prefixe = nom # Préfixe = nom du fichier
            numero_version = 1 # Version commence à 1.


        while True: # Tant que c'est vrai.
            nouveau_nom = f"{prefixe}v{numero_version}{ext}" # Créer le nom avec le numéro de version et l'extension.
            if nouveau_nom not in fichiers_distant: # Si le nom n'est pas encore utilisé.
                break # Quitter.
            numero_version += 1 # Incrémenter le numéro de version.

        with open(chemin_local, "rb") as f: # Ouverture du ficher.
            ftp.storbinary(f"STOR {nouveau_nom}", f) # Transfert du fichier.
        logger_action(hote, identifiant, "SAUVEGARDE FICHIER AUTOMATIQUE", chemin_local, ftp.pwd()) # Logger l'action.

    if os.path.isfile(source): # Si source est un fichier.
        sauvegarder_fichier_versionne(source) # Appelle de la fonction pour sauvegarder la version.
    elif os.path.isdir(source): # Si c'est un dossier.
        fichiers = os.listdir(source) #Lister les fichiers et dossiers qui sont dans source.
        for fichier in fichiers: # Pour chaque fichier dans fichiers.
            chemin_fichier = os.path.join(source, fichier) # Former le chemin complet vers le fichier/dossier.
            if os.path.isfile(chemin_fichier): # Si c'est un fichier.
                sauvegarder_fichier_versionne(chemin_fichier) # Apelle de la fonction pour sauvegarder la version.


threading.Thread(target=lambda: sauvegarde_automatique(), daemon=True).start() # Lancer la définition en arrière plan.

def port_specifique(Hote, Port, Techno): # Définition pour le port indivuduel.

    now = datetime.datetime.now().date() # Récupérer la date actuelle.
    now1 = datetime.datetime.now().time() # Récupérer l'heure actuelle.
    print("Date :", now.strftime('%A %d %B %y')) # Afficher la date au format lisible.
    print("Horaire :", now1.strftime('%H:%M:%S')) # Afficher l'heure au format lisible.

    filename = f"scan_de_port_{now.strftime('%d-%m-%Y')}____{now1.strftime('%H-%M-%S')}.txt" # Création d'un fichier scan_de_port avec la date et l'heure du jour.
    f = open(filename, 'w', encoding="utf-8") # Ouverture du fichier concerné.

    f.write("La date : " + str(now) + "\n") # Ecriture de la date dans le fichier.
    f.write("L'heure : " + now1.strftime('%H:%M:%S') + "\n") # Ecriture de l'heure dans le fichier.
    f.write("Adresse IP de l'équipement : " + Hote + "\n") # Ecriture de l'adresse IP dans le fichier.
    f.write('+-----------+---------------+\n') # Ecriture dans le fichier.
    f.write('| Port      |   État        |\n') # Ecriture dans le fichier.
    f.write('+-----------+---------------+\n') # Ecriture dans le fichier.
    

    while True: # Tant que c'est vrai.
        start = None # Initialisation de la variable start.
        try: # Essayer

            if not str(Port).isdigit(): # Si le port n'est pas un chiffre .
                raise ValueError("La valeur saisie n'est pas un chiffre entier positif ! ") # Arrêt de l'éxecution et déclaration de valueError.
            Port = int(Port) # La valeur du port est numérique.
            if Port < 1 or Port > 65535: # Si le port est inférieur à 1 ou supérieur à 65535.
                raise ValueError("Le port doit être compris entre 1 et 65535 ! ") # Arrêt de l'éxecution et déclaration de valueError.
            elif Techno != "1" and Techno != "2": # Si la technologie n'est pas TCP ni UDP.
                raise ValueError("Protocole non reconnu ! ") # Arrêt de l'éxecution et déclaration de valueError.
            
            start = time.time() # Enregistrement de l'heure actuelle dans la variable start.

            if Techno == "1":  # Si le protocole est TCP.                
                f.write("==> 1ère version en TCP.....\n") # Ecriture dans le fichier la ligne TCP.
                connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Création d'une connexion réseau en IPV4 TCP avec l'hôte.
                connexion_principale.settimeout(1) # Patienter pendant 1 seconde avant d'abandonner.
                connexion_principale.connect((Hote, Port)) # Ouvrir une connexion avec l'hôte et le port concerné.
                print("Le port", Port, "est ouvert") # # Afficher le message avec le port et l'état ouvert.
                f.write("==> Le port " + str(Port) + " : ouvert\n") # Ecriture du message dans le fichier.
                
            elif Techno == "2":  # Si le protocole est UDP.
                f.write("==> 1ère version en UDP.....\n") # Ecriture dans le fichier la ligne UDP.
                connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Création d'une connexion réseau en IPV4 UDP avec l'hôte.
                connexion_principale.settimeout(0.2) # Patienter pendant 0.2 seconde avant d'abandonner.
                connexion_principale.connect((Hote, Port)) # Ouvrir une connexion avec l'hôte et le port concerné.
                print("Le port", Port, "est ouvert") # Afficher le message avec le port et l'état ouvert.
                f.write("==> Le port " + str(Port) + " : ouvert\n") # Ecriture du message dans le fichier.

        except ValueError as e: # Exception sur une erreur de valeur.
            message_erreur = str(e) # Convertir l'erreur en chaîne de caractère.
            print(f"Erreur : {message_erreur}") # Afficher le message d'erreur lié à l'erreur rencontrée.

            if "Le port doit être compris entre 1 et 65535 !" in message_erreur: # Si le message contient "Le port doit être compris entre 1 et 65535 !"."
                print("Recommencer la procédure !") # Afficher le message.
                break # Sortir de la boucle.
            
            elif "La valeur saisie n'est pas un chiffre entier positif !" in message_erreur: # Si le message contient "La valeur saisie n'est pas un chiffre entier positif !".
                print("Recommencer la procédure !") # Afficher le message.
                break # Sortir de la boucle.
            
            elif "Protocole non reconnu !" in message_erreur: # Si le message contient "Protocole non reconnu !".
                print("Recommencer la procédure !") # Afficher le message.
                break # Sortir de la boucle.

        except Exception as e: # Exception sur n'importe quelle erreur.
            print("Le port", Port, "est fermé") # Afficher le message le port n° est fermé.
            f.write("Le port " + str(Port) + " : fermé\n") # Ecrire dans le fichier l'état du port.
            try: # Essayer
                connexion_principale.close() # Fermer la connexion.
            except: # Excepetion (erreur)
                pass # Passer

        finally :  # Enfin        
            if start is not None:  # Si start est défini.
                end = time.time()  # Noter le temps dans la variable end.
                print("Durée du scan :", round(end - start, 2), "secondes\n")  # Afficher la durée du scan.
                f.write("Le scan du port a duré : " + str(round(end - start, 2)) + " secondes\n")  # Écrire la durée.

            if 'connexion_principale' in locals():  # Si la connexion est ouverte.
                connexion_principale.close()  # Fermer la connexion.
            logger_action(Hote, identifiant, f"Scan PORT spécifique {Port} ({'TCP' if Techno == '1' else 'UDP'})", "non concerné", f"{round(end - start, 2)} sec") # Créer le log suivant.    

            break  # Sortir de la boucle après écriture.



def plage_de_port(Hote, Debut, Fin, Techno): # Définition pour la plage de port.

    now = datetime.datetime.now().date() # Récupérer la date actuelle.
    now1 = datetime.datetime.now().time() # Récupérer l'heure actuelle.
    print("Date :", now.strftime('%A %d %B %y')) # Afficher la date au format lisible.
    print("Horaire :", now1.strftime('%H:%M:%S')) # Afficher l'heure au format lisible.

    filename = f"plage_de_ports_{now.strftime('%d-%m-%Y')}____{now1.strftime('%H-%M-%S')}.txt" # Création d'un fichier plage_de_ports avec la date et l'heure du jour.
    f = open(filename, 'w', encoding="utf-8") # Ouverture du fichier concerné.

    f.write("La date :" + str(now) + "\n") # Ecriture de la date dans le fichier.
    f.write("L'heure :" + now1.strftime('%H:%M:%S') + "\n") # Ecriture de l'heure dans le fichier.
    f.write("Adresse IP de l'équipement : " + Hote + "\n") # Ecriture de l'adresse IP dans le fichier.
    f.write('+-----------+---------------+\n') # Ecriture dans le fichier.
    f.write('| Port      |   État        |\n') # Ecriture dans le fichier.
    f.write('+-----------+---------------+\n') # Ecriture dans le fichier.
    
    while True: # Tant que c'est vrai.
        try: # Essayer
            if not str(Debut).isdigit(): # Si le port de début n'est pas un chiffre.
                raise ValueError("La valeur DEBUT saisie n'est pas un chiffre entier positif ! ") # Arrêt de l'éxecution et déclaration de valueError.
            if not str(Fin).isdigit(): # Si le port de fin n'est pas un chiffre.
                raise ValueError("La valeur FIN saisie n'est pas un chiffre entier positif ! ") # Arrêt de l'éxecution et déclaration de valueError.
            Debut = int(Debut) # La valeur début est numérique.
            Fin = int(Fin) # La valeur début est numérique.
            if Debut < 1 or Fin > 65535: # Si Début est inférieur à 1 ou supérieur à 65535.
                raise ValueError("Les ports doivent être compris entre 1 et 65535.") # Arrêt de l'éxecution et déclaration de valueError.
            elif Debut > Fin: # Si début est supérieur à fin.
                raise ValueError("Le port de fin ne peut pas être inférieur au port de début.") # Arrêt de l'éxecution et déclaration de valueError.
            elif Techno != "1" and Techno != "2": # Si le protocole n'est pas TCP ni UDP.
                raise ValueError("Protocole non reconnu, choisissez 1 pour TCP ou 2 pour UDP.") # Arrêt de l'éxecution et déclaration de valueError.
            
            break # Quitter la boucle si aucune erreur.

        except ValueError as e: # Exception sur une erreur de valeur.

            message_erreur = str(e) # Convertir l'erreur en chaîne de caractère.
            print(f"Erreur : {message_erreur}") # Afficher le message d'erreur lié à l'erreur rencontrée.

            if "La valeur DEBUT saisie n'est pas un chiffre entier positif !" in message_erreur: # Si le message contient "Le port doit être compris entre 1 et 65535 !"."
                Debut = input("Quel est le premier port de la plage ? : ") # Redemander le nuémro de port de début.            
            elif "La valeur FIN saisie n'est pas un chiffre entier positif !" in message_erreur: # Si le message contient "La valeur saisie n'est pas un chiffre entier positif !".
                Fin = input("Quel est le dernier port de la plage ? : ") # Redemander le nuémro de port de fin.
            elif "Les ports doivent être compris entre 1 et 65535." in message_erreur: # Si le message contient "Protocole non reconnu !".
                Debut = input("Quel est le premier port de la plage ? : ") # Redemander le nuémro de port de début.
                Fin = input("Quel est le dernier port de la plage ? : ") # Redemander le nuémro de port de fin.            
            elif "Le port de fin ne peut pas être inférieur au port de début." in message_erreur: # Si le message contient "Protocole non reconnu !".
                Fin = input("Quel est le dernier port de la plage ? : ") # Redemander le nuémro de port de fin.
            elif "Protocole non reconnu, choisissez 1 pour TCP ou 2 pour UDP." in message_erreur: # Si le message contient "Protocole non reconnu !".
                Techno = input("Est-ce du TCP (choix 1) ou de l'UDP (choix 2) ? : ") # Redemander le protoocle a utilisé.
                       
    resultat_all_ports = [] # Création de la liste Resultat_all_ports.
    if Techno == "1" : # Si le protocole est TCP.
        f.write("==> Protocole utilisé : TCP\n") # Ecriture du message dans le fichier.
    elif Techno == "2" : # Si le protocole est UDP
        f.write("==> Protocole utilisé : UDP\n") # Ecriture du message dans le fichier.

    def verifier(port): # Définition pour vérifier l'état des ports.
        try: # Essayer
            if Techno == "1": # Si le protocole est TCP.
                connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Création d'une connexion réseau en IPV4 TCP avec l'hôte.
                connexion_principale.settimeout(1) # Patienter pendant 1 seconde avant d'abandonner.
                connexion_principale.connect((Hote, port)) # Ouvrir une connexion avec l'hôte et le port concerné.
                print(" Le port:", port, "est ouvert") # Afficher le message avec le port et l'état ouvert.
                return (port, "==> ouvert") # Retourner le numéro de port avec son état (ouvert).

            elif Techno == "2": # Si le protocole est UDP.
                connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Création d'une connexion réseau en IPV4 UDP avec l'hôte.
                connexion_principale.settimeout(1) # Patienter pendant 1 seconde avant d'abandonner.
                connexion_principale.connect((Hote, port)) # Ouvrir une connexion avec l'hôte et le port concerné.
                print(" Le port:", port, "est ouvert") # Afficher le message avec le port et l'état ouvert.
                return (port, "==> ouvert") # Retourner le numéro de port avec son état (fermé).
            
        except Exception as e: # Exception sur n'importe quelle erreur.
            print(f"Le port {port} est fermé") # Afficher le message le port n° est fermé.
            return (port, "fermé") # Retourner le numéro de port avec son état (fermé).
        
        finally: # Enfin
                connexion_principale.close() # Fermer la connexion.

    start = time.time() # Enregistrement de l'heure actuelle dans la variable start.

    with ThreadPoolExecutor(max_workers=300) as executor: # Avec un gestionnaire de Thread de 300 Threads .
        futures = [executor.submit(verifier, port) for port in range(Debut, Fin + 1)] # Lancement d'un thread pour chaque port dans la definition vérifier(port) et stoké ma tâche dans la liste future.

        for future in as_completed(futures): # Pour chaque état dans la liste "futures".
            port, etat = future.result() # Insérer les valeurs dans les variables port et état.
            resultat_all_ports.append((port, etat)) # Ajouter dans la liste resultat_all_port l'état de chaque port analyser.

    resultat_all_ports.sort(key=lambda x: x[0]) # Trier la liste par numéro de port (ordre croissant).

    for port, etat in resultat_all_ports: # Pour chaque port et état dans la liste resultats_all_ports.
        f.write(f"{str(port).ljust(10)} : {etat}\n") # Ecrire dans le fichier le port, son état et sauter une ligne (ligne de 10 caractères).

    end = time.time() # Noter le temps dans la variable end.
    f.write("===> Le scan de la plage de ports a duré : " + str(round(end - start, 2)) + " secondes\n") # Ecrire dans le fichier la durée du scan. 
    print("Le scan de la plage de ports a duré :", round(end - start, 2), "secondes" "\n") # Afficher la durée du scan et sauter une ligne.
    logger_action(Hote, identifiant, f"Scan PLAGE DE PORTS {Debut}-{Fin} ({'TCP' if Techno == '1' else 'UDP'})", "non concerné", f"{round(end - start, 2)} sec") # Créer le log suivant.


def tous_les_ports(Hote, Techno):  # Fonction pour scanner tous les ports de 1 à 65535
        now = datetime.datetime.now().date()  # Récupère la date actuelle
        now1 = datetime.datetime.now().time()  # Récupère l'heure actuelle
        print("Date :", now.strftime('%A %d %B %y'))  # Affiche la date dans un format lisible
        print("Horaire :", now1.strftime('%H:%M:%S'))  # Affiche l'heure dans un format lisible

        filename = f"tous_les_ports_{now.strftime('%d-%m-%Y')}___{now1.strftime('%H-%M-%S')}.txt"  # Nom du fichier de résultat
        f = open(filename, 'w', encoding="utf-8")  # Ouvre le fichier en écriture avec encodage UTF-8

        f.write("La date :" + str(now) + "\n")  # Écrit la date dans le fichier
        f.write("L'heure :" + now1.strftime('%H:%M:%S') + "\n")  # Écrit l'heure dans le fichier
        f.write("Adresse IP de l'équipement : " + Hote + "\n")  # Écrit l'IP de l'équipement
        f.write('+-----------+---------------+\n')  # Ligne de séparation dans le tableau
        f.write('| Port      |   État        |\n')  # En-tête du tableau
        f.write('+-----------+---------------+\n')  # Ligne de séparation

        if Techno != "1" and Techno != "2":  # Si le protocole n'est ni TCP ni UDP
            print("Protocole non reconnu. Choisissez 1 pour TCP ou 2 pour UDP.")  # Affiche une erreur
            f.write("Protocole non reconnu.\n")  # Écrit l'erreur dans le fichier
            f.close()  # Ferme le fichier
            return  # Sort de la fonction

        f.write("==> Protocole utilisé : " + ("TCP\n" if Techno == "1" else "UDP\n"))  # Écrit le protocole utilisé

        resultat_all_ports = []  # Liste pour stocker les résultats
        start = time.time()  # Enregistre le temps de début du scan

        def verifier(port):  # Fonction pour tester un port
            try: # Essayer.
                if Techno == "1":  # Si protocole TCP
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crée une socket TCP
                    s.settimeout(0.5)  # Définit un délai d'attente de 0.5 seconde
                    s.connect((Hote, port))  # Tente une connexion
                    print(" Le port:", port, "est ouvert") # Afficher le message avec le port et l'état ouvert.
                    return (port, "ouvert")  # Retourne le port comme ouvert
                elif Techno == "2":  # Si protocole UDP
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Crée une socket UDP
                    s.settimeout(1)  # Définit un délai d'attente d'1 seconde
                    s.sendto(b'', (Hote, port))  # Envoie un paquet vide
                    try: # Essayer.
                        s.recvfrom(1024)  # Tente de recevoir une réponse
                        print(" Le port:", port, "est ouvert") # Afficher le message avec le port et l'état ouvert.
                        return (port, "ouvert")  # Si réponse, port ouvert
                    except socket.timeout:
                        return (port, "pas de réponse (filtré ou inconnu)")  # Pas de réponse = filtré ou inconnu
            except: # Exception.
                print(f"Le port {port} est fermé") # Afficher le message le port n° est fermé.
                return (port, "fermé")  # Si exception, port fermé
            finally: # Finalement.
                s.close()  # Ferme la socket proprement

        with ThreadPoolExecutor(max_workers=300) as executor:  # Lancement de 300 threads max
            futures = [executor.submit(verifier, port) for port in range(1, 65536)]  # Crée une tâche pour chaque port
            for ftr in as_completed(futures):  # Récupère les résultats au fur et à mesure
                resultat_all_ports.append(ftr.result())  # Ajoute le résultat à la liste

        resultat_all_ports.sort(key=lambda x: x[0])  # Trie les résultats par numéro de port

        for port, etat in resultat_all_ports:
            ligne = f"{str(port).ljust(10)} : {etat}"  # Création de la ligne
            f.write(ligne + "\n")  # On écrit la ligne dans le fichier

        end = time.time()  # Enregistre le temps de fin du scan
        duree = round(end - start, 2)  # Calcule la durée du scan
        print(f"Le scan de tous les ports a duré : {duree} secondes")  # Affiche la durée du scan
        f.write(f"===> Le scan de tous les ports a duré : {duree} secondes\n")  # Écrit la durée dans le fichier
   
        logger_action(Hote, identifiant, f"Scan TOUS LES PORTS 1 - 6553 ({'TCP' if Techno == '1' else 'UDP'})", "non concerné", f"{round(end - start, 2)} sec") # Créer le log suivant.

        f.close()  # Ferme le fichier des résultats