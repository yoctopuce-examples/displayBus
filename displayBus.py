import json
import requests

import os, sys
# add ../../Sources to the PYTHONPATH
sys.path.append(os.path.join("..", "..", "Sources"))

from yoctopuce.yocto_api import *
from yoctopuce.yocto_display import *
from yoctopuce.yocto_wireless import *

from datetime import datetime


errmsg = YRefParam()
# Configuration de l'Api
if YAPI.RegisterHub("192.168.1.114", errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

# Desactive les exceptions dans l'API
YAPI.DisableExceptions()

# Connexion au Yocto-Hub
HubWifi = YModule.FindModule("YHUBWLN3-EAC9D")
if(HubWifi.isOnline()):
	Wifi = YWireless.FirstWireless()
	print("Hub connecte")
	Screen = YDisplay.FirstDisplay()
	if(Screen.isOnline()):
		print("Ecran connecte")
	else:
		print("Ecran non connecte")		
else:
	sys.exit("Hub wifi non atteignable")

# Efface l'ecran
Screen.resetAll()

# Recuperation de la taille de l'ecran
w = Screen.get_displayWidth()
h = Screen.get_displayHeight()

# Declaration des couches de l'ecran
layer0 = Screen.get_displayLayer(0)
layer1 = Screen.get_displayLayer(1)
layer4 = Screen.get_displayLayer(4)
layer0.clear()

# Affiche l'ecran de demarrage
layer0.selectFont('Medium.yfm')
layer0.drawRect(5,10,123,54)
layer0.drawRect(4,9,124,55)
layer0.drawText(w / 2, h/3, YDisplayLayer.ALIGN.CENTER, "Yocto")
layer0.drawText(w / 2, h/3*2, YDisplayLayer.ALIGN.CENTER, "Bus Scheduler")
time.sleep(2)
layer0.clear()

while True:
	myDate = datetime.now()
	#print(str(myDate.hour) + ":" + str(myDate.minute) + ":" + str(myDate.second))
	urlMollaz1 = 'https://www.tpg.ch/TempsReel-portlet/TRService?method=GetProchainsDepartsTriLigneSens&codeArret=MOLL&lignes=L&destinations=ATHENAZ'
	urlMollaz2 = 'https://www.tpg.ch/TempsReel-portlet/TRService?method=GetProchainsDepartsTriLigneSens&codeArret=MOLL&lignes=L&destinations=PXPLUSXR%20BERNEX'
	def http_req(url):
		response = requests.get(url)
		if response.status_code == 200:
			json_response = response.json()
			return json_response
		return None
	try:
		mollaz1 = http_req(urlMollaz1)
		mollazf1Flag = True
	except:
		print("Failure Accessing TPG Server (No 1)")
		mollazf1Flag = False
	try:
		mollaz2 = http_req(urlMollaz2)
		mollazf2Flag = True
	except:
		print("Failure Accessing TPG Server (No 2)")
		mollazf2Flag = False

	
	if(HubWifi.isOnline()):
		layer4.drawRect(0,10,128,10)
		layer4.drawRect(w/2,10,w/2,64)
		layer0.clear()
		layer0.selectFont('8x8.yfm')
		
		#Affichage de l'heure
		if(myDate.minute < 10):
			stringBuild = str(str(myDate.hour) + ":0" + str(myDate.minute))
		else:
			stringBuild = str(str(myDate.hour) + ":" + str(myDate.minute))
		layer0.drawText(0, 0, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)
		
		#Affichage du signal Wifi
		stringBuild = "RSSI:" + str(Wifi.get_linkQuality())
		layer0.drawText(128, 0, YDisplayLayer.ALIGN.TOP_RIGHT, stringBuild)
		
		#Direction Athenaz
		try:
			stringBuild = str(mollaz1['prochainsDeparts']['prochainDepart'][0]['destination'])
			layer0.drawText(1,13, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)	
			
			layer0.drawRect(0,21,62,41)
			layer0.drawText(62,23, YDisplayLayer.ALIGN.TOP_RIGHT, "1")			
			stringBuild = str(mollaz1['prochainsDeparts']['prochainDepart'][0]['attente']) + "'"
			layer0.drawText(1,23, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)			
			stringBuild = str(mollaz1['prochainsDeparts']['prochainDepart'][0]['heureArrivee'])
			layer0.drawText(1,33, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)	

			layer0.drawRect(0,42,62,63)
			layer0.drawText(62,44, YDisplayLayer.ALIGN.TOP_RIGHT, "2")
			if(mollaz1['prochainsDeparts']['prochainDepart'][1]['attente'] == "&gt;1h"):	#bug de reponse TPG
				stringBuild = "<60'"
			else:
				stringBuild = str(mollaz1['prochainsDeparts']['prochainDepart'][1]['attente']) + "'"
			layer0.drawText(1,44, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)	
			stringBuild = str(mollaz1['prochainsDeparts']['prochainDepart'][1]['heureArrivee'])
			layer0.drawText(1,55, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)
		except:
			print("Exception dans l'affichge des donnees [1]")
		
		#Direction Bernex
		try:
			stringBuild = str(mollaz2['prochainsDeparts']['prochainDepart'][0]['destination'])
			layer0.drawText(64,13, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)	
			
			layer0.drawRect(64,21,126,41)
			layer0.drawText(126,23, YDisplayLayer.ALIGN.TOP_RIGHT, "1")
			stringBuild = str(mollaz2['prochainsDeparts']['prochainDepart'][0]['attente']) + "'"
			layer0.drawText(66,23, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)			
			stringBuild = str(mollaz2['prochainsDeparts']['prochainDepart'][0]['heureArrivee'])
			layer0.drawText(66,33, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)	

			layer0.drawRect(64,42,126,63)
			layer0.drawText(126,44, YDisplayLayer.ALIGN.TOP_RIGHT, "2")
			if(mollaz2['prochainsDeparts']['prochainDepart'][1]['attente'] == "&gt;1h"):	#bug de reponse TPG
				stringBuild = "<60'"
			else:
				stringBuild = str(mollaz2['prochainsDeparts']['prochainDepart'][1]['attente']) + "'"
			layer0.drawText(66,44, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)	
			stringBuild = str(mollaz2['prochainsDeparts']['prochainDepart'][1]['heureArrivee'])
			layer0.drawText(66,55, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)			
		except:
			print("Exception dans l'affichge des donnees [2]")
		Screen.swapLayerContent(0,1)

	else:
		print("Ecran non atteignable")
	time.sleep(1)