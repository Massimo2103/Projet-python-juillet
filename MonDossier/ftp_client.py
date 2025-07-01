from ftplib import FTP
import logger

def acceder_ftp(identifiant, motdepasse): # Définition accéder au serveur FTP.

    try: # Essayer
        ftp = FTP()
        ftp.connect('127.0.0.1', 21)  # Remplacer par l'IP et le port de ton serveur FTP
        ftp.login(identifiant, motdepasse)   # Remplacer par tes identifiants FTP
        #print("Connexion FTP réussie.") # Afficher le message.
        
        # Activer le mode passif si nécessaire
        ftp.set_pasv(True)
        
        return ftp # retourner la valeur FTP.
    except Exception as e: # Exception.
        print(f" Erreur de connexion FTP : {e}") # Afficher le message d'erreur.
        return None # Retourner la valeur None.
