import datetime

def logger_action(Hote, identifiant, action, source, destination):  # Enregistre une action dans le fichier de logs
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Date et heure courantes formatées
    log_message = (  # Construction du message de log
        f"[{date_time}] Utilisateur: {identifiant} | "  # Date et utilisateur
        f"IP: {Hote} | Action: {action} | "  # IP et action
        f"Source: {source} | Destination/Nouveau nom/Element/Duree: {destination}\n"  # Source et destination
    )
    with open("logs_actions.log", "a", encoding="utf-8") as log_file:  # Ouvre le fichier en mode ajout
        log_file.write(log_message)  # Écrit le message