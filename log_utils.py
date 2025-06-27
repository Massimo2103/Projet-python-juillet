import logging

def log_action(ip_client, user, action, source, destination):
    msg = f"Utilisateur: {user} | IP: {ip_client} | Action: {action} | Source: {source} | Destination/Nouveau nom: {destination}"
    logging.info(msg)
