from PIL import Image
import random


# suma wartosci natezenia kanalow koloru(czerwony zielony niebieski) pixeli na obszarze 4x4 wokol punktu x,y z jest podzielona przez wartosc ascii znaku kodowanego
# funkcja zwraca kanal ktorego wynik jest najmniejszy
def kolor_check(img_alfa, x_alfa, y_alfa):

    # zmienne int do przechowywania sumy wartosci natezenia kolorow
    total_red, total_green, total_blue = 0, 0, 0

    # petla iterujaca po obszarze 4x4 wokol punktu x,y
    for x in range(x_alfa-2, x_alfa+2):
        for y in range(y_alfa-2, y_alfa+2):

            # aby funckja dzialala tez w dekodowaniu zdjecia nie mozemy sprawdzac
            # pixela 0,0 oraz pixeli kodujacych poniewaz sa zmodyfikowane kodem
            if not (x_alfa == 0 and y_alfa == 0):
                if not (x_alfa == x and y_alfa == y):
                    pixel_value = img_alfa.getpixel((x, y))
                    red, green, blue = pixel_value
                    total_red += red
                    total_green += green
                    total_blue += blue

    # (suma wszystkich wartosci podzielona przez ilosc pixeli sprawdzonych)-wartosc ascii znaku kodowanego
    # zwraca kanal ktorego wynik jest najblizej 100
    if abs((total_red/15)-100) < abs((total_green/15)-100) and abs((total_red/15)-100)-100 < abs((total_blue/15)-100):
        return "red"
    elif abs((total_green/15)-100) < abs((total_red/15)-100) and abs((total_green/15)-100) < abs((total_blue/15)-100):
        return "green"
    elif abs((total_blue/15)-100) < abs((total_red/15)-100) and abs((total_blue/15)-100) < abs((total_green/15)-100):
        return "blue"
    else:
        return 0


# funkcja kodowania
def kodowanie(tekst, img):
    # wyslosowanie poczatkowego polozenia pixela kodujacego
    x = random.randint(0, 4)
    y = random.randint(2, 4)

    # zakodowanie polozenia i dlugosci pozycji startowej bitu kodujacego do skrajnego pixela
    pixel_value = img.getpixel((0, 0))
    red, green, blue = pixel_value
    img.putpixel((0, 0), (x, y, blue))

    # petla do zakodowania tekstu
    for i in range(len(tekst)):
        # przesuniecie pixela kodujacego
        x = x + 16

        # jesli pixel wyjdzie poza szerokosc obrazu to przesuniecie w dol i ustawienie x na poczatek
        if x + 2 > img.width:
            x = x + 2 - img.width
            y = y + 16

        # sprawdzenie na ktorym kanale kodujemy
        kanal = kolor_check(img, x, y)

        pixel_value = img.getpixel((x, y))
        red, green, blue = pixel_value

        # kodowanie
        if kanal == "red":
            red = ord(tekst[i])
        elif kanal == "green":
            green = ord(tekst[i])
        else:
            blue = ord(tekst[i])
        img.putpixel((x, y), (red, green, blue))

    # ustawienie pixela kodujacego na czarny
    x = x + 16

    if x + 2 > img.width:
        x = x + 2 - img.width
        y = y + 16
    img.putpixel((x, y), (0, 0, 0))


# funkcja dekodowania

def dekodowanie(img):
    # string na ktorym bedziemy zapisywac tekst
    decoded_tekst = ""

    # pobieranie polozenia i dlugosci pozycji startowej bitu kodujacego
    pixel_value = img.getpixel((0, 0))
    x, y, blue = pixel_value

    # petla do dekodowania tekstu
    # for i in range(0, dlugosc):
    while True:
        # przesuniecie pixela kodujacego
        x = x + 16
        if x + 2 > img.width:
            x = x + 2 - img.width
            y = y + 16

        # sprawdzenie ktory kanal koduje
        kanal = kolor_check(img, x, y)

        pixel_value = img.getpixel((x, y))
        red, green, blue = pixel_value

        if red == 0 and green == 0 and blue == 0:
            break

        # dopisanie do stringa zdekodowanego znaku
        if kanal == "red":
            decoded_tekst = decoded_tekst + chr(red)
        elif kanal == "green":
            decoded_tekst = decoded_tekst + chr(green)
        else:
            decoded_tekst = decoded_tekst + chr(blue)

    # zwracanie zdekodowanego tekstu
    return decoded_tekst


# petla main
wybor = 0
while wybor != 3:
    print("1. Zakoduj tekst")
    print("2. Dekoduj tekst")
    print("3. Wyjscie")

    # pobranie wyboru
    try:
        wybor = int(input("Wybierz opcje: "))
    except ValueError:
        print("Podaj liczbe")
        wybor = 0

    if wybor == 3:
        break

    # pobranie nazwy zdjecia
    name = input("Podaj nazwe zdjecia: ")

    # otwarcie zdjecia
    with Image.open(f"{name}.png") as img:

        # kodowanie
        if wybor == 1:

            # pobranie dpi zdjecia
            metadata = img.info
            dpi = metadata.get('dpi')

            # pobieranie tekstu od uzytkownika
            tekst = input("Podaj tekst do zakodowania: ")

            # wywołanie funkcji kodowania
            kodowanie(tekst, img)

            # zapis zdjecia
            img.save("image_mod.png", dpi=dpi)

        # dekodowanie
        elif wybor == 2:
            # wywolanie funkcji dekodowania i wypisanie zdekodowanego tekstu
            print('tekst zakodowany w zdjeciu to:')
            decoded_text = dekodowanie(img)
            print(decoded_text.replace("\\n", "\n"))
        else:
            print("Nie ma takiej opcji")
