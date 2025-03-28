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
        id INTEGER PRIMARY KEY
        nev TEXT
        email TEXT
        iranyszam INTEGER
    )
""")

c.execute("""
    CREATE TABLE IF NOT EXISTS filmek (
          cim TEXT
          tipus TEXT
          fimlid INTEGER PRIMARY KEY
          hosszido TIME
          vetites DATE
          )
""")

c.execute(""""
          CREATE TABLE IF NOT EXISTS foglalas(
          id INTEGER
          filmid INTEGER
          foglalastime TIME
          SZEK INT
          TEREM INT
          FOREIGN KEY (id) REFERENCES users (id) ON DELETE CASCADE
          FOREIGN KEY (filmid) REFERENCES users (filmid) ON DELETE CASCADE
          )
""")

conn.commit()
conn.close()


def leiras():
    top = Toplevel()
    top.title("Film leírás")
    top.config(bg="white")


def halloween():
    top = Toplevel()
    top.title("Gyilkos halloween foglalás")
    top.config(bg="white")


def toyystory():
    toy = Toplevel()
    toy.title("Toy Story foglalás")
    toy.config(bg="#a3cef1")



def miia():
    mia = Toplevel()
    mia.title("Mamma mia foglalás")
    mia.config(bg="white")


def boots():
    cat = Toplevel()
    cat.title("Csizmás a kandúr foglalás")
    cat.config(bg="white")



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









horror_foglalas_button = Button(root, text="Foglalás", font=("Arial", 18), command=halloween)
horror_foglalas_button.grid(column=5, row=2, padx=10, pady=10)


horror_leiras_button = Button(root, text="Film leírás", font=("Arial", 18), command=leiras)
horror_leiras_button.grid(column=6, row=2, padx=10, pady=10)


toystory_foglalas_button = Button(root, text="Foglalás", font=("Arial", 18), command=toyystory)
toystory_foglalas_button.grid(column=11, row=2, padx=10, pady=10)


toystory_leiras_button = Button(root, text="Film leírás", font=("Arial", 18), command=leiras)
toystory_leiras_button.grid(column=12, row=2, padx=10, pady=10)


mamma_foglalas_button = Button(root, text="Foglalás", font=("Arial", 18), command=miia)
mamma_foglalas_button.grid(column=5, row=4, padx=10, pady=10)


mamma_leiras_button = Button(root, text="Film leírás", font=("Arial", 18), command=leiras)
mamma_leiras_button.grid(column=6, row=4, padx=10, pady=10)



puss_foglalas_button = Button(root, text="Foglalás", font=("Arial", 18), command=boots)
puss_foglalas_button.grid(column=11, row=4, padx=10, pady=10)


puss_leiras_button = Button(root, text="Film leírás", font=("Arial", 18), command=leiras)
puss_leiras_button.grid(column=12, row=4, padx=10, pady=10)

root.mainloop()
