import tkinter as tk
from tkinter import ttk

def update_entries(event):
    selected_option = combo.get()
    clear_entries()
    if selected_option == "Option 1":
        entry1.config(state="normal")
    elif selected_option == "Option 2":
        entry2.config(state="normal")
        entry3.config(state="normal")

def clear_entries():
    entry1.config(state="disabled")
    entry2.config(state="disabled")
    entry3.config(state="disabled")

root = tk.Tk()

combo = ttk.Combobox(root, values=["Option 1", "Option 2"])
combo.grid(row=0, column=0)
combo.bind("<<ComboboxSelected>>", update_entries)

entry1 = tk.Entry(root, state="disabled")
entry2 = tk.Entry(root, state="disabled")
entry3 = tk.Entry(root, state="disabled")

entry1.grid(row=1, column=0)
entry2.grid(row=2, column=0)
entry3.grid(row=3, column=0)

root.mainloop()
