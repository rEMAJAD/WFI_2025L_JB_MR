# System pomiaru odległości na Raspberry Pi z OLED, diodami LED i buzzerem

## Opis projektu
Ten projekt to prosty system pomiaru odległości z użyciem Raspberry Pi, czujnika ultradźwiękowego (HC-SR04), wyświetlacza OLED SSD1306, pięciu diod LED oraz buzzera. Odległość mierzona jest w czasie rzeczywistym i prezentowana na ekranie OLED, a LED-y i buzzer pełnią funkcję sygnalizacji wizualnej i dźwiękowej.

## Funkcje
- Pomiar odległości z wykorzystaniem czujnika HC-SR04
- Wyświetlanie aktualnej odległości na ekranie OLED
- Sygnalizacja odległości za pomocą 5 diod LED
- Aktywacja buzzera przy bardzo małych odległościach (poniżej 4 cm)


## Struktura kodu

### Pomiar odległości
```python
def signal():
    GPIO.output(TRIG, GPIO.LOW)
    time.sleep(0.05)
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(10e-6)
    GPIO.output(TRIG, GPIO.LOW)

def oczekiwanie_na_echo():
    # Oczekiwanie na sygnał ECHO i pomiar czasu przelotu

def odleglosc():
    # Obliczenie odległości na podstawie czasu przelotu
```

### Sterowanie diodami LED
```python
def kontrola_diod(dystans):
    # Zapala odpowiednią ilość diod w zależności od odległości
```

### Sterowanie buzzerem
```python
def kontrola_buzzera(dystans):
    # Włącza buzzer przy dystansie mniejszym niż 4 cm
```

### Wyświetlanie na OLED
```python
def pokaz_na_ekranie(tekst):
    # Rysuje tekst na ekranie OLED z wykorzystaniem PIL
```

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

## Uruchamianie
1. Upewnij się, że wszystkie wymagane biblioteki są zainstalowane.
2. Podłącz komponenty zgodnie ze swoim schematem.
3. Uruchom skrypt:

```bash
python3 main.py
```


## Autor
Jan Bujok
Michał Rempalski

---


