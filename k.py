import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def beim_klicken_passiert_das():
    print("Der 'Start'-Button wurde geklickt! Das Projekt startet!")
    my_label.configure(text="Projekt gestartet!")

root = ctk.CTk(fg_color="yellow")

root.title('Poco_Inventar')
root.geometry('500x500')

my_label = ctk.CTkLabel(master=root, text="Poco Inventar", font=("Arial", 24))
my_label.pack(pady=20)

my_button = ctk.CTkButton(master=root, text="Start", command=beim_klicken_passiert_das)
my_button.pack(pady=40)

root.mainloop()