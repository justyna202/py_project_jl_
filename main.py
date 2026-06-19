import tkinter as tk
from tkinter import messagebox, simpledialog
import tkintermapview

from notatnik import LOGIN, HASLO, firmy, klienci, pracownicy, zwierzeta
from kontroler import (
    sprawdz_logowanie,
    pobierz_wspolrzedne,
    opis_firmy,
    opis_klienta,
    opis_pracownika,
    opis_zwierzecia,
    klienci_firmy,
    pracownicy_firmy,
    zwierzeta_pracownika,
)

class AplikacjaWeterynaryjna:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.geometry("1200x900")
        self.root.title("System zarządzania klinikami weterynaryjnymi")

        self.wybrany_typ = "firmy"
        self.wybrana_firma = None
        self.wybrany_pracownik = None
        self.aktualna_lista = []

        self.zbuduj_logowanie()
        self.root.mainloop()

    def wyczysc_okno(self) -> None:
        for widget in self.root.winfo_children():
            widget.destroy()

    def zbuduj_logowanie(self) -> None:
        self.wyczysc_okno()

        ramka = tk.Frame(self.root, padx=40, pady=40)
        ramka.pack(expand=True)

        tk.Label(ramka, text="Logowanie", font=("Arial", 22, "bold")).grid(row=0, column=0, columnspan=2, pady=15)

        tk.Label(ramka, text="Login:").grid(row=1, column=0, sticky="e", pady=5)
        self.login_entry = tk.Entry(ramka, width=30)
        self.login_entry.grid(row=1, column=1, pady=5)

        tk.Label(ramka, text="Hasło:").grid(row=2, column=0, sticky="e", pady=5)
        self.haslo_entry = tk.Entry(ramka, width=30, show="*")
        self.haslo_entry.grid(row=2, column=1, pady=5)

        tk.Button(ramka, text="Zaloguj", width=20, command=self.zaloguj).grid(row=3, column=0, columnspan=2, pady=20)

    def zaloguj(self) -> None:
        login = self.login_entry.get()
        haslo = self.haslo_entry.get()

        if sprawdz_logowanie(login, haslo, LOGIN, HASLO):
            self.zbuduj_aplikacje()
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy login albo hasło")


    def zbuduj_aplikacje(self) -> None:
        self.wyczysc_okno()

        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=3)

        menu = tk.Frame(self.root, padx=10, pady=10)
        menu.grid(row=0, column=0, sticky="ns")

        tk.Label(menu, text="Menu", font=("Times New Roma", 13, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

        lewa_kolumna = [
            ("Firmy", lambda: self.pokaz_liste("firmy")),
            ("Klienci", lambda: self.pokaz_liste("klienci")),
            ("Pracownicy", lambda: self.pokaz_liste("pracownicy")),
            ("Zwierzęta", lambda: self.pokaz_liste("zwierzeta")),
        ]

        prawa_kolumna = [
            ("Klienci wybranej firmy", self.pokaz_klientow_wybranej_firmy),
            ("Pracownicy wybranej firmy", self.pokaz_pracownikow_wybranej_firmy),
            ("Zwierzęta pracownika", self.pokaz_zwierzeta_wybranego_pracownika),
        ]

        for i, (tekst, komenda) in enumerate(lewa_kolumna, start=1):
            tk.Button(menu, text=tekst, width=24, height=2, command=komenda).grid(row=i, column=0, padx=4, pady=4)

        for i, (tekst, komenda) in enumerate(prawa_kolumna, start=1):
            tk.Button(menu, text=tekst, width=28, height=2, command=komenda).grid(row=i, column=1, padx=4, pady=4)

        akcje = tk.Frame(self.root, padx=10, pady=5)
        akcje.grid(row=0, column=1, sticky="nsew")
        akcje.grid_columnconfigure(0, weight=1)

        self.tytul_listy = tk.Label(akcje, text="Firmy", font=("Arial", 14, "bold"))
        self.tytul_listy.grid(row=0, column=0, pady=5)

        self.lista = tk.Listbox(akcje, height=14, font=("Arial", 11))
        self.lista.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.lista.bind("<<ListboxSelect>>", self.po_wybraniu_elementu)

        przyciski = tk.Frame(akcje)
        przyciski.grid(row=2, column=0, pady=6)

        tk.Button(przyciski, text="Dodaj", width=14, command=self.dodaj).grid(row=0, column=0, padx=5)
        tk.Button(przyciski, text="Edytuj", width=14, command=self.edytuj).grid(row=0, column=1, padx=5)
        tk.Button(przyciski, text="Usuń", width=14, command=self.usun).grid(row=0, column=2, padx=5)

        self.mapa = tkintermapview.TkinterMapView(self.root, width=1150, height=520, corner_radius=0)
        self.mapa.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.mapa.set_position(52.0, 19.0)
        self.mapa.set_zoom(6)

        self.pokaz_liste("firmy")

    def pokaz_liste(self, typ: str) -> None:
        self.wybrany_typ = typ

        if typ == "firmy":
            self.aktualna_lista = firmy
            self.tytul_listy.config(text="Firmy")
            opisy = [opis_firmy(firma) for firma in firmy]
        elif typ == "klienci":
            self.aktualna_lista = klienci
            self.tytul_listy.config(text="Klienci")
            opisy = [opis_klienta(klient) for klient in klienci]
        elif typ == "pracownicy":
            self.aktualna_lista = pracownicy
            self.tytul_listy.config(text="Pracownicy")
            opisy = [opis_pracownika(pracownik) for pracownik in pracownicy]
        else:
            self.aktualna_lista = zwierzeta
            self.tytul_listy.config(text="Zwierzęta")
            opisy = [opis_zwierzecia(zwierze) for zwierze in zwierzeta]

        self.uzupelnij_liste(opisy)
        self.odswiez_mape()

    def uzupelnij_liste(self, opisy: list[str]) -> None:
        self.lista.delete(0, tk.END)
        for opis in opisy:
            self.lista.insert(tk.END, opis)

    def po_wybraniu_elementu(self, event=None) -> None:
        indeksy = self.lista.curselection()
        if not indeksy:
            return

        element = self.aktualna_lista[indeksy[0]]

        if "nazwa" in element:
            self.wybrana_firma = element["nazwa"]
        if "stanowisko" in element:
            self.wybrany_pracownik = element["imie_nazwisko"]

    def pokaz_klientow_wybranej_firmy(self) -> None:
        if not self.wybrana_firma:
            return
        lista = klienci_firmy(klienci, self.wybrana_firma)
        self.wybrany_typ = "klienci_firmy"
        self.aktualna_lista = lista
        self.tytul_listy.config(text=f"Klienci firmy: {self.wybrana_firma}")
        self.uzupelnij_liste([opis_klienta(klient) for klient in lista])
        self.odswiez_mape(lista)

    def pokaz_pracownikow_wybranej_firmy(self) -> None:
        if not self.wybrana_firma:
            return
        lista = pracownicy_firmy(pracownicy, self.wybrana_firma)
        self.wybrany_typ = "pracownicy_firmy"
        self.aktualna_lista = lista
        self.tytul_listy.config(text=f"Pracownicy firmy: {self.wybrana_firma}")
        self.uzupelnij_liste([opis_pracownika(pracownik) for pracownik in lista])
        self.odswiez_mape(lista)

    def pokaz_zwierzeta_wybranego_pracownika(self) -> None:
        if not self.wybrany_pracownik:
            return
        lista = zwierzeta_pracownika(zwierzeta, self.wybrany_pracownik)
        self.wybrany_typ = "zwierzeta_pracownika"
        self.aktualna_lista = lista
        self.tytul_listy.config(text=f"Zwierzęta pracownika: {self.wybrany_pracownik}")
        self.uzupelnij_liste([opis_zwierzecia(zwierze) for zwierze in lista])
        self.odswiez_mape()

    def pobierz_zaznaczony(self):
        indeksy = self.lista.curselection()
        if not indeksy:
            return None
        return self.aktualna_lista[indeksy[0]]


    def formularz(self, tytul: str, pola: list[str], dane: dict | None = None) -> dict | None:
        okno = tk.Toplevel(self.root)
        okno.geometry("420x360")
        okno.grab_set()

        wpisy = {}
        for i, pole in enumerate(pola):
            tk.Label(okno, text=pole).grid(row=i, column=0, sticky="e", padx=10, pady=7)
            entry = tk.Entry(okno, width=32)
            entry.grid(row=i, column=1, padx=10, pady=7)
            if dane and pole in dane:
                entry.insert(0, dane[pole])
            wpisy[pole] = entry

        wynik = {"dane": None}

        def zapisz():
            wynik["dane"] = {pole: wpisy[pole].get().strip() for pole in pola}
            okno.destroy()

        tk.Button(okno, text="Zapisz", width=14, command=zapisz).grid(row=len(pola), column=0, columnspan=2, pady=18)
        self.root.wait_window(okno)
        return wynik["dane"]

    def dodaj(self) -> None:
        if self.wybrany_typ in ["firmy"]:
            dane = self.formularz("Dodaj firmę", ["nazwa", "miejscowosc", "ulica"])
            if dane:
                dane["lat"], dane["lon"] = pobierz_wspolrzedne(dane["miejscowosc"], dane["ulica"])
                firmy.append(dane)
                self.pokaz_liste("firmy")

        elif self.wybrany_typ in ["klienci", "klienci_firmy"]:
            start = {"firma": self.wybrana_firma} if self.wybrana_firma else None
            dane = self.formularz("Dodaj klienta", ["imie_nazwisko", "firma", "miejscowosc", "ulica"], start)
            if dane:
                dane["lat"], dane["lon"] = pobierz_wspolrzedne(dane["miejscowosc"], dane["ulica"])
                klienci.append(dane)
                self.pokaz_liste("klienci")

        elif self.wybrany_typ in ["pracownicy", "pracownicy_firmy"]:
            start = {"firma": self.wybrana_firma} if self.wybrana_firma else None
            dane = self.formularz("Dodaj pracownika", ["imie_nazwisko", "firma", "stanowisko", "miejscowosc", "ulica"], start)
            if dane:
                dane["lat"], dane["lon"] = pobierz_wspolrzedne(dane["miejscowosc"], dane["ulica"])
                pracownicy.append(dane)
                self.pokaz_liste("pracownicy")

        else:
            dane = self.formularz("Dodaj zwierzę", ["nazwa", "gatunek", "wlasciciel", "pracownik"])
            if dane:
                zwierzeta.append(dane)
                self.pokaz_liste("zwierzeta")

    def edytuj(self) -> None:
        element = self.pobierz_zaznaczony()
        if not element:
            return

        if self.wybrany_typ in ["firmy"]:
            dane = self.formularz("Edytuj firmę", ["nazwa", "miejscowosc", "ulica"], element)
            if dane:
                stara_nazwa = element["nazwa"]
                dane["lat"], dane["lon"] = pobierz_wspolrzedne(dane["miejscowosc"], dane["ulica"])
                element.update(dane)
                for klient in klienci:
                    if klient["firma"] == stara_nazwa:
                        klient["firma"] = dane["nazwa"]
                for pracownik in pracownicy:
                    if pracownik["firma"] == stara_nazwa:
                        pracownik["firma"] = dane["nazwa"]
                self.pokaz_liste("firmy")

        elif self.wybrany_typ in ["klienci", "klienci_firmy"]:
            dane = self.formularz("Edytuj klienta", ["imie_nazwisko", "firma", "miejscowosc", "ulica"], element)
            if dane:
                stare_imie = element["imie_nazwisko"]
                dane["lat"], dane["lon"] = pobierz_wspolrzedne(dane["miejscowosc"], dane["ulica"])
                element.update(dane)
                for zwierze in zwierzeta:
                    if zwierze["wlasciciel"] == stare_imie:
                        zwierze["wlasciciel"] = dane["imie_nazwisko"]
                self.pokaz_liste("klienci")

        elif self.wybrany_typ in ["pracownicy", "pracownicy_firmy"]:
            dane = self.formularz("Edytuj pracownika", ["imie_nazwisko", "firma", "stanowisko", "miejscowosc", "ulica"], element)
            if dane:
                stare_imie = element["imie_nazwisko"]
                dane["lat"], dane["lon"] = pobierz_wspolrzedne(dane["miejscowosc"], dane["ulica"])
                element.update(dane)
                for zwierze in zwierzeta:
                    if zwierze["pracownik"] == stare_imie:
                        zwierze["pracownik"] = dane["imie_nazwisko"]
                self.pokaz_liste("pracownicy")

        else:
            dane = self.formularz("Edytuj zwierzę", ["nazwa", "gatunek", "wlasciciel", "pracownik"], element)
            if dane:
                element.update(dane)
                self.pokaz_liste("zwierzeta")

    def usun(self) -> None:
        element = self.pobierz_zaznaczony()
        if not element:
            return

        if self.wybrany_typ == "firmy":
            firmy.remove(element)
            self.pokaz_liste("firmy")
        elif self.wybrany_typ in ["klienci", "klienci_firmy"]:
            klienci.remove(element)
            self.pokaz_liste("klienci")
        elif self.wybrany_typ in ["pracownicy", "pracownicy_firmy"]:
            pracownicy.remove(element)
            self.pokaz_liste("pracownicy")
        else:
            zwierzeta.remove(element)
            self.pokaz_liste("zwierzeta")

    def odswiez_mape(self, lista_punktow: list | None = None) -> None:
        self.mapa.delete_all_marker()
        punkty = lista_punktow if lista_punktow is not None else firmy + klienci + pracownicy

        for punkt in punkty:
            if punkt.get("lat") is not None and punkt.get("lon") is not None:
                nazwa = punkt.get("nazwa") or punkt.get("imie_nazwisko") or "punkt"
                adres = f"{punkt.get('miejscowosc', '')}, {punkt.get('ulica', '')}"
                self.mapa.set_marker(punkt["lat"], punkt["lon"], text=f"{nazwa}")

        if punkty:
            pierwszy = next((p for p in punkty if p.get("lat") is not None and p.get("lon") is not None), None)
            if pierwszy:
                self.mapa.set_position(pierwszy["lat"], pierwszy["lon"])


if __name__ == "__main__":
    AplikacjaWeterynaryjna()


