from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("Főoldal")
root.geometry("750x270")
root.config(bg="")



#fő ablak dizájnolása, elemek létrehozása
label_szoveg = Label(root, text="Műsoron lévő filmek listája:", font=("Arial", 20))
label_szoveg.grid(column=1, row=1, columnspan=2, pady=10)


horror = Image.open('horror.jpg')
kep = horror.resize((30,25))
horror_meret= ImageTk.PhotoImage(kep)
horror_meret_cim =Label(root, image=horror_meret).grid(column=1, row=2)



# image1 = Image.open('kincs.webp')
# image1 = ImageTk.PhotoImage(image1)
# image1_label =Label(root, image=image).grid(column=1, row=3)

# image2 = Image.open('mammamia.jpg')
# image2 = ImageTk.PhotoImage(image2)
# image2_label =Label(root, image=image).grid(column=1, row=4)

# image3 = Image.open('puss.webp')
# image3 = ImageTk.PhotoImage(image3)
# image3_label =Label(root, image=image).grid(column=1, row=5)

# image4 = Image.open('toystory.jpg')
# image4 = ImageTk.PhotoImage(image4)
# image4_label =Label(root, image=image).grid(column=1, row=6)



# Futtatás
root.mainloop()
