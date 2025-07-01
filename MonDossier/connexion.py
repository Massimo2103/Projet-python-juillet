import csv
import getpass
import time

def charger_utilisateurs(fichiercsvusers): # Définition chargements des users du csv.
    utilisateurs = [] # Créer une liste utilisateurs.
    with open(fichiercsvusers, mode='r', newline='', encoding='utf-8') as file: # Ouvrir le csv en mode lecture.
        reader = csv.reader(file)
        next(reader)  # Ignore l'en-tête
        for row in reader: # Pour chaque éléments.
            if len(row) != 2:
                continue
            Id, Mdp = row
            utilisateurs.append({'identifiant': Id.strip().lower(), 'motdepasse': Mdp.strip()})
    return utilisateurs

def connexion(fichiercsvusers):
    utilisateurs = charger_utilisateurs(fichiercsvusers)
    tentatives_max = 3
    tentatives = 0

    while True: # Tant que c'est vrai.
        identifiant = input("Identifiant : ").strip().lower() # Demander l'identifiant.
        motdepasse = getpass.getpass("Mot de passe : ").strip() # De amnder le mdp.

        for user in utilisateurs: # Pour chaque user dans utilisateurs.
            if user['identifiant'] == identifiant and user['motdepasse'] == motdepasse:
                print("Connexion réussie.") # Afficher le message.
                return identifiant, motdepasse # Retourner les valeurs.

        tentatives += 1
        if tentatives >= tentatives_max:
            print("Trop de tentatives échouées. Blocage pendant 10 secondes...")
            time.sleep(10) # Attendre 10 secondes.
            tentatives = 0
        else: # Sinon
            print(f"Connexion échouée. Tentatives restantes : {tentatives_max - tentatives}") # Afficher message.