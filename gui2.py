import tkinter
from tkinter import messagebox as MessageBox
import customtkinter

def test():
    MessageBox.showinfo("Hola!", "Hola mundo") # título, mensaje

root = tkinter.Tk()

tkinter.Button(root, text = "Clícame", command=test).pack()
button = customtkinter.CTkButton(root, text="Open Dialog")
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

root.mainloop()