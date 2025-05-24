# System pomiaru odległości z wykorzystaniem Raspberry Pi, czujnika ultradźwiękowego, wyświetlacza OLED, diod LED i buzzera

## Opis projektu

Projekt realizuje funkcję pomiaru odległości za pomocą czujnika ultradźwiękowego HC-SR04 podłączonego do Raspberry Pi. Wynik pomiaru prezentowany jest na wyświetlaczu OLED SSD1306. Dodatkowo, odległość sygnalizowana jest wizualnie (za pomocą pięciu diod LED) oraz dźwiękowo (poprzez buzzer). Projekt został zrealizowany w ramach zajęć laboratoryjnych.

## Autorzy

- Jan Bujok  
- Michał Rempalski

## Wymagane biblioteki 

```python
import RPi.GPIO as GPIO
from luma.core.interface.serial import spi
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont
```

Instalacja:
```bash
pip install RPi.GPIO
pip install luma.oled
pip install Pillow
```

## Opis działania programu

1. **Inicjalizacja GPIO** – przypisanie odpowiednich pinów dla czujnika, diod oraz buzzera.
2. **Inicjalizacja wyświetlacza OLED** – połączenie przez SPI, przygotowanie obszaru rysowania, ustawienie czcionki.
3. **Pomiar odległości** – generacja impulsu wyzwalającego TRIG, oczekiwanie na sygnał ECHO, obliczenie czasu przelotu fali i przeliczenie go na odległość.
4. **Sterowanie diodami LED** – w zależności od odległości aktywowane są odpowiednie diody.
5. **Sterowanie buzzerem** – aktywacja przy odległości mniejszej niż 4 cm.
6. **Wyświetlanie na OLED** – wynik pomiaru w centymetrach jest wyświetlany na ekranie.

## Fragmenty kodu

### Pomiar odległości
```python
def odleglosc():
    signal()
    czas = oczekiwanie_na_echo()
    if czas:
        return round(czas * 34300 / 2, 2)
    return None
```

### Sterowanie diodami
```python
def kontrola_diod(dystans):
    # Zapala odpowiednią liczbę diod w zależności od dystansu
```

### Sterowanie buzzerem
```python
def kontrola_buzzera(dystans):
    if dystans < 4:
        GPIO.output(BUZZER, GPIO.HIGH)
    else:
        GPIO.output(BUZZER, GPIO.LOW)
```

### OLED
```python
def pokaz_na_ekranie(tekst):
    # Wyświetla tekst na ekranie OLED
```

### Pętla główna programu
```python
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
```

## Uruchomienie
Po zainstalowaniu wszystkich potrzebnych bibliotek i odpowiednim podłączeniu wszystkich elementów uruchom plik `Ekranodl.py`:

```bash
python3 Ekranodl.py
```

