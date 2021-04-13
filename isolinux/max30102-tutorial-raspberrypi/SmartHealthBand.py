# SPDX-FileCopyrightText: Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
#
# Ported to Pillow by Melissa LeBlanc-Williams for Adafruit Industries from Code available at:
# https://learn.adafruit.com/adafruit-oled-displays-for-raspberry-pi/programming-your-display

# Imports the necessary libraries...
import time
import board
import digitalio
import busio as io
import adafruit_mlx90614
import RPi.GPIO as GPIO
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import max30102
import hrcalc

import time
import board
import busio as io
import adafruit_mlx90614
import pyrebase

from board import SCL, SDA
import busio
from PIL import Image
import adafruit_ssd1306


#defining pin for the button
GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

m = max30102.MAX30102()

i2c = io.I2C(board.SCL, board.SDA, frequency=100000)
mlx = adafruit_mlx90614.MLX90614(i2c)

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)


#i2c = board.I2C()

#oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Clear display.
oled.fill(0)
oled.show()

config = {
  "apiKey": "Xh4o0OuBCz2hBtiD6dttanCMKLyuE2yLUV2DUMBr",
  "authDomain": "Covitrix-Senior.firebaseapp.com",
  "databaseURL": "https://covitrix-senior-default-rtdb.firebaseio.com/",
  "storageBucket": "Covitrix-Senior.appspot.com"
}
# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load a font in 2 different sizes.
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

offset = 0  # flips between 0 and 32 for double buffering
hrAv=0
lastTemp = mlx.object_temperature
prevTempTime = int(time.time())
firebase = pyrebase.initialize_app(config)
db = firebase.database()
while True:
    ambientString = "{:.2f}".format(mlx.ambient_temperature)
    objectString = "{:.2f}".format(mlx.object_temperature)

    ambientCelsius = float(ambientString)
    objectCelsius = float(objectString)

    
   

    if (time.time() > (prevTempTime + 2)):
        lastTemp = mlx.object_temperature
        prevTempTime = int(time.time())
    # Create blank image for drawing.
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    # write the current time to the display after each scroll
    draw.rectangle((0, 0, oled.width, oled.height * 2), outline=0, fill=0)
    text = time.strftime(str(lastTemp))
    text = "Temp"
    draw.rectangle((10, 0, oled.width, oled.height * 2), outline=0, fill=0)
    text = time.strftime(str(lastTemp))
    text = text[:5]
    draw.text((0, 0), text, font=font, fill=255)
    text = time.strftime("%e %b %Y")
    draw.text((0, 14), text, font=font, fill=255)
    text = time.strftime("%X")
    draw.text((0, 36), text, font=font2, fill=255)

    oled.image(image)
    oled.show()

    if GPIO.input(15) == GPIO.HIGH:
        isValueAccurate = False
        heartAnimation =True
        
        while not isValueAccurate:
            oled.fill(0)
            oled.show()
            offset=15
            
            hr_1 = 0
            hr_2 = 0
            hr_3 = 0
            
            spo2_1 = 0
            spo2_2 = 0
            spo2_3 = 0
            
            spo2Sum = 0;
            spo2Count = 0
            
            for x in range(3):
                if (heartAnimation):
                    image = Image.open("big_heart.ppm").convert("1")
                    
                else:
                    image = Image.open("small_heart.ppm").convert("1")             
                    
                oled.image(image)
                oled.show()
                heartAnimation = not heartAnimation 
                red, ir = m.read_sequential()
                hr, irValid, spo2, redValid =hrcalc.calc_hr_and_spo2(ir, red) 
            
                if (x == 0):
                    
                    hr_1 = hr
                    spo2_1 = spo2
                    if (spo2_1 <= 100 and spo2_1 >= 80):
                        spo2Sum = spo2Sum + spo2_1
                        spo2Count = spo2Count + 1
                        
                    print(hr," - ",spo2)
                    print("1st");
                if (x == 1):
                    hr_2 = hr
                    spo2_2 = spo2
                    if (hr_2 > (hr_1 + offset) or hr_2 < (hr_1 - offset) or hr_2 > 300):
                        print(hr," - ",spo2)
                        print("break 2nd")
                        break
                    if (spo2_1 <= 100 and spo2_1 >= 80):
                        spo2Sum = spo2Sum + spo2_1
                        spo2Count = spo2Count + 1
                        
                    print(hr," - ",spo2)
                    print ("2nd")
                if (x == 2):
                    hr_3 = hr
                    spo2_3 = spo2
                    if (hr_3 > (hr_2 + offset) or hr_3 < (hr_2 - offset) or hr_2 > 300):
                        print(hr," - ",spo2)
                        print("break 3rd")
                        break
                    
                    if (spo2_1 <= 100 and spo2_1 >= 80):
                        spo2Sum = spo2Sum + spo2_1
                        spo2Count = spo2Count + 1
                        
                    hrAv=(hr_1+hr_2+hr_3)/3
                    spo2Av = spo2Sum / spo2Count
                    isValueAccurate = True
                    print(hr," - ",spo2)
                    print ("3rd")
                    data = {
                    "ambient": (ambientCelsius),
                    "Temperature": str(objectCelsius),
                    "HeartRate": str(hrAv),
                    "SPO2": str(spo2Av),
                    "TimeDate": str(time.strftime("%X"))+"--> "+str(time.strftime("%e %b %Y"))
                    }
                    db.child("Covitrix").child("data_current").set(data)
                    db.child("Covitrix").child("data_log").push(data)
                    db.child("Covitrix").child("data").set(data)
                    db.child("sensors").child("1").set(data)
                    
  
                    print("BPM", hrAv)
                    print("SPO2", spo2Av)

                
                
