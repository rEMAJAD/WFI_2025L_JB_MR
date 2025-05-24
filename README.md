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

1. **Inicjalizacja GPIO** – przypisanie pinów TRIG, ECHO, D1–D5 (diody), BUZZER.
2. **Inicjalizacja OLED** – ustawienie interfejsu SPI, rozdzielczości, czcionki.
3. **Pomiar odległości** – funkcje `signal()` i `oczekiwanie_na_echo()` generują impuls oraz mierzą czas przelotu.
4. **Sterowanie LED** – w zależności od wartości odległości zapalane są 0–5 diod.
5. **Buzzer** – aktywowany, gdy dystans jest mniejszy niż 4 cm.
6. **OLED** – wynik pomiaru (w cm) wyświetlany jest na ekranie.

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
Funkcja `odleglosc()` inicjuje pomiar, a następnie na podstawie czasu przelotu fali dźwiękowej oblicza odległość w centymetrach. Wzór uwzględnia prędkość dźwięku w powietrzu (34300 cm/s).

---

### Sterowanie diodami LED
```python
def kontrola_diod(dystans):
    # Zapala odpowiednią liczbę diod w zależności od dystansu
```
W zależności od zmierzonej odległości funkcja włącza od 0 do 5 diod. Im mniejsza odległość, tym więcej diod się zapala.

Próg działania:
- < 5.3 cm → 5 diod
- < 7 cm → 4 diody
- < 11 cm → 3 diody
- < 15 cm → 2 diody
- < 20 cm → 1 dioda
- ≥ 20 cm → 0 diod

---

### Sterowanie buzzerem
```python
def kontrola_buzzera(dystans):
    if dystans < 4:
        GPIO.output(BUZZER, GPIO.HIGH)
    else:
        GPIO.output(BUZZER, GPIO.LOW)
```
Buzzer włącza się, gdy odległość spadnie poniżej 4 cm. W przeciwnym wypadku pozostaje wyłączony.

---

### Wyświetlanie na ekranie OLED
```python
def pokaz_na_ekranie(tekst):
    # Wyświetla tekst na ekranie OLED
```
Rysuje tekst (np. "12.4 cm" albo "Brak odczytu") na ekranie OLED za pomocą biblioteki PIL. Tekst wyświetlany jest w rozdzielczości 128x64 piksele.

---

### Pętla główna
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
Program działa w nieskończonej pętli. Co sekundę wykonuje pomiar, aktualizuje diody, buzzer i ekran. `KeyboardInterrupt` kończy program i zwalnia zasoby GPIO.

## Uruchomienie

Po zainstalowaniu wszystkich potrzebnych bibliotek i odpowiednim podłączeniu wszystkich elementów należy uruchomić plik `Ekranodl.py`:

```bash
python3 Ekranodl.py
```

