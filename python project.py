import re
import matplotlib.pyplot as plt
import datetime


def ile_dni(poczatek, koniec):
    poczatek_t = (re.split('[-]+', poczatek))
    koniec_t = (re.split('[-]+', koniec))
    a = datetime.date(int(poczatek_t[0]), int(poczatek_t[1]), int(poczatek_t[2]))
    b = datetime.date(int(koniec_t[0]), int(koniec_t[1]), int(koniec_t[2]))
    return (b - a).days


def PoprawnoscDanych(data_p, data_k):
    data_p1 = (re.split('[-]+', data_p))
    data_k1 = (re.split('[-]+', data_k))
    d1 = datetime.datetime(int(data_p1[0]), int(data_p1[1]), int(data_p1[2]))
    d2 = datetime.datetime(int(data_k1[0]), int(data_k1[1]), int(data_k1[2]))
    if (d1 > d2):
        print("Początek musi być mniejszy niż koniec!!!")
        return False
    else:
        dni = ile_dni(data_p, data_k)
        if (dni > 367):
            print("Za długi zakres dni. Wybierz zakres do roku.")
            return False
        elif (dni > 0):
            return True
    return False


def plotHistogram(x_axis, y_axis, title=""):
    t = []
    for i in range(len(x_axis)):
        t.append(i)
    plt.bar(t, y_axis, tick_label=' ')
    y_axis_min = min(y_axis)
    y_axis_max = max(y_axis)
    plt.xlim([min(t), max(t)])
    plt.ylim(y_axis_min - (y_axis_min * 0.02), y_axis_max + (y_axis_max * 0.01), 2)
    plt.title(title)
    plt.grid()
    plt.ylabel("Ceny")
    plt.show()


def wykres(kod_waluty, poczatek, koniec):
    url = "http://api.nbp.pl/api/exchangerates/rates/a/"
    zapytanie = url + kod_waluty + "/" + poczatek + "/" + koniec

    response = requests.get(zapytanie)
    print(zapytanie)
    ile_dni = len(re.findall('(?=mid)', str(response.json()['rates'])))
    x = []
    y = []
    for i in range(0, ile_dni):
        y.append(response.json()['rates'][i]['mid'])
        x.append(response.json()['rates'][i]['effectiveDate'])
    tytul = "Kursy waluty " + kod_waluty + " w dniach od " + poczatek + " do " + koniec
    plotHistogram(x, y, tytul)

def KursyWalut():
    url = "http://api.nbp.pl/api/exchangerates/tables/a/?format=json"
    response = requests.get(url)
    if (response.status_code == 200):
        ilosc_walut = len(re.findall('(?=code)', str(response.json())))
        for i in range(0, ilosc_walut):
            print((response.json()[0]['rates'][i]['currency']) + ': ' + str(
                response.json()[0]['rates'][i]['mid']) + ' ' + str(response.json()[0]['rates'][i]['code']))



import json
import requests


def Przeliczanie(kod_wymiany, kod_waluty, wejsciowa_waluta, ilosc):
    url = "http://api.nbp.pl/api/exchangerates/rates/c/"
    url_2 = "/today/?format=json"
    zapytanie = url + kod_waluty + url_2
    response = requests.get(zapytanie)
    if (response.status_code == 200):
        cena = response.json()['rates'][0][kod_wymiany]
        if (kod_wymiany == "bid"):  # sprzedaż waluty
            if (wejsciowa_waluta == 'zl'):
                wynik = ilosc / cena
                print("Żeby otrzymać " + str(ilosc) + " zł" + " musisz sprzedać " + str(
                    round(wynik, 4)) + " " + kod_waluty)
            elif (wejsciowa_waluta == 'obca'):
                wynik = ilosc * cena
                print("Za sprzedaż " + str(ilosc) + " " + kod_waluty + " otrzymasz " + str(round(wynik, 4)) + " zł")
        if (kod_wymiany == "ask"):  # kupno waluty
            if (wejsciowa_waluta == 'zl'):
                wynik = ilosc / cena
                print("Sprzedając " + str(ilosc) + " zł" + " otrzymasz " + str(round(wynik, 4)) + " " + kod_waluty)
            elif (wejsciowa_waluta == 'obca'):
                wynik = ilosc * cena
                print("Jeśli chcesz kupić " + str(ilosc) + " " + kod_waluty + " musisz zapłacić " + str(
                    round(wynik, 4)) + " zł")
    else:
        print("Error")


menu_glowne = '''Menu główne:
1. Chcę kupić walutę obcą
2. Chcę sprzedać walutę obcą
3. Rysowanie wykresów kursu walut dla 1-365 dni
4. Pokaż kursy wszystkich walut
5. Wyjście'''
menu_waluty = '''Wybierz numer waluty obcej:
1. Dolar amerykański : USD
2. Jen : JPY
3. Funt szterling : GBP
4. Korona czeska : CZK
5. Euro : EUR
6. Forint : HUF
7. Frank szwajcarski : CHF
8. Powrót do menu głównego
9. Wyjście
'''
menu_wejscia = '''Wybierz walute wejściową:
1. Złotówki
2. Waluta obca
3. Powrót do menu głównego
4. Wyjście'''


def WyborWaluty():
    print(menu_waluty)
    wybor = input()
    wybor = int(wybor)
    wybory = {1: 'USD', 2: 'JPY', 3: 'GBP', 4: 'CZK', 5: 'EUR', 6: 'HUF', 7: 'CHF', 8: 'menu', 9: 'wyjscie'}
    wynik = wybory.get(wybor, 'error')
    return wynik


def WalutaWejsciowa():
    print(menu_wejscia)
    wybor = input()
    wybor = int(wybor)
    wybory = {1: 'zl', 2: 'obca', 3: 'menu', 4: 'wyjscie'}
    wynik = wybory.get(wybor, 'error')
    return wynik


i = 1
while (i > 0):
    print(menu_glowne)
    wybor1 = input()
    if (wybor1 == '1'):  ###sprzedaż
        kod_wymiany = 'ask'
        nazwa_waluty = WyborWaluty()
        if (nazwa_waluty == 'wyjscie'):
            i = -1
        elif (nazwa_waluty == 'error'):
            print("Niepoprawny wybor. Sprobuj jeszcze raz")
        else:
            wejsciowa_waluta = WalutaWejsciowa()
            if (wejsciowa_waluta == 'wyjscie'):
                i = -1
            elif (wejsciowa_waluta == 'error'):
                print("Niepoprawny wybor. Sprobuj jeszcze raz")
            else:
                print("Podaj kwotę: ")
                ilosc = float(input())
                # URUCHOMIENIE FUNKCJI KURSU --- kod_wymiany=ask, nazwa_waluty=kod, wejsciowa_waluta =zl/obca, ilosc
                Przeliczanie(kod_wymiany, nazwa_waluty, wejsciowa_waluta, ilosc)
    elif (wybor1 == '2'):  ###kupno
        kod_wymiany = 'bid'
        nazwa_waluty = WyborWaluty()
        if (nazwa_waluty == 'wyjscie'):
            i = -1
        elif (nazwa_waluty == 'error'):
            print("Niepoprawny wybor. Sprobuj jeszcze raz")
        else:
            wejsciowa_waluta = WalutaWejsciowa()
            if (wejsciowa_waluta == 'wyjscie'):
                i = -1
            elif (wejsciowa_waluta == 'error'):
                print("Niepoprawny wybor. Sprobuj jeszcze raz")
            else:
                print("Podaj kwotę: ")
                ilosc = float(input())
                # URUCHOMIENIE FUNKCJI KURSU --- kod_wymiany=bid, nazwa_waluty=kod, wejsciowa_waluta =zl/obca, ilosc
                Przeliczanie(kod_wymiany, nazwa_waluty, wejsciowa_waluta, ilosc)
    elif (wybor1 == '3'):  ### wykresy
        y = 1
        while (y > 0):
            print("Podaj daty w formacie YYYY-MM-DD!!!")
            print("Podaj datę początkową: ")
            data_p = input()
            print("Podaj datę końcową: ")
            data_k = input()
            odp = PoprawnoscDanych(data_p, data_k)
            if (odp == True):
                y = 0
                nazwa_waluty = WyborWaluty()
                if (nazwa_waluty == 'wyjscie'):
                    i = -1
                elif (nazwa_waluty == 'error'):
                    print("Niepoprawny wybor. Sprobuj jeszcze raz")
                else:
                    wykres(nazwa_waluty, data_p, data_k)
    elif (wybor1 == '4'):
        KursyWalut()
    elif (wybor1 == '5'):  ### wyjście
        i = -1
    else:
        print("Niepoprawny wybor. Sprobuj jeszcze raz")
