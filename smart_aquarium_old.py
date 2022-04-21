from  gpiozero import PWMOutputDevice,DistanceSensor,AngularServo,LightSensor,LED,Button
from time import sleep,strftime
import Adafruit_DHT
import pyrebase
import threading
import telepot
from time import strftime,sleep
import RPi.GPIO as GPIO
import os
import glob
import serial


os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
config = {     
  "apiKey": "AIzaSyDmLjTHyFMMLg7RyIWpHCtrabgPe15Eyh8",
  "authDomain": "smart-aquarium-804ab.firebaseapp.com",
  "databaseURL": "https://smart-aquarium-804ab-default-rtdb.firebaseio.com",
  "storageBucket": "smart-aquarium-804ab.appspot.com"
}
buzzer = PWMOutputDevice(12)
bobber = Button(10)
in1 = 14
in2 = 15
in3 = 23
in4 = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
yellowR = PWMOutputDevice(in1)
yellowL = PWMOutputDevice(in2)
whiteR = PWMOutputDevice(in3)
whiteL = PWMOutputDevice(in4)
ledR = LED(22)
aquariumFilter = PWMOutputDevice(18)
aquariumHeater = PWMOutputDevice(17)
ultrasonic = DistanceSensor(echo=16, trigger=20) 
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 27
ledsEnabled = False
filterEnabled = False
servo = None
humidity = 0
temperature = 0
waterTemp = 0
waterAcidity = 0
   
try:
    firebase = pyrebase.initialize_app(config)
except Exception:
    pass   
yellowLed  = 0
whiteLed = 0
waterFilter = 0
waterHeater = 0
getServo = 0
isFeedFish = False

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def filterOn():
    aquariumFilter.off()   
    
def filterOff():
    aquariumFilter.on()

def heaterOn():
    aquariumHeater.off() 

def heaterOff():
    aquariumHeater.on()

def yellowOn():
    yellowR.on()
    yellowL.off()


def yellowOff():
    yellowR.off()
    yellowL.off()


def whiteOn():
    whiteR.off()
    whiteL.on()


def whiteOff():
    whiteR.off()
    whiteL.off()


def ledOn():
    yellowOn()
    whiteOn()


def ledOff():
    yellowOff()
    whiteOff()

def feed():
    servo.angle = -90
    sleep(1)
    servo.angle = 0
    sleep(1)
    servo.angle = 90
    sleep(1)

def feedFish():
    global isFeedFish, ledsEnabled , filterEnabled
    isFeedFish = True
    ledsEnabled = True
    ledOn()
    filterEnabled = True
    filterOff()
    feed()
    sleep(15)
    filterEnabled = False
    sleep(2)
    ledsEnabled = False
    isFeedFish = False
    
    
def yellow():
    global firebase , yellowLed , ledsEnabled
    while True:
        try:
            database = firebase.database()
            yellowLed = database.child("LED_YELLOW").get().val()
            if yellowLed == 1:
                yellowOn()
            else:
                if not ledsEnabled:
                    yellowOff()
                
        except Exception:
            pass


def white():
    global firebase
    global ledsEnabled
    global whiteLed
    while True:
        try:
            database = firebase.database()
            whiteLed = database.child("LED_WHITE").get().val()
            hour = strftime("%H")
            minute = strftime("%M")
            second = strftime("%S")

            
            if hour == "18" and  minute == "00" and second == "00":
                database.child("LED_WHITE").set(1)

            if hour == "23" and  minute == "59" and second == "59":  
                database.child("LED_WHITE").set(0)

            if whiteLed == 1:
                whiteOn()
            else:
                if not ledsEnabled:
                    whiteOff()
        except Exception:
            pass

def humidity():
    global humidity, temperature , firebase , bobber,waterAcidity
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if __name__ == '__main__':
        ser = serial.Serial('/dev/ttyUSB0',9600,timeout=1)
        ser.flush()
    while True:
        try:
            if ser.in_waiting > 0:
                waterAcidity = float(ser.readline().decode('utf-8').rstrip())
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
            database = firebase.database()
            database.child("HUMIDITY").set(humidity)
            database.child("TEMPERATURA").set(temperature)
            database.child("BOBBER").set(bobber.is_pressed)
            database.child("WATER_ACIDITY").set(waterAcidity)
            sleep(10);
        except Exception:
            pass

def servo():
    global getServo, servo  
    servo = AngularServo(21, min_pulse_width=0.0001, max_pulse_width=0.0026)
    servo.angle = 90
    while True:
        try:
            global firebase
            ledR.off()
            database = firebase.database()
            getServo = database.child("FEED").get().val()
            if getServo == 1:
                feedFish()
                database.child("FEED").set(0)
        except Exception:
            ledR.on()
            sleep(1)
           


def filterWater():
    global waterFilter,filterEnabled
    while True:
        try:
            global firebase
            database = firebase.database()
            waterFilter = database.child("FILTER").get().val()
            if not filterEnabled:
                if waterFilter == 1:
                    filterOn()
                else:
                    filterOff()
        except Exception:
            pass

def heater():
    while True:
        try:
            global firebase
            global waterHeater
            database = firebase.database()
            waterHeater = database.child("HEATER").get().val()
            if waterHeater == 1:
               heaterOn()
            else:
                heaterOff()
        except Exception:
            pass
           
        
def getYellowStatus():
    global yellowLed
    if yellowLed  == 0:
        return "Yellow led is off"
    else:
        return "Yellow led is on"

def getWhiteStatus():
    global whiteLed
    if whiteLed  == 0:
        return "White led is off"
    else:
        return "White led is on"

def getFilterStatus():
    global waterFilter
    if not waterFilter == 0:
        return "Filter is on"
    else:
        return "Filter is off"

def getHeaterStatus():
    global waterHeater
    if not waterHeater == 0:
        return "Heater is on"
    else:
        return "Heater is off"

def getBobberStatus():
    global boober
    if not bobber.is_pressed:
        return "Water is full"
    else:
        return"Water is scarce"
    
def getWaterAcidity():
    global waterAcidity
    if waterAcidity <= 7:
        return "Water is clean"
    else:
        return "Water is not clean"
  





def meatsureWaterTemp():
    global firebase,waterTemp
    while True:
        try:
            waterTemp= read_temp()
            database = firebase.database()
            database.child("WATER_TEMP").set(waterTemp)            
            sleep(10)
        except Exception:
            pass
            
def handle(msg):
    global telegramText
    global chat_id
    global receiveTelegramMessage
    global firebase
    global bobber
    database = firebase.database()
  
    chat_id = msg['chat']['id']
    telegramText = msg['text'].lower()
  
    print("Message received from " + str(chat_id))
    print("Message  " + telegramText)
  
    if telegramText == "/start":
        bot.sendMessage(chat_id, "Welcome to Armath Aquarium Bot")
        bot.sendMessage(chat_id, "You can do it\n"+
                        "status -  Find out information about the aquarium\n"+
                        "yellow -  turn on or off yellow led\n"+
                        "white  -  turn on or off white led\n"+
                        "feed   -  feed the fish\n"+
                        "filter -  turn on or off filter\n"+
                        "heater -  turn on or off temperature\n"+
                        "sensors - air temperature and humidity information" )
  
    elif telegramText == "yellow":
        val = database.child("LED_YELLOW").get().val()
        database.child("LED_YELLOW").set(not val)
        if not val == 0:
            bot.sendMessage(chat_id, "Yellow led is off")
        else:
            bot.sendMessage(chat_id, "Yellow led is on")
    elif telegramText == "white":
        val = database.child("LED_WHITE").get().val()
        database.child("LED_WHITE").set(not val)
        if not val == 0:
            bot.sendMessage(chat_id, "White led is off")
        else:
            bot.sendMessage(chat_id, "White led is on")
    elif telegramText == "feed":
        database.child("FEED").set(1)
        bot.sendMessage(chat_id, "The fish are fed")
        
    elif telegramText == "heater":
        val = database.child("HEATER").get().val()
        database.child("HEATER").set(not val)
        if not val == 0:
            bot.sendMessage(chat_id, "Heater is off")
        else:
            bot.sendMessage(chat_id, "Heater is on")
    elif telegramText == "filter":
        val = database.child("FILTER").get().val()
        database.child("FILTER").set(not val)
        if not val == 0:
            bot.sendMessage(chat_id, "Filter is off")
        else:
            bot.sendMessage(chat_id, "Filter is on")
    elif telegramText == "sensors":
        bot.sendMessage(chat_id, "Humidity "+str(humidity)+" %")
        bot.sendMessage(chat_id, "Temperature " + str(temperature)+" C")
        bot.sendMessage(chat_id, "Water Temperature " + str(waterTemp)+" C")
    elif telegramText == "status":
        bot.sendMessage(chat_id, "Humidity "+str(humidity)+" % \n"+
                        "Temperature " + str(temperature)+" C\n"+
                        "Water Temperature " + str(waterTemp)+" C\n" +
                        getYellowStatus() + "\n" + getWhiteStatus()+" \n"+
                        getFilterStatus() + "\n" + getHeaterStatus()+"\n"+
                        getBobberStatus()+"\n"+getWaterAcidity())
        
        
bot = telepot.Bot('5214025271:AAHXYu-8FBD9TAwDVgn2syC7xzveH8gqU-s')
bot.message_loop(handle)

threadWhite = threading.Thread(target=white)
threadYellow = threading.Thread(target=yellow)
threadServo = threading.Thread(target=servo)
threadFilter = threading.Thread(target=filterWater)
threadHeater = threading.Thread(target=heater)
threadHumidity = threading.Thread(target=humidity)
threadMeatsureWaterTemp = threading.Thread(target=meatsureWaterTemp)



threadWhite.start()
threadYellow.start()
threadServo.start()
threadFilter.start()
threadHeater.start()
threadHumidity.start()
threadMeatsureWaterTemp.start()


while True:
    
    try:
        hour = strftime("%H")
        minute = strftime("%M")
        second = strftime("%S")
      
        if GPIO.input(26):
            feedFish()
            
        if hour == "18" and  minute == "00" and second == "00":
            feedFish()
         

        
        dic = int(ultrasonic.distance * 100)
        sleep(0.1)
        if not isFeedFish:
            if dic > 20 and dic < 80 :
                ledsEnabled = True
                whiteOn()
            else:
                ledsEnabled = False

        if bobber.is_pressed:
            buzzer.on()
            sleep(1)
            buzzer.off()
            sleep(1)
        



    except KeyboardInterrupt:
        break
    except Exception:
        break
        pass   
