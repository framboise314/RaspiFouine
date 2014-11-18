#!/usr/bin/python
#
# Detecter des mouvements avec un capteur infrarouge
# Et declencher un relai
#
# Importation des librairies pythons
import RPi.GPIO as GPIO
import time
import urllib
import os

# Utiliser les BCM GPIO et pas les numeros des pins sur P1
GPIO.setmode(GPIO.BCM)
# Remet les ports a zero
GPIO.cleanup()

# Pin GPIO utilisee
GPIO_PIR = 4
GPIO_LED = 17
GPIO_PORTE = 18
# Constantes
TRUE = 1
FALSE = 0

print "Test du capteur de presence IR (CTRL-C pour quitter)"

# Configurer la pin 7 en entree les autres en sorties
GPIO.setup(GPIO_PIR,GPIO.IN)
GPIO.setup(GPIO_LED,GPIO.OUT)
GPIO.setup(GPIO_PORTE, GPIO.OUT)
GPIO.output(GPIO_LED,FALSE)
GPIO.output(GPIO_PORTE,FALSE)

# Initialisation des variables
Current_State  = 0
Previous_State = 0
compteur = 0

# Attendre n secondes avant de demarrer la detection
print "Temporisation de demarrage"
time.sleep(10)

try:
  print "Attente detection..."
  # Boucle jusqu a ce que la sortie du capteur passe a 1
  while GPIO.input(GPIO_PIR)==0:
    Current_State = 0
  print " Pret"

  # Tourne en boucle jusqu'a ce que l utilisateur quitte (par CTRL+C)
  while compteur < 3 :

    # Lire l'etat du capteur
    Current_State = GPIO.input(GPIO_PIR)

    if Current_State==1 and Previous_State==0:
      # Le detecteur a envoye un signal
      print " Mouvement detecte !"
      # Declencher camera
      # Recuperer la date et l heure
      nom=time.strftime('%d-%m-%y-%H-%M',time.localtime())
      print nom
      os.system("raspivid -o "+ nom +".mp4 -t 180000 &");
      print "Camera declenchee"
      # Attendre 1 seconde
      #time.sleep(1)
      # Coller relai eclairage
      GPIO.output(GPIO_LED,TRUE)
      # Attendre 1 seconde
      #time.sleep(1)
      # Coller relai porte
      GPIO.output(GPIO_PORTE,TRUE)
      # Attendre que le moteur tourne
      time.sleep(2)
      # Arreter le moteur
      GPIO.output(GPIO_PORTE,FALSE)
      # On attend  que la camera arrete de filmer
      time.sleep(180)
      # On decolle les relais
      GPIO.output(GPIO_LED,FALSE)
      # On enregistre l ancien etat
      Previous_State=1
    elif Current_State==0 and Previous_State==1:
      # On est de nouveau pret
      print " Pret "
      Previous_State=0
      compteur = compteur + 1


    # On attend 1 seconde
    time.sleep(1)

except KeyboardInterrupt:
  print " Quit"
  # Reinitialisation des parametres GPIOs
  GPIO.cleanup()


