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

