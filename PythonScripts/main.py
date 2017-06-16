# Elektrotehnicki fakultet Univerziteta u Sarajevu
# Godina : 2017
# Predmet : Ugradbeni sistemi
# Profesor : Konjicija Samim
# Asistentica: Zubaca Jasmina
# Studenti:
#       -Mustajbasic Belmin (16796)
#       -Mesihovic Mirza    (17345)
# Kod:


from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import RPi.GPIO as GPIO2
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import time
import threading
import pygame
import urllib2
import datetime
import csv

import requests

from Reminder import Reminder

# Konfiguracija za displej
DC = 24
RST = 25
SPI_PORT = 0
SPI_DEVICE = 0

# Button Configuration
BTN1 = 26
BTN2 = 13
BTN3 = 6

# LED Configuration
LED = 17
LEDStatus = False
GPIO2.setmode(GPIO2.BCM)
GPIO2.setup(BTN1, GPIO2.IN, pull_up_down=GPIO2.PUD_UP)
GPIO2.setup(BTN2, GPIO2.IN, pull_up_down=GPIO2.PUD_UP)
GPIO2.setup(BTN3, GPIO2.IN, pull_up_down=GPIO2.PUD_UP)
GPIO2.setup(LED, GPIO2.OUT)
GPIO2.setwarnings(False)
taskPointer = 0

# Flags

flagCSV = True
flagIdle = True
flagAlarm = False
flagTasks = False
flagLed = False
flagSound = False

font = ImageFont.truetype("Monospace.ttf", 32 )
fontReminder = ImageFont.truetype("Monospace.ttf", 19 )
fontHeader = ImageFont.truetype("Monospace.ttf", 16)
fontClock = ImageFont.truetype("Monospace.ttf", 80)
fontAlarmDateTime = ImageFont.truetype("Monospace.ttf", 28)

disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
disp.begin() 

reminderi = []
def deleteReminder():
    req = requests.post("http://localhost/pi/api/deleteFromRPi.php",data={'deleteKey':'GoOnDeleteIt'})
    print "Status of deleteReport: "+str(req.status_code)+" " +str(req.reason)


    
def draw_rotated_text(image, text, position, font, fill=(255,255,255)):
    draw = ImageDraw.Draw(image)
    width, height = draw.textsize(text, font=font)
    textimage = Image.new('RGBA', (width, height), (0,0,0,0))
    textdraw = ImageDraw.Draw(textimage)
    textdraw.text((0,0), text, font=font, fill=fill)
    rotated = textimage.rotate(90, expand=1)
    image.paste(rotated, position, rotated)

def DajPoruku(text):
	if isinstance(text,str):
		if (len(text) < 26):
                        lista = []
			while(len(text)<26):
				text = text + " "
			lista.append(text)
			lista.append("                          ")
			return lista
		elif (len(text)>26 and len(text)<52):
			lista = []
			lista.append(text[0:25]+"-")
			tmp = text[25:]
			while(len(tmp)<26):
				tmp = tmp + " "
			lista.append(tmp)
			return lista
		elif (len(text)>52):
			lista = []
			lista.append(text[0:25]+"-")
			lista.append(text[25:50]+"...")
			return lista

def displayIdleScreen(display,row1,row2,row3):
    display.clear()
    draw_rotated_text(disp.buffer, 'DESK ASSISTANT - Raspberry Pi 3', (5, 20), fontHeader, fill=(255,255,255))
    #Ispis datuma
    dateText=datetime.datetime.now()
    draw_rotated_text(disp.buffer, dateText.strftime("%d.%m.%Y"), (35, 80), font, fill=(255,255,255))

    draw_rotated_text(disp.buffer, dateText.strftime("%H:%M"), (60, 60), fontClock, fill=(255,255,255))

    draw_rotated_text(disp.buffer, row1, (155, 10), fontReminder, fill=(255,255,255))
    draw_rotated_text(disp.buffer, row2, (180, 10), fontReminder, fill=(0,255,0))
    draw_rotated_text(disp.buffer, row3, (205, 10), fontReminder, fill=(0,255,0))
    disp.display()


def displayAlarmScreen(display,row2,row3):
    display.clear()
    draw_rotated_text(disp.buffer, 'DESK ASSISTANT - Raspberry Pi 3', (5, 20),  fontHeader, fill=(255,255,255))
    dateText=datetime.datetime.now()
    draw_rotated_text(disp.buffer, dateText.strftime("%d.%m.%Y"), (30, 145), fontAlarmDateTime, fill=(255,255,255))
    draw_rotated_text(disp.buffer, dateText.strftime("%H:%M"), (30, 10),  fontAlarmDateTime, fill=(255,255,255))
    base = Image.open('alarm.png').convert('RGBA')
    rotated = base.rotate(90, expand=1)
    disp.buffer.paste(rotated,(80,110),rotated)
    draw_rotated_text(disp.buffer, row2, (180, 10), fontReminder, fill=(255,0,0))
    draw_rotated_text(disp.buffer, row3, (205, 10), fontReminder, fill=(255,0,0))
    disp.display()

def displayTaskScreen(display,row1,row2,row3):
    display.clear()
    draw_rotated_text(disp.buffer, 'DESK ASSISTANT - Raspberry Pi 3', (5, 20), fontHeader, fill=(255,255,255))
    draw_rotated_text(disp.buffer, row1, (60, 15), font, fill=(100,100,255))
    draw_rotated_text(disp.buffer, row2, (100, 10), fontReminder, fill=(100,100,255))
    draw_rotated_text(disp.buffer, row3, (125, 10), fontReminder, fill=(100,100,255))
    draw_rotated_text(disp.buffer, '<- Prev    Home    Next ->', (220, 10), fontReminder, fill=(255,255,255))
    disp.display()


def refreshCSVThread():
    while True:
        if flagCSV:
            print "Refreshing CSV set of Reminders"
            global reminderi
            tempReminderi = []
            url = 'http://localhost/pi/reminders.csv'
            response = urllib2.urlopen(url)
            cr = csv.reader(response)
            for row in cr:
                tmp = Reminder(row[0],row[1],row[2],row[3],row[4],row[5])
                tempReminderi.append(tmp)
            reminderi = tempReminderi
            time.sleep(2)
def refreshCSVOnce():
    global reminderi
    tempReminderi = []
    url = 'http://localhost/pi/reminders.csv'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    for row in cr:
        tmp = Reminder(row[0],row[1],row[2],row[3],row[4],row[5])
        tempReminderi.append(tmp)
    reminderi = tempReminderi
    
def idleScreenThread():
    global flagIdle
    global disp
    global flagAlarm
    global flagLed
    global flagSound
    while True:
        if flagIdle:
            if len(reminderi) == 0:
                displayIdleScreen(disp,"    No reminders found    ","If you need to be reminded","add it via the webapp     ")
            else:
                poruka = DajPoruku(reminderi[0].getMessage())
                displayIdleScreen(disp,"Next task: "+reminderi[0].getDate(),poruka[0],poruka[1])
                vrijeme = datetime.datetime.now()
                vText = vrijeme.strftime("%d.%m.%Y %H:%M");
                if len(reminderi) > 0:
                    if (reminderi[0].getDate()==vText):
                        flagIdle = False
                        flagAlarm = True
                        flagLed = True
                        flagSound = True            
            time.sleep(1)

def tasksScreenThread():
    global flagIdle
    global disp
    global flagAlarm
    global flagLed
    global flagSound
    while True:
        if flagTasks:
            if len(reminderi) == 0:
                displayIdleScreen(disp,"    No reminders found    ","If you need to be reminded","add it via the webapp     ")
            else:
                taskDate = reminderi[taskPointer].getDate()
                taskPoruka = DajPoruku(reminderi[taskPointer].getMessage())
                displayTaskScreen(disp,taskDate,taskPoruka[0],taskPoruka[1])
                #Dodati slucaj aktivacije alarma
            time.sleep(0.3)

def alarmScreenThread():
    global disp
    print "alarmScreenThread"
    while True:
        if flagAlarm:
            if len(reminderi) > 0:
                poruka = DajPoruku(reminderi[0].getMessage())
                displayAlarmScreen(disp,poruka[0],poruka[1])
            print "alarmScreenThread"
        time.sleep(1)

def ledThread():
    global LEDStatus
    while True:
        if flagLed:
            GPIO2.output(LED,GPIO2.HIGH)
            LEDStatus=True
            time.sleep(0.3)       
            GPIO2.output(LED,GPIO2.LOW)
            LEDStatus = False
            time.sleep(0.3)
            GPIO2.output(LED,GPIO2.HIGH)
            LEDStatus = True
            time.sleep(0.3)       
            GPIO2.output(LED,GPIO2.LOW)
            LEDStatus = False
            time.sleep(1)

def soundThread():
    while True:
        if flagSound:
            print "sound thread"
            pygame.mixer.init()
            pygame.mixer.music.load("b.mp3")
            pygame.mixer.music.play()
            print "Playing sound now"
            while pygame.mixer.music.get_busy() == True:
                continue
            print "Playing sound ended"
            time.sleep(0.1)
        

def btn1Callback(c):
    global flagIdle
    global disp
    global flagAlarm
    global flagLed
    global flagSound
    global flagTasks
    if flagTasks:
        global taskPointer
        if taskPointer > 0:
            taskPointer-=1
    elif flagIdle:
        if len(reminderi)>0:
            flagTasks = True
            flagAlarm = False
            flagLed = False
            flagSound = False
            flagIdle = False
    print "Left Button Event Executed"

def btn2Callback(c):
    global flagIdle
    global disp
    global flagAlarm
    global flagLed
    global flagSound
    global flagTasks
    global LEDStatus
    if flagAlarm:
        deleteReminder()
        refreshCSVOnce()
        time.sleep(1)
        flagAlarm = False
        flagLed = False
        flagSound = False
        flagIdle = True
    elif flagTasks:
        disp.clear()
        taskPointer=0
        flagTasks = False
        flagAlarm = False
        flagLed = False
        flagSound = False
        flagIdle = True
    elif flagIdle:
        if LEDStatus:
            print "off"
            GPIO2.output(LED,GPIO2.LOW)
            LEDStatus = False
        else:
            print "on"
            GPIO2.output(LED,GPIO2.HIGH)
            LEDStatus = True
        
    print "Mid Button Event Executed"

def btn3Callback(c):
    global flagIdle
    global disp
    global flagAlarm
    global flagLed
    global flagSound
    global flagTasks
    if flagTasks:
        global taskPointer
        if taskPointer < len(reminderi)-1:
            taskPointer+=1
    elif flagIdle:
        if len(reminderi)>0:
            flagTasks = True
            flagAlarm = False
            flagLed = False
            flagSound = False
            flagIdle = False
    print "Right Button Event Executed"

GPIO2.add_event_detect(BTN1, GPIO2.FALLING, callback=btn1Callback, bouncetime=300)
GPIO2.add_event_detect(BTN2, GPIO2.FALLING, callback=btn2Callback, bouncetime=1000)
GPIO2.add_event_detect(BTN3, GPIO2.FALLING, callback=btn3Callback, bouncetime=300)

displayIdleScreen(disp,"          Hello!          ","    Belmin Mustajbasic    ","     Mirza Mesihovic      ")

CSVRefreshThread = threading.Thread(target=refreshCSVThread)
IdleScreenThread = threading.Thread(target=idleScreenThread)
TaskScreenThread = threading.Thread(target=tasksScreenThread)
AlarmScreenThread = threading.Thread(target=alarmScreenThread)


LedThread = threading.Thread(target=ledThread)
SoundThread = threading.Thread(target=soundThread)

CSVRefreshThread.start()

time.sleep(1)
IdleScreenThread.start()
AlarmScreenThread.start()
TaskScreenThread.start()
LedThread.start()
SoundThread.start()
while True:
        time.sleep(1e6)
GPIO.cleanup()
