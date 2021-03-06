import requests
from yoctopuce.yocto_display import *
from yoctopuce.yocto_wireless import *


def http_req(url):
    reponse = requests.get(url)
    if reponse.status_code == 200:
        json_reponse = reponse.json()
        return json_reponse
    return None


hub_url = 'usb'

if len(sys.argv) > 1:
    hub_url = sys.argv[1].upper()

errmsg = YRefParam()
# Configuration de l'Api
if YAPI.RegisterHub(hub_url, errmsg) != YAPI.SUCCESS:
    sys.exit("init error" + errmsg.value)

# Desactive les exceptions dans l'API
# YAPI.DisableExceptions()

# Affichage du signal Wifi
Wifi = YWireless.FirstWireless()

Screen = YDisplay.FirstDisplay()
if (Screen.isOnline()):
    print("Ecran connecte")
else:
    print("Ecran non connecte")

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
layer0.drawRect(5, 10, 123, 54)
layer0.drawRect(4, 9, 124, 55)
layer0.drawText(w / 2, h / 3, YDisplayLayer.ALIGN.CENTER, "Yocto")
layer0.drawText(w / 2, h / 3 * 2, YDisplayLayer.ALIGN.CENTER, "Bus Scheduler")
time.sleep(2)
layer0.clear()

while True:
    myDate = datetime.datetime.now()
    # print(str(myDate.hour) + ":" + str(myDate.minute) + ":" + str(myDate.second))
    urlMollaz1 = 'http://www.tpg.ch/TempsReel-portlet/TRService?method=GetProchainsDepartsTriLigneSens&codeArret=MOLL&lignes=L&destinations=ATHENAZ'
    urlMollaz2 = 'http://www.tpg.ch/TempsReel-portlet/TRService?method=GetProchainsDepartsTriLigneSens&codeArret=MOLL&lignes=L&destinations=PXPLUSXR%20BERNEX'

    try:
        mollaz1 = http_req(urlMollaz1)
        mollazf1Flag = True
    except Exception as ecx:
        print("Exception lors de l acces au serveur TPG (No 1)" + str(ecx))
        mollazf1Flag = False
    try:
        mollaz2 = http_req(urlMollaz2)
        mollazf2Flag = True
    except Exception as ecx:
        print("Exception lors de l acces au serveur TPG (No 2):" + str(ecx))
        mollazf2Flag = False

    if (Screen.isOnline()):
        layer4.drawRect(0, 10, 128, 10)
        layer4.drawRect(w / 2, 10, w / 2, 64)
        layer0.clear()
        layer0.selectFont('8x8.yfm')

        # Affichage de l'heure
        if (myDate.minute < 10):
            stringBuild = str(str(myDate.hour) + ":0" + str(myDate.minute))
        else:
            stringBuild = str(str(myDate.hour) + ":" + str(myDate.minute))
        layer0.drawText(0, 0, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)

        # Affichage du signal Wifi
        if Wifi is not None:
            stringBuild = "RSSI:" + str(Wifi.get_linkQuality())
            layer0.drawText(128, 0, YDisplayLayer.ALIGN.TOP_RIGHT, stringBuild)

        # Direction Athenaz
        try:
            stringBuild = str(mollaz1['prochainsDeparts']['prochainDepart'][0]['destination'])
            layer0.drawText(1, 13, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)

            layer0.drawRect(0, 21, 62, 41)
            layer0.drawText(62, 23, YDisplayLayer.ALIGN.TOP_RIGHT, "1")
            stringBuild = str(mollaz1['prochainsDeparts']['prochainDepart'][0]['attente']) + "'"
            layer0.drawText(1, 23, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)
            stringBuild = str(mollaz1['prochainsDeparts']['prochainDepart'][0]['heureArrivee'])
            layer0.drawText(1, 33, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)

            layer0.drawRect(0, 42, 62, 63)
            layer0.drawText(62, 44, YDisplayLayer.ALIGN.TOP_RIGHT, "2")
            if (mollaz1['prochainsDeparts']['prochainDepart'][1]['attente'] == "&gt;1h"):  # bug de reponse TPG
                stringBuild = "<60'"
            else:
                stringBuild = str(mollaz1['prochainsDeparts']['prochainDepart'][1]['attente']) + "'"
            layer0.drawText(1, 44, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)
            stringBuild = str(mollaz1['prochainsDeparts']['prochainDepart'][1]['heureArrivee'])
            layer0.drawText(1, 55, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)
        except Exception as ecx:
            print("Exception dans l'affichge des donnees [1]:" + str(ecx))

        # Direction Bernex
        try:
            stringBuild = str(mollaz2['prochainsDeparts']['prochainDepart'][0]['destination'])
            layer0.drawText(64, 13, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)

            layer0.drawRect(64, 21, 126, 41)
            layer0.drawText(126, 23, YDisplayLayer.ALIGN.TOP_RIGHT, "1")
            stringBuild = str(mollaz2['prochainsDeparts']['prochainDepart'][0]['attente']) + "'"
            layer0.drawText(66, 23, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)
            stringBuild = str(mollaz2['prochainsDeparts']['prochainDepart'][0]['heureArrivee'])
            layer0.drawText(66, 33, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)

            layer0.drawRect(64, 42, 126, 63)
            layer0.drawText(126, 44, YDisplayLayer.ALIGN.TOP_RIGHT, "2")
            if (mollaz2['prochainsDeparts']['prochainDepart'][1]['attente'] == "&gt;1h"):  # bug de reponse TPG
                stringBuild = "<60'"
            else:
                stringBuild = str(mollaz2['prochainsDeparts']['prochainDepart'][1]['attente']) + "'"
            layer0.drawText(66, 44, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)
            stringBuild = str(mollaz2['prochainsDeparts']['prochainDepart'][1]['heureArrivee'])
            layer0.drawText(66, 55, YDisplayLayer.ALIGN.TOP_LEFT, stringBuild)
        except Exception as ecx:
            print("Exception dans l'affichge des donnees [2]:" + str(ecx))
        Screen.swapLayerContent(0, 1)

    else:
        print("Ecran non atteignable")
    time.sleep(1)