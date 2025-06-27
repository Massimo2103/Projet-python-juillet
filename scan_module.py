import socket # Import du module socket
import time # Import du module time
import datetime # Import du module datetime
import os # Import du module os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed # Import du module (éxecution simultanée de threads) avec récupération de résultats.
from log_utils import log_action  # Import de la fonction log unique
import session_utilisateur


def ip_valide(Hote): # Définition de l'adresse IP
    try: # Essaye
        socket.inet_aton(Hote) # Convertir l'adresse IP en binaire.
        print("L'adresse IP "+ str(Hote) +" est valide.") # Afficher le message si l'adresse IP est valide.
        return 0 # Retourner la valeur 0.
    except socket.error: # Interception de l'erreur lié au réseau.
        print("Erreur : L'adresse IP "+ str(Hote) +" n'est pas valide.") # Afficher le message si l'adresse IP n'est pas valide.
        return 1 # Retourner la valeur 1.
    
def ip_input(): # Définition demande et ping de l'adresse IPV4.

    Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
    Response = ip_valide(Hote) # Vérification de la validité de l'adresse IPV4.
    if Response == 0: # Si la défnition précendente renvoie la valeur 0.
        Response = os.system("ping -n 1 " + Hote ) # Ping avec 1 pacquet vers l'adresse IP.

        if Response == 0: # Si le ping réussi.
            return Hote # Retourner l'adresse IP de l'équipement.
        
        else: # Sinon
            print ("") # Afficher ligne vide.
            print("Adresse IP incorrect! ") # Afficher message d'erreur.
            return ip_input() # Demander l'adresse IPV4 valide.
        
    else: # Sinon
        print ("") # Afficher ligne vide.
        print("Adresse IP incorrect ou PING échoué ! ") # Afficher message d'erreur.
        return ip_input() # Demander l'adresse IPV4 valide.


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

            log_action(  # on écrit dans le même log général
                Hote,                                                      # IP scannée
                session_utilisateur.utilisateur_courant,                   # utilisateur connecté
                f"Scan PORT spécifique {Port} ({'TCP' if Techno == '1' else 'UDP'})",  # description de l’action
                "non concerné",                                            # champ source
                f"{round(end - start, 2)} sec"                             # champ destination = durée
            )



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

    log_action(  # on écrit dans le même log général
        Hote,                                                      # IP scannée
        session_utilisateur.utilisateur_courant,                   # utilisateur connecté
        f"Scan PLAGE PORTS {Debut}-{Fin} ({'TCP' if Techno == '1' else 'UDP'})",  # action
        "non concerné",                                            # source
        f"{round(end - start, 2)} sec"                             # durée du scan
    )






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
            try:
                if Techno == "1":  # Si protocole TCP
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Crée une socket TCP
                    s.settimeout(0.5)  # Définit un délai d'attente de 0.5 seconde
                    s.connect((Hote, port))  # Tente une connexion
                    return (port, "ouvert")  # Retourne le port comme ouvert
                elif Techno == "2":  # Si protocole UDP
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Crée une socket UDP
                    s.settimeout(1)  # Définit un délai d'attente d'1 seconde
                    s.sendto(b'', (Hote, port))  # Envoie un paquet vide
                    try:
                        s.recvfrom(1024)  # Tente de recevoir une réponse
                        return (port, "ouvert")  # Si réponse, port ouvert
                    except socket.timeout:
                        return (port, "pas de réponse (filtré ou inconnu)")  # Pas de réponse = filtré ou inconnu
            except:
                return (port, "fermé")  # Si exception, port fermé
            finally:
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

        log_action(  # on écrit dans le même log général
            Hote,                                                      # IP scannée
            session_utilisateur.utilisateur_courant,                   # utilisateur connecté
            f"Scan TOUS PORTS ({'TCP' if Techno == '1' else 'UDP'})", # action
            "non concerné",                                            # source
            f"{duree} sec"                                             # durée totale
        )




        f.close()  # Ferme le fichier des résultats


def interaction_port(Hote): # Définition intéraction 

    while True : # Tant que c'est vrai.

        print("1 : Scanner un port specifique.") # Afficher le choix.
        print("2 : Scanner une plage de port.") # Afficher le choix.
        print("3 : Scanner tous les ports simultanement.") # Afficher le choix.
        print("4 : Quitter le module.") # Afficher le choix.

        choix = input("Selectionner l'action que vous souhaitez faire : ") # Demander le choix.

        if choix == "1" : # Scanner un port specifique.
             Port = input("Quel est le port concerné ? : ") # Demander le nuémro de port
             Techno = input("Est-ce du TCP (choix 1) ou de l'UDP (choix 2) ? : ") # Demander TCP ou UDP

             port_specifique(Hote, Port, Techno) # Appel de la définition de l'analyse du port spécifique.

        elif choix == "2" : # Scanner une plage de port.
             Debut = input("Quel est le premier port de la plage ? : ") # Demander le nuémro de port de début.
             Fin = input("Quel est le dernier port de la plage ? : ") # Demander le nuémro de port de fin.
             Techno = input("Est-ce du TCP (choix 1) ou de l'UDP (choix 2) ? : ") # Demander TCP ou UDP

        if Techno == "1":  # Si TCP # Connexion avec retour clair
            plage_de_port(Hote, Debut, Fin, Techno)  # Scan TCP
        elif Techno == "2":  # Si UDP # Connexion sans retour fiable
            plage_de_port_udp(Hote, Debut, Fin)  # Scan UDP personnalisé

        elif choix == "3" : # Scanner tous les ports simultanement.
             Techno = input("Est-ce du TCP (choix 1) ou de l'UDP (choix 2) ? : ") # Demander TCP ou UDP

             tous_les_ports(Hote, Techno) # Appel de la définition de l'analyse de tous les ports.

        elif choix == "4" : # Quitter le module.
                break # Quitter la boucle .

def plage_de_port_udp(Hote, Debut, Fin):  # Fonction pour scanner une plage de ports en UDP
    now = datetime.datetime.now().date()  # Récupération de la date du jour
    now1 = datetime.datetime.now().time()  # Récupération de l'heure actuelle
    print("Date :", now.strftime('%A %d %B %y'))  # Affichage lisible de la date
    print("Horaire :", now1.strftime('%H:%M:%S'))  # Affichage lisible de l'heure

    filename = f"plage_de_ports_UDP_{now.strftime('%d-%m-%Y')}___{now1.strftime('%H-%M-%S')}.txt"  # Création du nom de fichier de résultats
    f = open(filename, 'w', encoding="utf-8")  # Ouverture du fichier pour écrire les résultats

    f.write("La date : " + str(now) + "\n")  # Écriture de la date dans le fichier
    f.write("L'heure : " + now1.strftime('%H:%M:%S') + "\n")  # Écriture de l'heure dans le fichier
    f.write("Adresse IP de l'équipement : " + Hote + "\n")  # Écriture de l'adresse IP cible
    f.write('+-----------+------------------------------+\n')  # Ligne de séparation du tableau
    f.write('| Port      |   État                       |\n')  # En-tête du tableau
    f.write('+-----------+------------------------------+\n')  # Ligne de séparation

    resultat_all_ports = []  # Liste pour stocker les résultats des ports

    def verifier(port):  # Fonction interne pour tester un port UDP
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Création d'une socket UDP
            sock.settimeout(1)  # Timeout de 1 seconde
            message = b"Test"  # Message arbitraire à envoyer
            sock.sendto(message, (Hote, port))  # Envoi du message sur l'IP et le port
            sock.recvfrom(1024)  # Tentative de réception de réponse
            return (port, "ouvert")  # Si on reçoit quelque chose, le port est considéré comme ouvert
        except socket.timeout:
            return (port, "pas de réponse (ouvert ou filtré)")  # Aucun retour, peut être ouvert mais silencieux
        except Exception:
            return (port, "fermé")  # Autre erreur, le port est sûrement fermé
        finally:
            sock.close()  # Fermeture de la socket

    start = time.time()  # Démarrage du chronomètre

    with ThreadPoolExecutor(max_workers=300) as executor:  # Utilisation de 300 threads en parallèle
        futures = [executor.submit(verifier, port) for port in range(int(Debut), int(Fin) + 1)]  # Lancement des tests de ports
        for future in as_completed(futures):  # Récupération des résultats au fur et à mesure
            port, etat = future.result()  # Extraction du port et de son état
            resultat_all_ports.append((port, etat))  # Ajout à la liste des résultats
            print(f"Port {port}: {etat}")  # Affichage du résultat dans le terminal
            f.write(f"{str(port).ljust(10)} : {etat}\n")  # Écriture dans le fichier

    end = time.time()  # Fin du chronomètre
    duree = round(end - start, 2)  # Calcul de la durée du scan
    f.write(f"\nDurée du scan UDP : {duree} secondes\n")  # Écriture de la durée dans le fichier
    print("Le scan UDP a duré :", duree, "secondes\n")  # Affichage de la durée

    log_action(  # on écrit dans le même log général
        Hote,                                                      # IP scannée
        session_utilisateur.utilisateur_courant,                   # utilisateur connecté
        f"Scan PLAGE PORTS {Debut}-{Fin} (UDP)",                  # action
        "non concerné",                                            # source
        f"{duree} sec"                                             # durée du scan
    )




    f.close()  # Fermeture du fichier

def scan_ip():
    ip_base = input("Entrez le début de l'adresse réseau (ex: 192.168.1) : ").strip()  # Récupère le préfixe réseau
    plage = input("Entrez la plage à scanner (exemple : 1-10) : ").strip()  # Récupère la plage de hosts à scanner

    debut, fin = map(int, plage.split("-"))  # Sépare la plage en début et fin, convertit en int
    resultats_ping = []  # Initialise la liste des résultats de ping

    print(f"\nDébut du scan de {ip_base}.{debut} à {ip_base}.{fin} ...")  # Affiche la plage scannée

    def ping(ip):
        response = os.system(f"ping -n 1 {ip} >nul")  # Exécute ping et ignore la sortie
        resultats_ping.append((ip, response == 0))  # Ajoute le résultat (True si réponse) à la liste

    threads = []  # Liste pour stocker les threads
    for i in range(debut, fin + 1):
        ip = f"{ip_base}.{i}"  # Construit l'adresse IP
        t = threading.Thread(target=ping, args=(ip,))  # Crée un thread pour le ping
        t.start()  # Démarre le thread
        threads.append(t)  # Ajoute le thread à la liste

    for t in threads:
        t.join()  # Attend la fin de chaque thread

    resultats_ping.sort(key=lambda x: list(map(int, x[0].split("."))))  # Trie par adresse IP

    print("\nRésultat du scan réseau :")  # Affiche l'en-tête des résultats
    for ip, actif in resultats_ping:
        etat = "actif" if actif else "injoignable"  # Établit le statut
        print(f"{ip} : {etat}")  # Affiche chaque résultat

    log_action(  # on écrit dans le même log général
        "LOCAL",                                                   # IP source (scan réseau local)
        session_utilisateur.utilisateur_courant,                   # utilisateur connecté
        f"Scan IP de la plage {ip_base}.{debut}-{fin}",           # action
        "non concerné",                                            # source
        f"{sum(1 for _, actif in resultats_ping if actif)} hôtes actifs"  # résultat
    )


def menu_scan():
    while True:
        print("\n====== MENU SCAN ======")                                       # affiche le menu principal
        print("1 : Scan IP (réseau)")                                         # option 1
        print("2 : Scan d'un port spécifique")                                # option 2
        print("3 : Scan d'une plage de ports")                                # option 3
        print("4 : Scan de tous les ports")                                   # option 4
        print("5 : Quitter le module de scan")                                # option 5
        choix = input("Votre choix : ")                                       # lit le choix utilisateur

        if choix == "1":
            scan_ip()                                                         # lance le scan IP
            log_action(                                                       # écrit dans le même log général
                action="Scan IP (réseau)",                                    # description de l’action
                utilisateur=session_utilisateur.utilisateur_courant,          # utilisateur connecté
                role=session_utilisateur.role_utilisateur,                   # rôle de l’utilisateur
                ip="LOCAL",                                                  # IP source
                source="non concerné",                                       # champ source
                destination="non concerné"                                   # champ destination
            )  # log scan réseau

        elif choix == "2":
            Hote = ip_input()                                                 # demande l’adresse IP cible
            Port = input("Quel port voulez-vous scanner ? : ")                # lit le port
            Techno = input("Protocole TCP (1) ou UDP (2) ? : ")               # lit le protocole
            port_specifique(Hote, Port, Techno)                               # lance le scan de port spécifique
            log_action(                                                       # écrit dans le même log général
                action=f"Scan menu : port spécifique {Port} sur {Hote} en protocole {'TCP' if Techno == '1' else 'UDP'}",  # description
                utilisateur=session_utilisateur.utilisateur_courant,          # utilisateur connecté
                role=session_utilisateur.role_utilisateur,                   # rôle de l’utilisateur
                ip=Hote,                                                     # IP cible
                source="non concerné",                                       # champ source
                destination="non concerné"                                   # champ destination
            )  # log scan port

        elif choix == "3":
            Hote = ip_input()                                                 # demande l’adresse IP cible
            Debut = input("Port de début : ")                                 # lit port de début
            Fin = input("Port de fin : ")                                     # lit port de fin
            Techno = input("Protocole TCP (1) ou UDP (2) ? : ")               # lit le protocole
            if Techno == "1":
                plage_de_port(Hote, Debut, Fin, Techno)                       # lance le scan TCP de la plage
            else:
                plage_de_port_udp(Hote, Debut, Fin)                           # lance le scan UDP de la plage
            log_action(                                                       # écrit dans le même log général
                action=f"Scan menu : plage {Debut}-{Fin} sur {Hote} en protocole {'TCP' if Techno == '1' else 'UDP'}",  # description
                utilisateur=session_utilisateur.utilisateur_courant,          # utilisateur connecté
                role=session_utilisateur.role_utilisateur,                   # rôle de l’utilisateur
                ip=Hote,                                                     # IP cible
                source="non concerné",                                       # champ source
                destination="non concerné"                                   # champ destination
            )  # log scan plage

        elif choix == "4":
            Hote = ip_input()                                                 # demande l’adresse IP cible
            Techno = input("Protocole TCP (1) ou UDP (2) ? : ")               # lit le protocole
            tous_les_ports(Hote, Techno)                                      # lance le scan de tous les ports
            log_action(                                                       # écrit dans le même log général
                action=f"Scan menu : tous les ports sur {Hote} en protocole {'TCP' if Techno == '1' else 'UDP'}",  # description
                utilisateur=session_utilisateur.utilisateur_courant,          # utilisateur connecté
                role=session_utilisateur.role_utilisateur,                   # rôle de l’utilisateur
                ip=Hote,                                                     # IP cible
                source="non concerné",                                       # champ source
                destination="non concerné"                                   # champ destination
            )  # log scan tous ports

        elif choix == "5":
            print("Sortie du module de scan.")                                # message de sortie
            log_action(                                                       # écrit dans le même log général
                action="Sortie du module de scan",                           # description de l’action
                utilisateur=session_utilisateur.utilisateur_courant,          # utilisateur connecté
                role=session_utilisateur.role_utilisateur,                   # rôle de l’utilisateur
                ip="LOCAL",                                                  # IP source
                source="non concerné",                                       # champ source
                destination="non concerné"                                   # champ destination
            )  # log sortie
            break                                                            # quitte la boucle

        else:
            print("Choix invalide.")                                         # message erreur de saisie
