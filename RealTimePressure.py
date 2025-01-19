#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 15:45:23 2024

@author: leopotvin
"""
import asyncio
from bleak import BleakScanner
from bleak import BleakClient
from qasync import QEventLoop
import struct
import pandas as pand
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
import cv2
 



#UUIDs
address = "46270FD2-1135-FC98-4997-422977E13E19" 
MESURES_UUID = "97918cb5-8f6d-4247-9296-6cead3928adf"

#Plotting option (v:voltage, m:mass, f:force, p:pressure)
selection = "p" 

#Surface of a sensor(m^2)
surface = 0.0002585398163
if selection == "v":
  VALEURMAX = 3160
  VALEURMIN = 142
elif selection == "m":
  VALEURMAX = 10000
  VALEURMIN = 0
elif selection == "f":
  VALEURMAX = 10 * 9.80665
  VALEURMIN = 0
elif selection == "p":
  VALEURMAX = ((10 * 9.80665)/surface)/1000
  VALEURMIN = 0

def masse_interpolee (z):
  resultat = -17.3429*z**9 + 221.7042*z**8 + -1077.4485*z**7 + 2402.209*z**6 + -2164.828*z**5 + 42.0744*z**4 +  224.1687*z**3 + 1440.927*z**2 + -2179.7278*z + 2613.0283 
  return  resultat
# lecture de l'image de référence pour le contour
imageRef = cv2.imread('OpenCVImages/OriginalImage.jpg')
#déclaration de l'image background pour l'affichage
if selection == "v":
  imageDestination = cv2.imread('OpenCVImages/VoltageCanvas.jpg')
elif selection == "m":
  imageDestination = cv2.imread('OpenCVImages/MassCanvas.jpg')
elif selection == "f":
    imageDestination = cv2.imread('OpenCVImages/ForceCanvas.jpg')
elif selection == "p":
        imageDestination = cv2.imread('OpenCVImages/PressureCanvas.jpg')
#acquisition des contours
imgray = cv2.cvtColor(imageRef, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

#fonction de normalisation des valeur(pour attribuer une couleur aux valeurs)
valeurNormalisee = mcolors.Normalize(vmin = VALEURMIN, vmax = VALEURMAX)
#déclaration de la color map 'jet'
cmap = plt.get_cmap('jet')
#tableau contenant les positions des valeurs de pression sur l'affichage
tableauPositionsTexte = [(120, 800), (150, 1000), (530, 1250), (175, 1250), (90, 600), (85, 400),(100, 200), (460, 165), (320, 480), (355, 1080), (345, 875), 
                         (340, 670),(530, 1000), (550, 800), (570, 600), (550, 380)]
#tableau contenant les indexs des contours à remplir pour chaque capteur
tableauContours = [17, 9, 5, 3, 23, 31, 33, 35, 28, 11, 15, 21, 7, 13, 19, 26]

#option pour afficher ou pas les valeurs numériques
affichageNumerique = True
#option pour afficher les valeurs numériques avec la même couleur que le capteur
affichageRGB = True

# fonction d'affichage temps réel
def updateMap(zones):

  #tout couvrir de blanc pour ne pas que le nouveau texte overlap sur l'ancien
  cv2.drawContours(imageDestination, contours, 0, color=(255, 255, 255), thickness=cv2.FILLED)
  #affichage des contours
  cv2.drawContours(imageDestination, contours, -1, (0,0,0), 5)
  cv2.drawContours(imageDestination, contours, 0, (255,255,255), 3)
  cv2.drawContours(imageDestination, contours, 1, (255,255,255), 3)
  #affichage des 16 capteurs
  for indexZone, indexPosition, indexContour in zip(zones, tableauPositionsTexte, tableauContours):
       rgba = cmap(valeurNormalisee(indexZone))
       r, g, b, a = [int(x * 255) for x in rgba[:4]]
       cv2.drawContours(imageDestination, contours, indexContour, color=(b, g, r), thickness=cv2.FILLED)
       if affichageNumerique:
        if selection == "v" or selection == "m" :
          texte = "{:.0f}".format(indexZone)
        else:
          texte = "{:.3f}".format(indexZone)

        if affichageRGB:
          cv2.putText(imageDestination, text = texte, org = indexPosition, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=(b, g, r), thickness=2)
        else:
          cv2.putText(imageDestination, text = texte, org = indexPosition, fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1.0, color=(0, 0, 0), thickness=2)

  #rafraichissement de l'affichage
  cv2.imshow('Systeme de diagnostique podiatrique dynamique', imageDestination)
  cv2.waitKey(1)
  print("affichage réussi")


#Boucle de lecture des données 
async def main():
  async with BleakClient(address) as client:
      await client.connect()
      while True:
      #Extraction des voltages
        mesures = await client.read_gatt_char(MESURES_UUID)
        zones = [] # 
        for i in range (0, len(mesures), 4):
          voltage, = (struct.unpack('<I', mesures[i:i+4]))
          #Calcul de la résistance du capteur (diviseur de tension)
          resistance = ((3.3*430000 - voltage*430)/(voltage/1000))
          #Conditions afin de ne pas afficher de masses négatives
          if (resistance > 228000.0):
            masse = 0
          elif (resistance < 68000.0):
            masse = 10000
          else:
            masse = masse_interpolee((resistance-1.017e+05)/3.292e+04)
          #Calcul de la force sur le capteur (N)
          force = (masse * 9.80665)/1000
          #Calcul de la pression (moyenne) sur le capteur (kPa)
          pression = (force/surface)/1000
          if selection == "v":
            zones.append(voltage)
          elif selection == "m":
            zones.append(masse)
          elif selection == "f":
            zones.append(force)
          elif selection == "p":
            zones.append(pression)
        #appel de la fonction d'affichage
        updateMap(zones)
asyncio.run(main())


