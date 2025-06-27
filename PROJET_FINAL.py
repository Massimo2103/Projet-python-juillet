from ftplib import FTP # Module de connection au FTP.
from unittest.mock import patch
import os # Module pour intéragir avec le système de fichier. 
import socket # Module pour intérgir avec le client.
import shutil # Module copier, déplacer, supprimer des fichiers/dossiers.
import time # Module de dates.
import datetime # Module d'horodatage.
import threading # Module de threads.
import csv  # Pour lire le fichier CSV des utilisateurs
from concurrent.futures import ThreadPoolExecutor, as_completed
from log_utils import log_action  # Seul à garder
import session_utilisateur
import logging

import scan_module


# Configure le module logging pour écrire tous les messages dans un seul fichier de log
logging.basicConfig(
    filename="logs_actions.log",         # Nom du fichier de sortie pour les logs
    level=logging.INFO,                  # Niveau minimal de log à capturer (INFO, WARNING, ERROR…)
    format='[%(asctime)s] %(message)s',  # Format de chaque ligne de log : horodatage + message
    datefmt='%Y-%m-%d %H:%M:%S'          # Format de l’horodatage (YYYY-MM-DD HH:MM:SS)
)

def authentification():
    print("===== CONNEXION UTILISATEUR =====")

    try:
        with open("users.csv", mode='r', encoding='utf-8-sig') as f:
            lecteur = csv.DictReader(f, delimiter=',')
            utilisateurs = list(lecteur)

        tentatives = 0
        while tentatives < 3:
            login = input("Login : ").strip()
            password = input("Mot de passe : ").strip()

            utilisateur_trouve = next(
                (u for u in utilisateurs if u['login'] == login and u['password'] == password),
                None
            )

            if utilisateur_trouve:
                    session_utilisateur.utilisateur_courant = login
                    session_utilisateur.role_utilisateur    = utilisateur_trouve['role']
                    print(f"Connexion réussie. Rôle : {session_utilisateur.role_utilisateur.upper()}")
                    return
            else:
                tentatives += 1
                print(f"Identifiants incorrects. Tentative {tentatives}/3\n")

        print("Trop de tentatives échouées. L'accès est bloqué.")
        exit()

    except FileNotFoundError:
        print("Fichier users.csv introuvable.")
        exit()


def ip_valide(Hote): # Définition de l'adresse IP
    try: # Essaye
        socket.inet_aton(Hote) # Convertir l'adresse IP en binaire.
        print("L'adresse IP "+ str(Hote) +" est valide.") # Afficher le message si l'adresse IP est valide.
        return 0 # Retourner la valeur 0.
    except socket.error: # Interception de l'erreur lié au réseau.
        print("Erreur : L'adresse IP "+ str(Hote) +" n'est pas valide.") # Afficher le message si l'adresse IP n'est pas valide.
        return 1 # Retourner la valeur 1.
    
def ip_input(Hote): # Définition demande et ping de l'adresse IPV4.

    #Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
    Response = ip_valide(Hote) # Vérification de la validité de l'adresse IPV4.
    if Response == 0: # Si la défnition précendente renvoie la valeur 0.
        Response = os.system("ping -n 1 " + Hote ) # Ping avec 1 pacquet vers l'adresse IP.

        if Response == 0: # Si le ping réussi.
            return Hote # Retourner l'adresse IP de l'équipement.
        
        else: # Sinon
            print ("") # Afficher ligne vide.
            print("Adresse IP incorrect! ") # Afficher message d'erreur.
            return ip_input(Hote) # Demander l'adresse IPV4 valide.
        
    else: # Sinon
        print ("") # Afficher ligne vide.
        print("Adresse IP incorrect ou PING échoué ! ") # Afficher message d'erreur.
        return ip_input(Hote) # Demander l'adresse IPV4 valide.
    

def ville_autorisee_par_utilisateur():  # Retourne la ville que l'utilisateur peut gérer
    uc = session_utilisateur.utilisateur_courant
    if uc == "admin_marseille":            # <- ajouté le `:` ici
        return "MARSEILLE"                # Accès à Marseille uniquement
    elif uc == "admin_rennes":             # on utilise toujours `uc`
        return "RENNES"                    # Accès à Rennes uniquement
    elif uc == "admin_grenoble":
        return "GRENOBLE"                  # Accès à Grenoble uniquement
    elif uc == "admin_supreme_paris":
        return "TOUS"                      # Accès à toutes les villes
    else:
        return None                        # Pas de ville autorisée


def recuperer_identifiants_ftp():  # Renvoie les identifiants FTP selon l'utilisateur courant
    uc = session_utilisateur.utilisateur_courant
    if uc == "admin_supreme_paris":
        return ("admin_supreme_paris", "paris123")
    elif uc == "admin_marseille":
        return ("admin_marseille", "marseille123")
    elif uc == "admin_rennes":
        return ("admin_rennes", "rennes123")
    elif uc == "admin_grenoble":
        return ("admin_grenoble", "grenoble123")
    else:
        print(f"[DEBUG] utilisateur non reconnu = {uc}")
        return (None, None)


def logger_action(ip_client, user, action, source, destination):  # Enregistre une action dans le fichier de logs
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Date et heure courantes formatées
    log_message = (  # Construction du message de log
        f"[{date_time}] Utilisateur: {user} | "  # Date et utilisateur
        f"IP: {ip_client} | Action: {action} | "  # IP et action
        f"Source: {source} | Destination/Nouveau nom: {destination}\n"  # Source et destination
    )
    with open("logs_actions.log", "a", encoding="utf-8") as log_file:  # Ouvre le fichier en mode ajout
        log_file.write(log_message)  # Écrit le message

def acceder_ftp(verbose=False):  # Tente de se connecter au serveur FTP
    try:  # Bloc principal
        user, mdp = recuperer_identifiants_ftp()  # Récupère login et mot de passe
        if not user or not mdp:  # Si identifiants non trouvés
            print("Impossible de récupérer les identifiants FTP.")  # Message d'erreur
            return None  # Retourne None

        ftp = FTP()  # Crée une instance FTP
        ftp.connect('127.0.0.1', 21)  # Connexion au serveur local sur le port 21
        ftp.login(user, mdp)  # Authentification
        ftp.set_pasv(True)  # Mode passif

        if verbose:  # Si mode verbeux activé
            print(f"Connexion FTP réussie avec le compte : {user}")  # Confirme la connexion

        return ftp  # Retourne l'objet FTP établi
    except Exception as e:  # En cas d'erreur quelconque
        print(f"Erreur de connexion FTP : {e}")  # Affiche l'erreur
        return None  # Retourne None en échec



def copier_fichier_dossier(): # Définition pour copier un fichier ou dossier.

    print("\nCopie FICHIER/DOSSIER ") # Afficher le message.
     
    while True : # Tant que c'est vrai
        try: # Essayer
                choix_server_hote = input("sur ftp (1) ou client (2) ? ") # Demande de connexion au FTP ou au client.
                if choix_server_hote == "1" : # Si le choix est 1.
                    acceder_ftp() # Lancer la définition acceder au FTP.
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
                        logger_action("Serveur FTP", session_utilisateur.utilisateur_courant, "COPIE FICHIER", source, destination) # Créer le log suivant.
                    elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, session_utilisateur.utilisateur_courant, "COPIE FICHIER", source, destination) # Créer le log suivant.
                    print(f"Fichier copié avec succès vers : {destination} !") # Afficher le message.
                elif choix == "2": # Si le choix est 2.
                    shutil.copytree(source, destination) # Copie le dossier source en conservant la date...
                    if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", session_utilisateur.utilisateur_courant, "COPIE DOSSIER", source, destination) # Créer le log suivant.
                    elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, session_utilisateur.utilisateur_courant, "COPIE FICHIER", source, destination) # Créer le log suivant.
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
                    acceder_ftp() # Lancer la définition acceder au FTP.
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
                
                destination = input("Entrez le chemin COMPLET du fichier ou du dossier à renommer (ex : C/Massimo/Juillet/Paris) : ").strip() # Demander le chemin avec le nouveau nom.
               
                dossier_parent = os.path.dirname(destination) # Extraire le chemin dossier.
                if not os.path.isdir(dossier_parent): # Si le dossier n'existe pas.
                    raise ValueError("Le chemin est incorrect ! ") # Arrêt de l'éxecution.
                              
                os.rename(source, destination) # Renommer le fichier.

                if choix == "1":# Si le choix est 1.
                    if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", session_utilisateur.utilisateur_courant, "RENOMMER FICHIER", source, destination) # Créer le log suivant.
                    elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, session_utilisateur.utilisateur_courant, "RENOMMER FICHIER", source, destination) # Créer le log suivant.
                    print(f"Fichier renommé avec succès : {source} ==> {destination}") # Afficher le message.
                elif choix == "2": # Si le choix est 2.
                    if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", session_utilisateur.utilisateur_courant, "RENOMMER DOSSIER", source, destination) # Créer le log suivant.
                    elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, session_utilisateur.utilisateur_courant, "RENOMMER DOSSIER", source, destination) # Créer le log suivant.
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
                acceder_ftp() # Lancer la définition acceder au FTP.
            elif choix_server_hote == "2" : # Si le choix est 2.
                Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
                ip_input(Hote) # Lancer la définition ip_input.
            if choix_server_hote not in ("1", "2"): # Si le choix n'est ni 1 et 2.
                raise ValueError("La valeur saisie n'est pas 1 ou 2 ! ") # Arrêt de l'éxecution.
            choix = input("Souhaitez-vous créer un fichier (1) ou un dossier (2) ? : ") # Demander si on créer un fichier ou un dossier.
            if choix not in ("1", "2"): # Si le choix n'est ni 1 ni 2.
                raise ValueError("La valeur saisie n'est pas 1 ou 2 !") # Arrêt de l'éxecution.
            source = input("Entrez le chemin COMPLET où créer le fichier ou dossier (ex : C/Massimo/Juillet/Paris/test.txt ou /REMOTE_PROJET/MARSEILLE/Projet.txt) : ").strip() # Demander le chemin.
            if not source: # Si ce n'est pas source.
                 raise ValueError("La localisation n'a pas été renseignée !")
            dossier_parent = os.path.dirname(source) # Extraire le chemin dossier.
            if not os.path.isdir(dossier_parent): # Si le dossier n'existe pas.
                raise ValueError("Le chemin est incorrect ! ") # Arrêt de l'éxecution.

            if choix == "1": # Si le choix est 1.
                with open(source, 'x') as f:  # Ouvrir le fichier uniquement s'il n'existe pas.
                    pass # Passer (ne rien écrire dans le fichier).
                if choix_server_hote == "1": # Si le choix est 1.
                    logger_action("Serveur FTP", session_utilisateur.utilisateur_courant, "CRÉER FICHIER", source, "non concerné") # Créer le log suivant.
                elif choix_server_hote == "2": # Si le choix est 2.
                    logger_action(Hote, session_utilisateur.utilisateur_courant, "CRÉER FICHIER", source, "non concerné") # Créer le log suivant.
                print(f"Fichier créé avec succès : {source}") # Afficher le message.

            elif choix == "2": # Si le choix est 2.
                os.makedirs(source, exist_ok=False)  # Créer le dossier uniquement s'il n'existe pas.
                if choix_server_hote == "1": # Si le choix est 1.
                    logger_action("Serveur FTP", session_utilisateur.utilisateur_courant, "CRÉER DOSSIER", source, "non concerné") # Créer le log suivant.
                elif choix_server_hote == "2": # Si le choix est 2.
                    logger_action(Hote, session_utilisateur.utilisateur_courant, "CRÉER DOSSIER", source, "non concerné") # Créer le log suivant.
                print(f"Fichier créé avec succès : {source}") # Afficher le message.
                print(f"Dossier créé avec succès : {source}") # Afficher le message.

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
                acceder_ftp() # Lancer la définition acceder au FTP.
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
                        logger_action("Serveur FTP", session_utilisateur.utilisateur_courant, "DÉPLACER FICHIER", source, destination) # Créer le log suivant.
                elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, session_utilisateur.utilisateur_courant, "DÉPLACER FICHIER", source, destination) # Créer le log suivant.
                print(f"Fichier déplacé avec succès : {source} ==> {destination}") # Afficher le message.
            elif choix == "2": # Si le choix est 2.
                if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", session_utilisateur.utilisateur_courant, "DÉPLACER DOSSIER", source, destination) # Créer le log suivant.
                elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, session_utilisateur.utilisateur_courant, "DÉPLACER DOSSIER", source, destination) # Créer le log suivant.
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
                acceder_ftp() # Lancer la définition acceder au FTP.
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
                        logger_action("Serveur FTP", session_utilisateur.utilisateur_courant, "SUPPRESSION FICHIER", source, "non concerné") # Créer le log suivant.
                    elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, session_utilisateur.utilisateur_courant, "SUPPRESSION FICHIER", source, "non concerné") # Créer le log suivant.
                    print(f"Fichier supprimé avec succès : {source}") # Afficher le message.

                elif choix == "2": # Si c'est un dossier.
                    if not os.path.isdir(source): # Si l'élément n'est pas un dossier.
                        raise ValueError("Le chemin renseigné ne renvoie pas un dossier !") # Arrêt de l'éxecution.
                    shutil.rmtree(source) # Supprimé le dossier.
                    if choix_server_hote == "1": # Si le choix est 1.
                        logger_action("Serveur FTP", session_utilisateur.utilisateur_courant, "SUPPRESSION DOSSIER", source, "non concerné") # Créer le log suivant.
                    elif choix_server_hote == "2": # Si le choix est 2.
                        logger_action(Hote, session_utilisateur.utilisateur_courant, "SUPPRESSION DOSSIER", source, "non concerné") # Créer le log suivant.
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


def lister_arborescence(chemin, prefixe=""):  # Parcourt récursivement et affiche l’arborescence d’un dossier
    try:  # Tente d’exécuter le bloc de code
        for element in os.listdir(chemin):  # Liste les éléments (fichiers et dossiers) du chemin donné
            chemin_complet = os.path.join(chemin, element)  # Construit le chemin complet de l’élément
            if os.path.isdir(chemin_complet):  # Vérifie si le chemin complet est un dossier
                print(f"{prefixe}[D] {element}/")  # Affiche le nom du dossier avec un indicateur [D]
                lister_arborescence(chemin_complet, prefixe + "    ")  # Appelle récursivement pour le sous-dossier
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
                acceder_ftp() # Appeler la défintion.
            elif choix_server_hote == "2" : # Si le choix est client.
                Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
                ip_input(Hote) # Appeler la définition avec la valeur HOTE.
            chemin = input("Saisissez le chemin (ex : C:/Massimo/Paris) : ").strip() # Demander le chemin en supprimant les espaces.
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
        except ValueError as erreur: # En cas de Value Error.
                print(f"Une erreur s'est produite : {erreur}") # Afficher le message d'erreur.
        break # Quitter.


def lister_dossier_fichier(): # Définition lister dossier fichier.
    print("\nLister les DOSSIERS, les SOUS-DOSSIERS et les FICHIERS") # Afficher le message de la définition.
    
    while True: # Tant que c'est vrai.
        try: # Essayer.
            choix_server_hote = input("sur ftp (1) ou client (2) ? ") # Demande de connexion au FTP ou au client.
            if choix_server_hote == "1" : # Si le choix est 1.
                acceder_ftp() # Lancer la définition acceder au FTP.
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


def sauvegarder_fichier_dossier(): # Définition sauvergader les fochiers et dossiers.
    print("\nSauvegarder FICHIER/DOSSIER du client vers le serveur FTP") # Afficher le message de la définition.

    ftp = acceder_ftp() # lancer la définition de connexion au FTP.
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
            logger_action("Serveur FTP", session_utilisateur.utilisateur_courant, "SAUVEGARDE FICHIER", source, destination) # Créer le log suivant.
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
                
            logger_action(Hote, session_utilisateur.utilisateur_courant, "SAUVEGARDE DOSSIER", source, destination) # Créer le log suivant.
            print(f"Tous les fichiers de '{source}' ont été sauvegardés dans '{destination}'.") # Affichage du message.

    except Exception as e: # En cas d'erreur.
        print(f" Erreur : {e}") # Afficher le message d'erreur.


def restaurer_fichier_dossier(): # Définition restauration fichier ou dossier.
    print("\nRestaurer FICHIER/DOSSIER du serveur FTP vers le CLIENT") # Afficher le message de la définition.

    ftp = acceder_ftp() # Lancer la connexion FTP.
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
                    
            logger_action(Hote, session_utilisateur.utilisateur_courant, "RESTAURATION FICHIER", source, destination) # Créer le log suivant.
            print(f"Fichier restauré avec succès vers : {destination}") # Afficher le message de confirmation avec la destination


        elif choix == "2" : # Si le choix est 2.
            ftp.cwd(source)  # On s'assure que c'est un dossier FTP
            fichiers = ftp.nlst()  # Liste les fichiers et sous-dossiers

            for fichier in fichiers: # Pour chaque fichier de la liste fichiers.
                try: # Essayer
                    ftp.size(fichier)  # Si pas d’erreur rencontrée, c’est un fichier.
                    destination = os.path.join(destination, os.path.basename(fichier)) # Défini la destiantion avec me nom du fichier + la destination locale.
                    print(f"Téléchargement de '{fichier}' vers '{destination}' ...") # Affichage du message.

                    with open(destination, "wb") as f: # Ouvrir le fichier de la variable destination en write binary.
                        ftp.retrbinary(f"RETR {fichier}", f.write) # Télcharger le fichier en mode binaire et son contenu.
                    print(f" Téléchargé : {fichier}") # Affichage du message.
                except: # Exception.
                    print(f" Ignoré (probablement un dossier) : {fichier}") # Affichage du message.
                        
            logger_action(Hote, session_utilisateur.utilisateur_courant, "RESTAURATION DOSSIER", source, destination) # Créer le log suivant.
            print(f"\\Tous les fichiers du dossier '{source}' ont été restaurés dans '{destination}'.") # Afficher le message.

    except Exception as e: # Exception.
        print(f" Erreur : {e}") # Afficher l'erreur.


def sauvegarde_automatique(): # Définition sauvegarde automatique.

    date_execution = "2025-06-25 19:12:00" # Définition de la date et l'heure.
    hote = "192.168.1.53" # Adresse IP du client.
    source = r"C:/Users/Massi/Music/A IMPRIMER/test.txt" # Chemin source depuis le client.
    destination = "/massimo2/"

    # Attente jusqu'à l'heure d'exécution
    date_exec = datetime.datetime.strptime(date_execution, "%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()
    delai = (date_exec - now).total_seconds() # Le delai est égal la date d'execution - date actuelle.
    if delai > 0: # Si le délai est supérieur à 0.
        time.sleep(delai) # Attendre le créneau.

    ftp = acceder_ftp() # Lancer la défintion connexion au ftp.
    if not ftp:
        return # Retourner FTP.
    
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

            with open(chemin_local, "rb") as f: # Ouvrir le fichier en retry binary.
                ftp.storbinary(f"STOR {nouveau_nom}", f) # Sauvegarde du fichier dans le FTP.
            logger_action(hote, session_utilisateur.utilisateur_courant, "SAUVEGARDE FICHIER AUTOMATIQUE", chemin_local, ftp.pwd()) # Créer le log suivant.
            
            if os.path.isfile(source): # Si source est un fichier.
                sauvegarder_fichier_versionne(source) # Appelle de la fonction pour sauvegarder la version.
            elif os.path.isdir(source): # Si c'est un dossier.
                fichiers = os.listdir(source) #Lister les fichiers et dossiers qui sont dans source.
                for fichier in fichiers: # Pour chaque fichier dans fichiers.
                    chemin_fichier = os.path.join(source, fichier) # Former le chemin complet vers le fichier/dossier.
                    if os.path.isfile(chemin_fichier): # Si c'est un fichier.
                        sauvegarder_fichier_versionne(chemin_fichier) # Apelle de la fonction pour sauvegarder la version.
                    else: # Sinon.
                        continue # Continuer.

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
        print("11 : MODULE SCAN (réseau et ports).")
        print("12 : QUITTER.") # Afficher le choix.

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
            logger_action("LOCAL", session_utilisateur.utilisateur_courant, "NAVIGATION ARBORESCENCE", "non concerné", "non concerné")  # Log de la navigation
        elif choix == "7":  # Lister arborescence d'un chemin donné
            chemin = input("Entrez le chemin à lister : ").strip()  # Demande le chemin à lister
            prefixe = input("Entrez un préfixe (facultatif) : ")  # Demande un préfixe d'affichage
            lister_arborescence(chemin, prefixe)  # Appelle la fonction de listage
            logger_action("LOCAL", session_utilisateur.utilisateur_courant, "LISTE ARBORESCENCE", chemin, "non concerné")  # Log du listage
        elif choix == "8":  # Lister dossiers, sous-dossiers et fichiers
            lister_dossier_fichier()  # Appelle la fonction de listing complet
            logger_action("LOCAL", session_utilisateur.utilisateur_courant, "LISTE DOSSIER/FICHIERS", "non concerné", "non concerné")  # Log du listing
        elif choix == "9":  # Sauvegarder un fichier ou dossier vers le FTP
            sauvegarder_fichier_dossier()  # Appelle la fonction de sauvegarde FTP
        elif choix == "10":  # Restaurer un fichier ou dossier depuis le FTP
            restaurer_fichier_dossier()  # Appelle la fonction de restauration FTP
        elif choix == "11":  # Lancer le module de scan réseau et ports
            scan_module.menu_scan()  # Appelle le menu du module scan
            logger_action("LOCAL", session_utilisateur.utilisateur_courant, "SCAN MODULE", "non concerné", "non concerné")  # Log du lancement du scan
        elif choix == "12":  # Quitter le programme
            break  # Sort de la boucle de gestion
        else:  # Cas d'un choix invalide
            print("Le choix est invalide !")  # Informe l'utilisateur

if __name__ == "__main__":  # Point d'entrée du script
    authentification()  # Lance la procédure d'authentification
    threading.Thread(target=sauvegarde_automatique, daemon=True).start()  # Démarre la sauvegarde automatique en arrière-plan
    gestion_fichier()  # Démarre la boucle principale de gestion des fichiers