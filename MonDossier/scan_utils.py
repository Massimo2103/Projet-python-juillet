import os
import socket
from logger import logger_action

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

def menu_scan(): # Définition du menu scan.

    while True: # Tant que c'est vrai.
        print("\n====== MENU SCAN ======")# afficher le menu principal
        print("1 : Scan IP (réseau)")# Afficher le choix.
        print("2 : Scan d'un port spécifique")# Afficher le choix.
        print("3 : Scan d'une plage de ports")# Afficher le choix.
        print("4 : Scan de tous les ports")# Afficher le choix.
        print("5 : Quitter le module de scan")# Afficher le choix.
        
        choix = input("Selectionner l'action que vous souhaitez faire : ") # Demander le choix.

        if choix == "1":  # Tester la connectivité (ping)
            hote = input("IP à tester (ping) : ").strip()
            ip_input(hote)


        elif choix == "2": # Scanner un port specifique.
            Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement. 
            ip_input(Hote) # Vérifier si l'équipement est valide et ping.
            Port = input("Quel port voulez-vous scanner ? : ") # Demander le port.
            Techno = input("Protocole TCP (1) ou UDP (2) ? : ") # TCP ou UDP.
            import operations
            operations.port_specifique(Hote, Port, Techno) # Appeler la définition.
        
        elif choix == "3":
            Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement.
            ip_input(Hote) # Vérifier si l'équipement est valide et ping.
            Debut = input("Port de début : ") # Demander le début de la plage.
            Fin = input("Port de fin : ") # Demander la fin de la plage.
            Techno = input("Protocole TCP (1) ou UDP (2) ? : ") # TCP ou UDP.
            import operations
            operations.plage_de_port(Hote, Debut, Fin, Techno) # Appeler la définition.

        elif choix == "4": # Scanner tous les ports.
            Hote = input("Quelle est l'adresse IPv4 de l'équipement concené ? : ") # Demander l'adresse IPV4 de l'équipement.
            ip_input(Hote) # Vérifier si l'équipement est valide et ping.
            Techno = input("Protocole TCP (1) ou UDP (2) ? : ") # TCP ou UDP.
            import operations
            operations.tous_les_ports(Hote, Techno) # Appeler la définition.

        elif choix == "5": # Quitter le module.
            print("Sortie du module de scan.") # Afficher le message.
            break # quitter la boucle.
        
        else: # Sinon.
            print("\nChoix invalide !") # message erreur de saisie.