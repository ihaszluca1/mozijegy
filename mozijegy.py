from tkinter import *
from PIL import Image, ImageTk
import sqlite3

root = Tk()
root.title("Főoldal")
root.geometry("1000x1000")
root.config(bg="white")


conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        nev TEXT,
        email TEXT,
        iranyszam INTEGER
    )
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS filmek (
        cim TEXT,
        tipus TEXT,
        fimlid INTEGER PRIMARY KEY,
        hosszido TIME,
        vetites DATE
    )
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS foglalas (
        id INTEGER,
        filmid INTEGER,
        foglalastime TIME,
        SZEK INT,
        TEREM INT,
        FOREIGN KEY (id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (filmid) REFERENCES filmek (fimlid) ON DELETE CASCADE
    )
""")



def leiras():
    top = Toplevel()
    top.title("Film leírás")
    top.config(bg="white")
    


def foglalas():
    top = Toplevel()
    top.title("Jegyfoglalás")
    top.config(bg="green")

    Label(top, text="Vezetéknév", font=("Ariel", 15)).grid(column=1, row=1, columnspan=2, pady=10)
    Label(top, text="Keresztnév", font=("Ariel", 15)).grid(column=1, row=2, columnspan=2, pady=10)
    Label(top, text="Telefonszám", font=("Ariel", 15)).grid(column=1, row=3, columnspan=2, pady=10)
    Label(top, text="Email", font=("Ariel", 15)).grid(column=1, row=4, columnspan=2, pady=10)
    Label(top, text="Email ismét", font=("Ariel", 15)).grid(column=1, row=5, columnspan=2, pady=10)

    vezeteknev_be = Entry(top, width=20, font=("Arial", 15), borderwidth=1, relief="solid")
    vezeteknev_be.grid(column=4, row=1, columnspan=2, padx=3, pady=5)

    keresztnev_be = Entry(top, width=20, font=("Arial", 15), borderwidth=1, relief="solid")
    keresztnev_be.grid(column=4, row=2, columnspan=2, padx=3, pady=5)

    telefon_be = Entry(top, width=20, font=("Arial", 15), borderwidth=1, relief="solid")
    telefon_be.grid(column=4, row=3, columnspan=2, padx=3, pady=5)

    email_be = Entry(top, width=20, font=("Arial", 15), borderwidth=1, relief="solid")
    email_be.grid(column=4, row=4, columnspan=2, padx=3, pady=5)

    email_megint_be = Entry(top, width=20, font=("Arial", 15), borderwidth=1, relief="solid")
    email_megint_be.grid(column=4, row=5, columnspan=2, padx=3, pady=5)

    uzenet_label = None  # Az üzenet címke eleinte nem létezik

    def adatbazis_mentes():
        nonlocal uzenet_label  # Használhatjuk a külső változót

        vezeteknev = vezeteknev_be.get().strip()
        keresztnev = keresztnev_be.get().strip()
        telefon = telefon_be.get().strip()
        email = email_be.get().strip()
        email_megint = email_megint_be.get().strip()

        # Ha az üzenet_label még nem létezik, létrehozzuk
        if uzenet_label is None:
            uzenet_label = Label(top, text="", font=("Arial", 12))
            uzenet_label.grid(column=4, row=6, columnspan=2, pady=5)

        if not vezeteknev or not keresztnev or not telefon or not email or not email_megint:
            uzenet_label.config(text="Minden mezőt ki kell tölteni!", fg="red")
            return

        if email != email_megint:
            uzenet_label.config(text="Az e-mail címek nem egyeznek!", fg="red")
            return

        # Ha minden rendben, mentés az adatbázisba
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (nev, email, iranyszam) VALUES (?, ?, ?)",
                  (vezeteknev + " " + keresztnev, email, telefon))
        conn.commit()
        conn.close()

        uzenet_label.config(text="Foglalás sikeres!", fg="green")

    foglalas_button = Button(top, text="Foglalás", font=("Arial", 18), command=adatbazis_mentes)
    foglalas_button.grid(column=2, row=7, padx=10, pady=10)





label_szoveg = Label(root, text="Műsoron lévő filmek listája:", font=("Arial", 20))
label_szoveg.grid(column=6, row=1, columnspan=2, pady=10)


label_szoveg = Label(root)
label_szoveg.grid(column=5, row=3, columnspan=2, pady=10)







horror = Image.open('horror.jpg')
kep = horror.resize((200,300))
horror_meret= ImageTk.PhotoImage(kep)
horror_meret_cim =Label(root, image=horror_meret).grid(column=2, row=2)


toystory = Image.open('toystory.jpg')
kep = toystory.resize((200,300))
toystory_meret= ImageTk.PhotoImage(kep)
toystory_meret_cim =Label(root, image=toystory_meret).grid(column=7, row=2)


mamma = Image.open('mammamia.jpg')
kep = mamma.resize((200,300))
mamma_meret= ImageTk.PhotoImage(kep)
mamma_meret_cim =Label(root, image=mamma_meret).grid(column=2, row=4)


puss = Image.open('puss.webp')
kep = puss.resize((200,300))
puss_meret= ImageTk.PhotoImage(kep)
puss_meret_cim =Label(root, image=puss_meret).grid(column=7, row=4)









horror_foglalas_button = Button(root, text="Foglalás", font=("Arial", 18), command=foglalas)
horror_foglalas_button.grid(column=5, row=2, padx=10, pady=10)


horror_leiras_button = Button(root, text="Film leírás", font=("Arial", 18), command=leiras)
horror_leiras_button.grid(column=6, row=2, padx=10, pady=10)


toystory_foglalas_button = Button(root, text="Foglalás", font=("Arial", 18), command=foglalas)
toystory_foglalas_button.grid(column=11, row=2, padx=10, pady=10)


toystory_leiras_button = Button(root, text="Film leírás", font=("Arial", 18), command=leiras)
toystory_leiras_button.grid(column=12, row=2, padx=10, pady=10)


mamma_foglalas_button = Button(root, text="Foglalás", font=("Arial", 18), command=foglalas)
mamma_foglalas_button.grid(column=5, row=4, padx=10, pady=10)


mamma_leiras_button = Button(root, text="Film leírás", font=("Arial", 18), command=leiras)
mamma_leiras_button.grid(column=6, row=4, padx=10, pady=10)



puss_foglalas_button = Button(root, text="Foglalás", font=("Arial", 18), command=foglalas)
puss_foglalas_button.grid(column=11, row=4, padx=10, pady=10)


puss_leiras_button = Button(root, text="Film leírás", font=("Arial", 18), command=leiras)
puss_leiras_button.grid(column=12, row=4, padx=10, pady=10)

root.mainloop()
