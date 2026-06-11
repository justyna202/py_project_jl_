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

        tk.Label(menu, text="Menu", font=("Arial", 13, "bold")).grid(row=0, column=0, columnspan=2, pady=5)

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


