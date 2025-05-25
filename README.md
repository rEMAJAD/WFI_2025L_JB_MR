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

## Fragmenty kodu i ich opis

### Pomiar odległości

```python
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
```

Funkcje te odpowiadają za wysyłanie sygnału z czujnika oraz odczyt odpowiedzi. Na podstawie czasu przelotu impulsu obliczana jest odległość. Wynik zwracany jest w centymetrach.

---

### Sterowanie diodami LED

```python
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
```

W zależności od zmierzonej odległości funkcja włącza odpowiednią liczbę diod – im bliżej znajduje się obiekt, tym więcej diod zostaje zapalonych.

---

### Sterowanie buzzerem

```python
def kontrola_buzzera(dystans):
    if dystans < 4:
        GPIO.output(BUZZER, GPIO.HIGH)
    else:
        GPIO.output(BUZZER, GPIO.LOW)
```

Buzzer zostaje aktywowany tylko wtedy, gdy zmierzony dystans jest mniejszy niż 4 cm.

---

### Wyświetlanie wyniku na ekranie OLED

```python
def pokaz_na_ekranie(tekst):
    obraz = Image.new("1", oled.size)
    rysuj = ImageDraw.Draw(obraz)
    rysuj.text((0, 20), tekst, font=font, fill=255)
    oled.display(obraz)
```

Funkcja rysuje na ekranie tekst, którym może być wynik pomiaru (np. "12.3 cm") lub informacja o braku odczytu.

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

Program działa w nieskończonej pętli. Co sekundę wykonywany jest nowy pomiar, aktualizowane są diody, buzzer i ekran OLED. Użycie `Ctrl+C` pozwala zakończyć działanie programu – wtedy czyszczone są zasoby GPIO.

## Uruchomienie

Po zainstalowaniu wszystkich potrzebnych bibliotek i odpowiednim podłączeniu wszystkich elementów należy uruchomić plik `Ekranodl.py`:

```bash
python3 Ekranodl.py
```
