import tkinter as tk
from tkinter import ttk

class CustomCombobox(ttk.Combobox):
    def __init__(self, master=None, values=[], **kwargs):
        super().__init__(master, values=values, **kwargs)
        self.values = values
        self.bind("<<ComboboxSelected>>", self.update_entries)

    def update_entries(self, event):
        selected_option = self.get()
        for entry in self.master.entries:
            if entry["state"] == "disabled":
                entry.delete(0, 'end')

        if selected_option == "Option 1":
            self.master.entry1.config(state="normal")
        elif selected_option == "Option 2":
            self.master.entry2.config(state="normal")
            self.master.entry3.config(state="normal")

class CustomEntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', **kwargs):
        state = kwargs.pop('state', 'normal')
        super().__init__(master, **kwargs)

        self.state = state
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        if self.state != 'disabled':
            self.insert(0, self.placeholder)
            self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get() and self.state == 'normal':
            self.put_placeholder()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.combo = CustomCombobox(self, values=["Option 1", "Option 2"])
        self.combo.grid(row=0, column=0)

        self.entry1 = CustomEntryWithPlaceholder(self, state="disabled", placeholder='entry')
        self.entry2 = CustomEntryWithPlaceholder(self, state="disabled", placeholder='entry')
        self.entry3 = CustomEntryWithPlaceholder(self, state="disabled", placeholder='entry')

        self.entry1.grid(row=1, column=0)
        self.entry2.grid(row=2, column=0)
        self.entry3.grid(row=3, column=0)

    def clear_entries(self):
        for entry in self.entries:
            if entry["state"] == "disabled":
                entry.delete(0, 'end')
                entry.put_placeholder()

app = Application()
app.mainloop()
