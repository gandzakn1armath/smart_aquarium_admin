from gpiozero import PWMOutputDevice, DistanceSensor, AngularServo, LightSensor, LED, Button
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import Adafruit_DHT
import threading
from time import strftime, sleep
import RPi.GPIO as GPIO
import os
import glob
import serial
import json

USER_ID = "-N0E8J3ItyjCsWAJ-0l4"

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

buzzer = PWMOutputDevice(12)
bobber = Button(10)
in1 = 14
in2 = 15
in3 = 23
in4 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

yellowR = PWMOutputDevice(in1)
yellowL = PWMOutputDevice(in2)
whiteR = PWMOutputDevice(in3)
whiteL = PWMOutputDevice(in4)

aquariumFilter = PWMOutputDevice(18)
aquariumHeater = PWMOutputDevice(17)
ultrasonic = DistanceSensor(echo=16, trigger=20)

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 27
ledR = LED(22)

ledsEnabled = False
filterEnabled = False
isFeedFish = False
servo = None

cred = credentials.Certificate("/home/pi/Desktop/smart_aquarium.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smart-aquarium-e9439-default-rtdb.firebaseio.com/'
})


def update_user_data(key, value):
    ref = db.reference('/')
    ref.child(USER_ID).update({key: value})


def update_user_data(value):
    ref = db.reference('/')
    ref.child(USER_ID).update(value)


def get_user_data(key):
    ref = db.reference('/')
    user = ref.child(USER_ID)
    json_object = json.loads(json.dumps(user.get()))
    return json_object[key]


def get_led_white():
    return get_user_data("led_white")


def get_led_yellow():
    return get_user_data("led_yellow")


def get_filter():
    return get_user_data("filter")


def get_heater():
    return get_user_data("heater")


def get_feed():
    return get_user_data("feed")


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
        temp_string = lines[1][equals_pos + 2:]
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
    global servo
    servo.angle = -90
    sleep(1)
    servo.angle = 0
    sleep(1)
    servo.angle = 90
    sleep(1)


def feedFish():
    global isFeedFish, ledsEnabled, filterEnabled
    isFeedFish = True
    ledsEnabled = True
    ledOn()
    filterEnabled = True
    filterOff()
    feed()
    sleep(10)
    filterEnabled = False
    sleep(2)
    ledsEnabled = False
    isFeedFish = False


def yellow():
    global ledsEnabled
    while True:
        try:

            yellowLed = get_led_yellow()
            if yellowLed == 1:
                yellowOn()
            else:
                if not ledsEnabled:
                    yellowOff()

        except Exception:
            pass


def white():
    global ledsEnabled
    while True:
        try:
            whiteLed = get_led_white()
            hour = strftime("%H")
            minute = strftime("%M")
            second = strftime("%S")

            if hour == "18" and minute == "00" and second == "00":
                update_user_data({'led_white': True})

            if hour == "23" and minute == "59" and second == "59":
                update_user_data({'led_white': False})

            if whiteLed == 1:
                whiteOn()
            else:
                if not ledsEnabled:
                    whiteOff()
        except Exception:
            pass


def sensors():
    global bobber
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if __name__ == '__main__':
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.flush()
    while True:
        try:
            if ser.in_waiting > 0:
                waterAcidity = float(ser.readline().decode('utf-8').rstrip())
                update_user_data({'water_acidity': waterAcidity})

            sleep(10)
        except Exception:
            pass


def other_sensors():
    global bobber
    Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    while True:
        try:
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
            update_user_data({'humidity': float(humidity),
                              'temperature': float(temperature),
                              'bobber': bobber.is_pressed})
            waterTemp = read_temp()
            update_user_data({'water_temperature': float(waterTemp)})
            sleep(10)
        except Exception:
            pass


def servo_motor():
    global servo
    servo = AngularServo(21, min_pulse_width=0.0001, max_pulse_width=0.0026)
    servo.angle = 90
    while True:
        try:
            ledR.off()
            feed = get_feed()
            if feed == 1:
                feedFish()
                update_user_data({'feed': 0})
        except Exception:
            ledR.on()
            sleep(1)


def filterWater():
    global filterEnabled
    while True:
        try:
            waterFilter = get_filter()
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
            waterHeater = get_heater()
            if waterHeater == 1:
                heaterOn()
            else:
                heaterOff()
        except Exception:
            pass


threadWhite = threading.Thread(target=white)
threadYellow = threading.Thread(target=yellow)
threadServo = threading.Thread(target=servo_motor)
threadFilter = threading.Thread(target=filterWater)
threadSensors = threading.Thread(target=sensors)
threadOtherSensors = threading.Thread(target=other_sensors)

threadWhite.start()
threadYellow.start()
threadServo.start()
threadFilter.start()
threadSensors.start()
threadOtherSensors.start()
print("Start")

while True:
    try:
        hour = strftime("%H")
        minute = strftime("%M")
        second = strftime("%S")

        if GPIO.input(26):
            feedFish()

        if hour == "18" and minute == "00" and second == "00":
            feedFish()

        dic = int(ultrasonic.distance * 100)
        sleep(0.1)
        if not isFeedFish:
            if dic > 20 and dic < 80:
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
