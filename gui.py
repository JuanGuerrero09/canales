import tkinter
from tkinter import ttk

window = tkinter.Tk()
window.title('Data entry form')

frame = tkinter.Frame(window)
frame.pack()

def submit_data():
    print('Hola mundo')
    proyectname = project_name_entry.get()
    managername = manager_name_entry.get()
    areaname = area_combobox.get()
# Project info 

project_info_frame = tkinter.LabelFrame(frame, text='Project info')
project_info_frame.grid(row= 0, column=0, padx=20, pady=10)

project_name_label = tkinter.Label(project_info_frame, text='Project Name')
project_name_label.grid(row=0, column=0)

manager_name_label = tkinter.Label(project_info_frame, text='Project Manager')
manager_name_label.grid(row=0, column=1)


project_name_entry = tkinter.Entry(project_info_frame)
manager_name_entry = tkinter.Entry(project_info_frame)
project_name_entry.grid(row=1, column=0)
manager_name_entry.grid(row=1, column=1)

area_label = tkinter.Label(project_info_frame, text='Area')
area_combobox = ttk.Combobox(project_info_frame, values=["", "Water", "Structures", "Oil"])
area_label.grid(row=0, column=2)
area_combobox.grid(row=1, column=2)

price_label = tkinter.Label(project_info_frame, text="Price")
price_spinbox = tkinter.Spinbox(project_info_frame, from_=0, to='infinity')
price_label.grid(row=2, column=0)
price_spinbox.grid(row=3, column=0)

location_label = tkinter.Label(project_info_frame, text="Project Location")
location_combobox = ttk.Combobox(project_info_frame, values=["Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America"])
location_label.grid(row=2, column=1)
location_combobox.grid(row=3, column=1)

for widget in project_info_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)
# Activity info

# sticky news toma todo el espacio entro de lo posible
activity_frame = tkinter.LabelFrame(frame)
activity_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

activity_status = tkinter.Label(activity_frame, text="Activity Status")

reg_status_var = tkinter.StringVar(value="Not Completed")
registered_check = tkinter.Checkbutton(activity_frame, text="Completed Activity",
                                       variable=reg_status_var, onvalue="Registered", offvalue="Not registered")

activity_status.grid(row=0, column=0)
registered_check.grid(row=1, column=0)

name_activity_label = tkinter.Label(activity_frame, text= "Name of activity")
name_activity_spinbox = tkinter.Entry(activity_frame)
name_activity_label.grid(row=0, column=1)
name_activity_spinbox.grid(row=1, column=1)

price_activity_label = tkinter.Label(activity_frame, text="Price")
price_activity_spinbox = tkinter.Spinbox(activity_frame, from_=0, to="infinity")
price_activity_label.grid(row=0, column=2)
price_activity_spinbox.grid(row=1, column=2)

for widget in activity_frame.winfo_children():
    widget.grid_configure(padx=10, pady=5)

# Button 

button_frame = tkinter.LabelFrame(frame)
button_frame.grid(row=2, column=0, sticky="news", padx=20, pady=10)


add_activity_button = tkinter.Button(button_frame, text='Add Activity', command = submit_data)
submit_button = tkinter.Button(button_frame, text='Submit')

add_activity_button.grid(row=0, column=0, padx=20, pady=10)
submit_button.grid(row=0, column=1, padx=20, pady=10)

window.mainloop()

#ACTIVIDAD -> SUBACTIVIDAD -> RECURSOS (TODO EN HORAS O EN LO QUE SE REQUIERA)