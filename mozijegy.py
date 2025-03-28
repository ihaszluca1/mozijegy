from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Főoldal")
root.geometry("1000x1000")
root.config(bg="white")


def halloween():
    top = Toplevel()
    top.title("Hosszúság átváltás")
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


horror = Image.open('horror.jpg')
kep = horror.resize((200,300))
horror_meret= ImageTk.PhotoImage(kep)
horror_meret_cim =Label(root, image=horror_meret).grid(column=1, row=2)

horror_foglalas_button = Button(root, text="Foglalás", font=("Arial", 18), command=halloween)
horror_foglalas_button.grid(column=5, row=2, padx=10, pady=10)


toystory = Image.open('toystory.jpg')
kep = toystory.resize((200,300))
toystory_meret= ImageTk.PhotoImage(kep)
toystory_meret_cim =Label(root, image=toystory_meret).grid(column=7, row=2)


toystory_foglalas_button = Button(root, text="Foglalás", font=("Arial", 18), command=toyystory)
toystory_foglalas_button.grid(column=11, row=2, padx=10, pady=10)


label_szoveg = Label(root)
label_szoveg.grid(column=5, row=3, columnspan=2, pady=10)


mamma = Image.open('mammamia.jpg')
kep = mamma.resize((200,300))
mamma_meret= ImageTk.PhotoImage(kep)
mamma_meret_cim =Label(root, image=mamma_meret).grid(column=1, row=4)


mamma_foglalas_button = Button(root, text="Foglalás", font=("Arial", 18), command=miia)
mamma_foglalas_button.grid(column=5, row=4, padx=10, pady=10)



puss = Image.open('puss.webp')
kep = puss.resize((200,300))
puss_meret= ImageTk.PhotoImage(kep)
puss_meret_cim =Label(root, image=puss_meret).grid(column=7, row=4)


puss_foglalas_button = Button(root, text="Foglalás", font=("Arial", 18), command=boots)
puss_foglalas_button.grid(column=11, row=4, padx=10, pady=10)




root.mainloop()
