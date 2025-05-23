import RPi.GPIO as GPIO
import time
from luma.core.interface.serial import spi
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# GPIO dla czujnika i diod
ECHO = 16
TRIG = 26
D1 = 27
D2 = 17
D3 = 5
D4 = 6
D5 = 13
BUZZER = 22

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(D1, GPIO.OUT)
GPIO.setup(D2, GPIO.OUT)
GPIO.setup(D3, GPIO.OUT)
GPIO.setup(D4, GPIO.OUT)
GPIO.setup(D5, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)

# OLED setup (SPI)
serial = spi(port=0, device=0, gpio_DC=25, gpio_RST=24)
oled = ssd1306(serial, width=128, height=64)

# Czcionka OLED
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size=22)

# Pomiar odległości
def signal():
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.05)
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(10e-6)
    GPIO.output(TRIG, GPIO.LOW)

def oczekiwanie_na_echo():
    czekanie = time.time() + 1
    while GPIO.input(ECHO) == GPIO.LOW:
        czas_poczatkowy = time.time()
        if time.time() > czekanie:
            return None
    while GPIO.input(ECHO) == GPIO.HIGH:
        czas_koncowy = time.time()
        if time.time() > czekanie:
            return None
    return czas_koncowy - czas_poczatkowy

def odleglosc():
    signal()
    czas_przelotu = oczekiwanie_na_echo()
    if czas_przelotu is not None:
        return round(czas_przelotu * 34300 / 2, 2)
    return None

def kontrola_diod(dystans):
    diody = [D1, D2, D3, D4, D5]
    if dystans < 5.3:
        ilosc_diod = 5
    elif dystans < 7:
        ilosc_diod = 4
    elif dystans < 11:
        ilosc_diod = 3
    elif dystans < 15:
        ilosc_diod = 2
    elif dystans < 20:
        ilosc_diod = 1
    else:
        ilosc_diod = 0

    for dioda in diody:
        GPIO.output(dioda, GPIO.LOW)
    for i in range(ilosc_diod):
        GPIO.output(diody[i], GPIO.HIGH)

def kontrola_buzzera(dystans):
    if dystans < 4:
        GPIO.output(BUZZER, GPIO.HIGH)
    else:
        GPIO.output(BUZZER, GPIO.LOW)

def pokaz_na_ekranie(tekst):
    obraz = Image.new("1", oled.size)
    rysuj = ImageDraw.Draw(obraz)
    rysuj.text((0, 20), tekst, font=font, fill=255)
    oled.display(obraz)

# Pętla główna
try:
    while True:
        dystans = odleglosc()
        if dystans is not None:
            kontrola_diod(dystans)
            kontrola_buzzera(dystans)
            pokaz_na_ekranie(f"{dystans} cm")
        else:
            pokaz_na_ekranie("Brak odczytu")
        time.sleep(1)

except KeyboardInterrupt:
    print("Zatrzymano")

finally:
    GPIO.cleanup()
