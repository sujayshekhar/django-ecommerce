# On crée une tâche asynchrone pour envoyer une notification par email à nos utilisateurs
# lorsqu'ils passent une commande. La convention consiste à inclure des tâches asynchrones
# pour l'application dans un module de tâches dans le répertoire l'application.


from celery import task
from django.core.mail import send_mail
from .models import Commande


@task
def task_commande(id_commande):
    """Tâche pour envoyer une notification par e-mail
    lorsqu'une commande est créée avec succès"""
    
    commande = Commande.objects.get(id=id_commande)
    subject = 'Commande N°. {}'.format(commande.id)
    message = 'Bonjour {}, \n\nVotre commande a été validé avec success.\
                Lid de la commande est {}.'.format(commande.first_name, commande.id)
    
    envoi_email = send_mail(subject, message,
                            [commande.email],
                            'flavienhgs@gmail.com')
    
    return envoi_email
