import tkinter as tk
import customtkinter as ctk
import mysql.connector  # Importiere das MySQL-Konnektor-Modul

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

RICHTIGER_PIN = "1234"


# --- Datenbankfunktionen ---
def get_connection():
    return mysql.connector.connect(
        host='tramspotters.ddnss.de',
        port=3306,
        user='kdm25',
        password='kdm25',
        database='kdm25_sql_uebung'
    )


def get_inventar_daten():
    """Holt die Inventardaten aus der Datenbank und gibt sie als Liste von Dictionaries zurück."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = 'SELECT id, name, kategorie, standort, status FROM t_inventar'
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as err:
        print(f"Datenbankfehler beim Abrufen des Inventars: {err}")
        return []  # Gib eine leere Liste zurück, wenn ein Fehler auftritt
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()


# --- GUI-Seitenfunktionen ---

def zeige_inventar_bearbeiten_seite():
    for widget in root.winfo_children():
        widget.destroy()

    ctk.CTkLabel(master=root, text="Inventar bearbeiten", font=("Arial", 24)).pack(pady=20)
    # Hier könnten die Widgets für die Bearbeitung hinzugefügt werden
    ctk.CTkButton(master=root, text="Änderungen speichern", command=lambda: print("Änderungen gespeichert!")).pack(
        pady=10)
    ctk.CTkButton(master=root, text="Zurück zur Hauptseite", command=zeige_hauptanwendung).pack(pady=30)


def zeige_inventar_loeschen_seite():
    for widget in root.winfo_children():
        widget.destroy()

    ctk.CTkLabel(master=root, text="Inventar löschen", font=("Arial", 24)).pack(pady=20)
    # Hier könnten die Widgets für das Löschen hinzugefügt werden
    ctk.CTkButton(master=root, text="Zurück zur Hauptseite", command=zeige_hauptanwendung).pack(pady=30)


def zeige_inventar_hinzufuegen_seite():
    for widget in root.winfo_children():
        widget.destroy()

    ctk.CTkLabel(master=root, text="Inventar hinzufügen", font=("Arial", 24)).pack(pady=20)
    # Hier könnten die Widgets für das Hinzufügen hinzugefügt werden
    ctk.CTkButton(master=root, text="Zurück zur Hauptseite", command=zeige_hauptanwendung).pack(pady=30)


def zeige_inventar_anzeige_seite():
    """Zeigt eine Seite an, auf der das gesamte Inventar aus der Datenbank angezeigt wird."""
    for widget in root.winfo_children():
        widget.destroy()

    ctk.CTkLabel(master=root, text="Aktuelles Inventar", font=("Arial", 24)).pack(pady=20)

    inventar_daten = get_inventar_daten()  # Hol die Daten von der Datenbank

    if not inventar_daten:
        ctk.CTkLabel(master=root, text="Keine Inventardaten gefunden oder Fehler bei der Verbindung.",
                     font=("Arial", 16)).pack(pady=10)
    else:
        # Erstelle einen Frame für die Tabelle, um die Widgets besser zu gruppieren und zu layouten
        table_frame = ctk.CTkFrame(master=root)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Kopfzeile der Tabelle
        headers = ["ID", "Name", "Kategorie", "Standort", "Status"]
        for col_idx, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(master=table_frame, text=header_text, font=("Arial", 14, "bold"))
            header_label.grid(row=0, column=col_idx, padx=5, pady=5, sticky="w")
            table_frame.grid_columnconfigure(col_idx, weight=1)  # Macht die Spalten flexibel

        # Inventardaten anzeigen
        for row_idx, item in enumerate(inventar_daten):
            ctk.CTkLabel(master=table_frame, text=item['id'], font=("Arial", 12)).grid(row=row_idx + 1, column=0,
                                                                                       padx=5, pady=2, sticky="w")
            ctk.CTkLabel(master=table_frame, text=item['name'], font=("Arial", 12)).grid(row=row_idx + 1, column=1,
                                                                                         padx=5, pady=2, sticky="w")
            ctk.CTkLabel(master=table_frame, text=item['kategorie'], font=("Arial", 12)).grid(row=row_idx + 1, column=2,
                                                                                              padx=5, pady=2,
                                                                                              sticky="w")
            ctk.CTkLabel(master=table_frame, text=item['standort'], font=("Arial", 12)).grid(row=row_idx + 1, column=3,
                                                                                             padx=5, pady=2, sticky="w")
            ctk.CTkLabel(master=table_frame, text=item['status'], font=("Arial", 12)).grid(row=row_idx + 1, column=4,
                                                                                           padx=5, pady=2, sticky="w")

    ctk.CTkButton(master=root, text="Zurück zur Hauptseite", command=zeige_hauptanwendung).pack(pady=30)


# --- Aktionen für Buttons der Hauptanwendung ---
def bearbeiten_aktion():
    zeige_inventar_bearbeiten_seite()


def loeschen_aktion():
    zeige_inventar_loeschen_seite()


def hinzufuegen_aktion():
    zeige_inventar_hinzufuegen_seite()


def zeige_hauptanwendung():
    for widget in root.winfo_children():
        widget.destroy()

    global main_app_label

    main_app_label = ctk.CTkLabel(master=root, text="Willkommen im Poco Inventar!", font=("Arial", 24))
    main_app_label.pack(pady=30)

    # Neuer Button zum Anzeigen des Inventars
    btn_inventar_anzeigen = ctk.CTkButton(master=root, text="Inventar anzeigen", command=zeige_inventar_anzeige_seite)
    btn_inventar_anzeigen.pack(pady=10)

    btn_bearbeiten = ctk.CTkButton(master=root, text="Inventar bearbeiten", command=bearbeiten_aktion)
    btn_bearbeiten.pack(pady=10)

    btn_loeschen = ctk.CTkButton(master=root, text="Inventar löschen", command=loeschen_aktion)
    btn_loeschen.pack(pady=10)

    btn_hinzufuegen = ctk.CTkButton(master=root, text="Inventar hinzufügen", command=hinzufuegen_aktion)
    btn_hinzufuegen.pack(pady=10)


# --- Login-Logik ---
def beim_klicken_passiert_das():
    eingegebener_pin = pin_eingabe.get()

    if eingegebener_pin == RICHTIGER_PIN:
        print("PIN korrekt! Zugriff gewährt.")
        zeige_hauptanwendung()
    else:
        print(f"Falscher PIN: {eingegebener_pin}. Versuch es nochmal.")
        my_label.configure(text="Falscher PIN! Bitte erneut versuchen.")
        pin_eingabe.delete(0, ctk.END)


# --- Hauptfenster-Setup (Login-Seite als Start) ---
root = ctk.CTk(fg_color="yellow")

root.title('Poco_Inventar - Login')
root.geometry('700x700')  # Etwas mehr Platz für die Inventaranzeige

my_label = ctk.CTkLabel(master=root, text="Bitte PIN eingeben:", font=("Arial", 20))
my_label.pack(pady=20)

pin_eingabe = ctk.CTkEntry(master=root, placeholder_text="PIN", width=200, show="*")
pin_eingabe.pack(pady=10)

my_button = ctk.CTkButton(master=root, text="Anmelden", command=beim_klicken_passiert_das)
my_button.pack(pady=20)

root.mainloop()