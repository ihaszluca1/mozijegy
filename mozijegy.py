import sqlite3
import os
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as tb

# --- ADATBÁZIS LÉTREHOZÁSA ---
conn = sqlite3.connect("mozi.db")
c = conn.cursor()

# Terem tábla
c.execute('''
CREATE TABLE IF NOT EXISTS termek (
    terem_szam INTEGER PRIMARY KEY,
    film_cim TEXT,
    ev INTEGER,
    mufaj TEXT,
    jatekido INTEGER,
    kapacitas INTEGER
)
''')

# Foglalás tábla
c.execute('''
CREATE TABLE IF NOT EXISTS foglalasok (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vezeteknev TEXT,
    keresztnev TEXT,
    terem_szam INTEGER,
    szek_szam INTEGER,
    jegytipus TEXT,
    FOREIGN KEY (terem_szam) REFERENCES termek (terem_szam)
)
''')

# Dummy filmadatok (ha még nincsenek)
c.execute("SELECT COUNT(*) FROM termek")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO termek VALUES (1, 'Horror Express', 1972, 'Horror', 94, 10)")
    c.execute("INSERT INTO termek VALUES (2, 'Toy Story', 1995, 'Animáció', 81, 12)")
    c.execute("INSERT INTO termek VALUES (3, 'Mamma Mia!', 2008, 'Musical', 108, 15)")
    c.execute("INSERT INTO termek VALUES (4, 'Csizmás a kandúr', 2011, 'Családi', 90, 14)")
    conn.commit()

conn.close()

# --- ALKALMAZÁS ---
app = tb.Window(themename="superhero")
app.title("Mozi Jegyfoglalás")
app.geometry("1200x800")

cim = Label(app, text="🎬 Műsoron lévő filmek", font=("Arial", 24))
cim.pack(pady=20)

frame = Frame(app)
frame.pack()

# Film adatok lekérése adatbázisból
conn = sqlite3.connect("mozi.db")
c = conn.cursor()
c.execute("SELECT * FROM termek")
filmek = c.fetchall()
conn.close()

# --- KÉPEK ÉS GOMBOK MEGJELENÍTÉSE ---
def film_kartya(film, index):
    terem_szam, cim, ev, mufaj, jatekido, kapacitas = film
    kep_path = f"film{terem_szam}.jpg"
    if os.path.exists(kep_path):
        img = Image.open(kep_path).resize((200, 300))
    else:
        img = Image.new('RGB', (200, 300), color='gray')
    tk_kep = ImageTk.PhotoImage(img)

    panel = Label(frame, image=tk_kep)
    panel.image = tk_kep
    panel.grid(row=0, column=index, padx=20)

    cimke = Label(frame, text=cim, font=("Arial", 14))
    cimke.grid(row=1, column=index)

    Button(frame, text="Leírás", bootstyle="info", command=lambda: leiras_ablak(film)).grid(row=2, column=index, pady=5)
    Button(frame, text="Foglalás", bootstyle="success", command=lambda: foglalas_ablak(film)).grid(row=3, column=index, pady=5)

for i, film in enumerate(filmek):
    film_kartya(film, i)

# --- FILM LEÍRÁS ABLAK ---
def leiras_ablak(film):
    terem_szam, cim, ev, mufaj, jatekido, kapacitas = film

    conn = sqlite3.connect("mozi.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM foglalasok WHERE terem_szam = ?", (terem_szam,))
    foglalt = c.fetchone()[0]
    conn.close()

    szabad = kapacitas - foglalt

    top = Toplevel(app)
    top.title(f"{cim} - Leírás")
    Label(top, text=f"Cím: {cim}\nÉv: {ev}\nMűfaj: {mufaj}\nJátékidő: {jatekido} perc\n\nElérhető helyek: {szabad}/{kapacitas}", font=("Arial", 14), justify=LEFT).pack(padx=20, pady=20)

# --- FOGLALÁS ABLAK ---
def foglalas_ablak(film):
    terem_szam, cim, ev, mufaj, jatekido, kapacitas = film

    fog_win = Toplevel(app)
    fog_win.title("Foglalás")

    Label(fog_win, text=f"Film: {cim}", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

    Label(fog_win, text="Vezetéknév").grid(row=1, column=0, sticky=W, padx=10)
    Label(fog_win, text="Keresztnév").grid(row=2, column=0, sticky=W, padx=10)
    Label(fog_win, text="Székszám").grid(row=3, column=0, sticky=W, padx=10)
    Label(fog_win, text="Jegytípus").grid(row=4, column=0, sticky=W, padx=10)

    vnev = Entry(fog_win)
    knev = Entry(fog_win)
    szek = Entry(fog_win)
    tipus = tb.Combobox(fog_win, values=["Normál", "Diák", "Nyugdíjas"])

    vnev.grid(row=1, column=1)
    knev.grid(row=2, column=1)
    szek.grid(row=3, column=1)
    tipus.grid(row=4, column=1)

    def mentes():
        try:
            szek_szam = int(szek.get())
        except:
            messagebox.showerror("Hiba", "Székszám csak szám lehet!")
            return

        conn = sqlite3.connect("mozi.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM foglalasok WHERE terem_szam = ?", (terem_szam,))
        foglalt = c.fetchone()[0]
        c.execute("SELECT kapacitas FROM termek WHERE terem_szam = ?", (terem_szam,))
        kap = c.fetchone()[0]

        if foglalt >= kap:
            messagebox.showwarning("Nincs több hely", "Ez a vetítés megtelt!")
        else:
            c.execute("INSERT INTO foglalasok (vezeteknev, keresztnev, terem_szam, szek_szam, jegytipus) VALUES (?, ?, ?, ?, ?)",
                      (vnev.get(), knev.get(), terem_szam, szek_szam, tipus.get()))
            conn.commit()
            messagebox.showinfo("Siker", "Foglalás sikeres!")
        conn.close()

    Button(fog_win, text="Foglalás rögzítése", command=mentes, bootstyle="success").grid(row=5, column=0, columnspan=2, pady=20)

app.mainloop()
