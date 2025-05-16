import sqlite3
import os
from ttkbootstrap.constants import *
from ttkbootstrap import Button, Label, Entry, Toplevel, Frame, Combobox
from ttkbootstrap.widgets import Meter
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as tb
from fpdf import FPDF
import plotly.graph_objects as go


# --- ADATBÁZIS LÉTREHOZÁSA ---
conn = sqlite3.connect("mozi.db")
c = conn.cursor()

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

c.execute("SELECT COUNT(*) FROM termek")
if c.fetchone()[0] == 0:
    c.execute("INSERT INTO termek VALUES (1, 'Horror Express', 1972, 'Horror', 94, 10)")
    c.execute("INSERT INTO termek VALUES (2, 'Toy Story', 1995, 'Animáció', 81, 12)")
    c.execute("INSERT INTO termek VALUES (3, 'Mamma Mia!', 2008, 'Musical', 108, 15)")
    c.execute("INSERT INTO termek VALUES (4, 'Csizmás a kandúr', 2011, 'Családi', 90, 14)")
    conn.commit()

conn.close()

app = tb.Window(themename="superhero")
app.title("Mozi Jegyfoglalás")
app.geometry("1200x800")

Label(app, text="\U0001F3AC Műsoron lévő filmek", font=("Arial", 24)).pack(pady=20)
frame = Frame(app)
frame.pack()

conn = sqlite3.connect("mozi.db")
c = conn.cursor()
c.execute("SELECT * FROM termek")
filmek = c.fetchall()
conn.close()

def generate_pdf(nev, foglalasok):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Mozi Jegy - {nev}", ln=True, align="C")
    pdf.ln(10)
    for f in foglalasok:
        pdf.cell(200, 10, txt=f"Terem: {f[0]}, Szék: {f[1]}, Jegytípus: {f[2]}", ln=True)
    file_name = f"{nev.replace(' ', '_')}_jegyek.pdf"
    pdf.output(file_name)

def film_kartya(film, index):
    terem_szam, cim, ev, mufaj, jatekido, kapacitas = film
    kep_path = f"film{terem_szam}.jpg"
    img = Image.open(kep_path).resize((200, 300)) if os.path.exists(kep_path) else Image.new('RGB', (200, 300), color='gray')
    tk_kep = ImageTk.PhotoImage(img)
    panel = Label(frame, image=tk_kep)
    panel.image = tk_kep
    panel.grid(row=0, column=index, padx=20)
    Label(frame, text=cim, font=("Arial", 14)).grid(row=1, column=index)
    Button(frame, text="Leírás", bootstyle="info", command=lambda: leiras_ablak(film)).grid(row=2, column=index, pady=5)
    Button(frame, text="Foglalás", bootstyle="success", command=lambda: foglalas_ablak(film)).grid(row=3, column=index, pady=5)

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

def foglalas_ablak(film):
    terem_szam, cim, ev, mufaj, jatekido, kapacitas = film
    fog_win = Toplevel(app)
    fog_win.title("Foglalás")
    Label(fog_win, text=f"Film: {cim}", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)
    Label(fog_win, text="Vezetéknév").grid(row=1, column=0, sticky=W, padx=10)
    Label(fog_win, text="Keresztnév").grid(row=2, column=0, sticky=W, padx=10)
    Label(fog_win, text="Kiinduló Székszám").grid(row=3, column=0, sticky=W, padx=10)
    Label(fog_win, text="Jegytípus").grid(row=4, column=0, sticky=W, padx=10)
    Label(fog_win, text="Jegyek száma").grid(row=5, column=0, sticky=W, padx=10)
    vnev, knev, szek, tipus, jegy_szam = Entry(fog_win), Entry(fog_win), Entry(fog_win), Combobox(fog_win, values=["Normál", "Diák", "Nyugdíjas"]), Entry(fog_win)
    vnev.grid(row=1, column=1); knev.grid(row=2, column=1); szek.grid(row=3, column=1); tipus.grid(row=4, column=1); jegy_szam.grid(row=5, column=1)
    conn = sqlite3.connect("mozi.db")
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM foglalasok WHERE terem_szam = ?", (terem_szam,))
    foglalt = c.fetchone()[0]
    c.execute("SELECT kapacitas FROM termek WHERE terem_szam = ?", (terem_szam,))
    kapacitas = c.fetchone()[0]
    conn.close()

    szazalek = round((foglalt / kapacitas) * 100) if kapacitas else 0

    # Szín meghatározása
    if szazalek > 90:
        szin = "danger"
    elif szazalek < 40:
        szin = "success"
    else:
        szin = "warning"

    meter = Meter(fog_win,
                bootstyle=szin,
                subtext="Foglaltság",
                interactive=False,
                textright="%",
                amountused=szazalek,
                amounttotal=100)
    meter.grid(row=6, column=0, columnspan=2, pady=20)

    def mentes():
        try:
            kezdoszek = int(szek.get())
            darab = int(jegy_szam.get())
        except:
            messagebox.showerror("Hiba", "Székszám és jegyszám legyen szám!")
            return
        conn = sqlite3.connect("mozi.db"); c = conn.cursor()
        c.execute("SELECT szek_szam FROM foglalasok WHERE terem_szam = ?", (terem_szam,))
        foglaltak = {s[0] for s in c.fetchall()}
        c.execute("SELECT kapacitas FROM termek WHERE terem_szam = ?", (terem_szam,))
        kap = c.fetchone()[0]
        sikeres = 0
        for i in range(darab):
            aktualis_szek = kezdoszek + i
            if aktualis_szek in foglaltak or aktualis_szek > kap:
                continue
            c.execute("INSERT INTO foglalasok (vezeteknev, keresztnev, terem_szam, szek_szam, jegytipus) VALUES (?, ?, ?, ?, ?)",
                      (vnev.get(), knev.get(), terem_szam, aktualis_szek, tipus.get()))
            sikeres += 1
        conn.commit()
        c.execute("SELECT terem_szam, szek_szam, jegytipus FROM foglalasok WHERE vezeteknev=? AND keresztnev=? ORDER BY id DESC LIMIT ?", 
                  (vnev.get(), knev.get(), darab))
        pdf_foglalasok = c.fetchall()
        conn.close()
        generate_pdf(f"{vnev.get()} {knev.get()}", pdf_foglalasok)
        messagebox.showinfo("Eredmény", f"{sikeres} jegyet sikeresen lefoglaltunk.")
        fog_win.destroy()

    Button(fog_win, text="Foglalás rögzítése", command=mentes, bootstyle="success").grid(row=7, column=0, columnspan=2, pady=20)

def torles_ablak():
    top = Toplevel(app)
    top.title("Foglalás törlése")
    Label(top, text="Foglalási azonosító:").pack(pady=10)
    id_entry = Entry(top); id_entry.pack()
    def torol():
        conn = sqlite3.connect("mozi.db")
        c = conn.cursor()
        c.execute("DELETE FROM foglalasok WHERE id=?", (id_entry.get(),))
        conn.commit(); conn.close()
        messagebox.showinfo("Törlés", "Foglalás törölve.")
        top.destroy()
    Button(top, text="Törlés", command=torol, bootstyle="danger").pack(pady=10)

def statisztika():
    conn = sqlite3.connect("mozi.db")
    c = conn.cursor()
    c.execute("SELECT terem_szam, kapacitas FROM termek")
    termek = {row[0]: row[1] for row in c.fetchall()}
    c.execute("SELECT terem_szam, COUNT(*) FROM foglalasok GROUP BY terem_szam")
    foglaltsag = {row[0]: row[1] for row in c.fetchall()}
    conn.close()
    labels, values = [], []
    for terem, kap in termek.items():
        foglalt = foglaltsag.get(terem, 0)
        labels.append(f"Terem {terem}")
        values.append((foglalt / kap) * 100)
    fig = go.Figure([go.Bar(x=labels, y=values)])
    fig.update_layout(title="Foglaltsági százalék termenként", yaxis_title="Foglaltság (%)")
    fig.show()

for i, film in enumerate(filmek):
    film_kartya(film, i)

Button(app, text="Foglalás törlése", command=torles_ablak, bootstyle="danger").pack(pady=10)
Button(app, text="Statisztika", command=statisztika, bootstyle="info").pack(pady=10)
app.mainloop()
