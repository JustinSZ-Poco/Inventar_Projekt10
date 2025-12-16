import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

RICHTIGER_PIN = "1234"

def zeige_inventar_bearbeiten_seite():
    for widget in root.winfo_children():
        widget.destroy()

    ctk.CTkButton(master=root, text="Zurück zur Hauptseite", command=zeige_hauptanwendung).pack(pady=30)

def bearbeiten_aktion():
    zeige_inventar_bearbeiten_seite()

def loeschen_aktion():
    print("Löschen-Button geklickt!")

def hinzufuegen_aktion():
    print("Hinzufügen-Button geklickt!")

def zeige_hauptanwendung():
    for widget in root.winfo_children():
        widget.destroy()

    global main_app_label

    main_app_label = ctk.CTkLabel(master=root, text="Willkommen im Poco Inventar!", font=("Arial", 24))
    main_app_label.pack(pady=30)

    btn_bearbeiten = ctk.CTkButton(master=root, text="Inventar bearbeiten", command=bearbeiten_aktion)
    btn_bearbeiten.pack(pady=10)

    btn_loeschen = ctk.CTkButton(master=root, text="Inventar löschen", command=loeschen_aktion)
    btn_loeschen.pack(pady=10)

    btn_hinzufuegen = ctk.CTkButton(master=root, text="Inventar hinzufügen", command=hinzufuegen_aktion)
    btn_hinzufuegen.pack(pady=10)

def beim_klicken_passiert_das():
    eingegebener_pin = pin_eingabe.get()

    if eingegebener_pin == RICHTIGER_PIN:
        print("PIN korrekt! Zugriff gewährt. Öffne Hauptanwendung.")
        zeige_hauptanwendung()
    else:
        print(f"Falscher PIN: {eingegebener_pin}. Versuch es nochmal.")
        my_label.configure(text="Falscher PIN! Bitte erneut versuchen.")
        pin_eingabe.delete(0, ctk.END)

root = ctk.CTk(fg_color="yellow")

root.title('Poco_Inventar - Login')
root.geometry('500x500')

my_label = ctk.CTkLabel(master=root, text="Bitte PIN eingeben:", font=("Arial", 20))
my_label.pack(pady=20)

pin_eingabe = ctk.CTkEntry(master=root, placeholder_text="PIN", width=200, show="*")
pin_eingabe.pack(pady=10)

my_button = ctk.CTkButton(master=root, text="Anmelden", command=beim_klicken_passiert_das)
my_button.pack(pady=20)

root.mainloop()