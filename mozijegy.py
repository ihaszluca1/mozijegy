from tkinter import *

root = Tk()
root.title("Főoldal")
root.config(bg="")



#fő ablak dizájnolása, elemek létrehozása
label_szoveg = Label(root, text="Műsoron lévő filmek listája:", font=("Arial", 20))
label_szoveg.grid(column=1, row=1, columnspan=2, pady=10)

# Futtatás
root.mainloop()
