import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

RICHTIGER_PIN = "1234"

def beim_klicken_passiert_das():
    eingegebener_pin = pin_eingabe.get()

    if eingegebener_pin == RICHTIGER_PIN:
        print("PIN korrekt! Zugriff gewährt.")
        my_label.configure(text="PIN korrekt! Willkommen!")
    else:
        print(f"Falscher PIN: {eingegebener_pin}. Versuch es nochmal.")
        my_label.configure(text="Falscher PIN! Bitte erneut versuchen.")
        pin_eingabe.delete(0, ctk.END)

root = ctk.CTk(fg_color="yellow")

root.title('Poco_Inventar')
root.geometry('500x500')

my_label = ctk.CTkLabel(master=root, text="Bitte PIN eingeben:", font=("Arial", 20))
my_label.pack(pady=20)

pin_eingabe = ctk.CTkEntry(master=root, placeholder_text="PIN", width=200, show="*")
pin_eingabe.pack(pady=10)

my_button = ctk.CTkButton(master=root, text="Anmelden", command=beim_klicken_passiert_das)
my_button.pack(pady=20)

root.mainloop()