import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/50.0.2661.102 Safari/537.36"}

def sprawdz_logowanie(login: str, haslo: str, poprawny_login: str, poprawne_haslo: str) -> bool:
    return login == poprawny_login and haslo == poprawne_haslo

def przygotuj_adres(miejscowosc: str, ulica: str = "") -> str:
    miejscowosc = miejscowosc.strip()
    ulica = ulica.strip()
    if miejscowosc and ulica:
        return f"{ulica}, {miejscowosc}, Polska"
    if miejscowosc:
        return f"{miejscowosc}, Polska"
    return "Polska"

def _tekst_na_float(tekst: str) -> float:
    tekst = tekst.strip().replace(",", ".")
    tekst = re.sub(r"[^0-9.\-]", "", tekst)
    return float(tekst)

def pobierz_wspolrzedne(miejscowosc: str, ulica: str = "") -> tuple[float | None, float | None]:
    adres = przygotuj_adres(miejscowosc, ulica)
    try:
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": adres,
                "format": "json",
                "limit": 1,
                "addressdetails": 1,
            },
            headers=HEADERS,
            timeout=10,
        )
        response.raise_for_status()
        dane = response.json()
        if dane:
            return round(float(dane[0]["lat"]), 6), round(float(dane[0]["lon"]), 6)
    except Exception:
        pass

    try:
        miejscowosc_url = miejscowosc.strip().replace(" ", "_")
        url = f"https://pl.wikipedia.org/wiki/{miejscowosc_url}"
        response = requests.get(url, headers=HEADERS, timeout=8)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        latitude = soup.select(".latitude")
        longitude = soup.select(".longitude")

        if latitude and longitude:
            lat = _tekst_na_float(latitude[0].text)
            lon = _tekst_na_float(longitude[0].text)
            return round(lat, 6), round(lon, 6)
    except Exception:
        pass

    return None, None

def opis_firmy(firma: dict) -> str:
    return f"{firma['nazwa']} | {firma['miejscowosc']}, {firma['ulica']}"

def opis_klienta(klient: dict) -> str:
    return f"{klient['imie_nazwisko']} | firma: {klient['firma']} | {klient['miejscowosc']}, {klient['ulica']}"

def opis_pracownika(pracownik: dict) -> str:
    return f"{pracownik['imie_nazwisko']} | {pracownik['stanowisko']} | firma: {pracownik['firma']} | {pracownik['miejscowosc']}, {pracownik['ulica']}"

def opis_zwierzecia(zwierze: dict) -> str:
    return f"{zwierze['nazwa']} | {zwierze['gatunek']} | właściciel: {zwierze['wlasciciel']} | opiekun: {zwierze['pracownik']}"

def klienci_firmy(klienci: list, nazwa_firmy: str) -> list:
    return [klient for klient in klienci if klient["firma"] == nazwa_firmy]

def pracownicy_firmy(pracownicy: list, nazwa_firmy: str) -> list:
    return [pracownik for pracownik in pracownicy if pracownik["firma"] == nazwa_firmy]

def zwierzeta_pracownika(zwierzeta: list, imie_nazwisko_pracownika: str) -> list:
    return [zwierze for zwierze in zwierzeta if zwierze["pracownik"] == imie_nazwisko_pracownika]

