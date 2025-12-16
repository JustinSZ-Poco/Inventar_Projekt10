
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import mysql.connector  # Importiere das MySQL-Konnektor-Modul

# ---- CustomTkinter Setup ----
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

RICHTIGER_PIN = "1234"

# >>> WICHTIG: root früh erzeugen (fix für "Unresolved reference 'root'")
root = ctk.CTk(fg_color="yellow")
root.title('Poco_Inventar - Login')
root.geometry('1000x600')  # Mehr Platz für die Inventaranzeige

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
        sql = 'SELECT id, name, kategorie, standort, status FROM t_inventar ORDER BY id ASC'
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

def get_inventar_by_id(inventar_id):
    """Holt einen einzelnen Datensatz per ID (dict) oder gibt None zurück."""
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = 'SELECT id, name, kategorie, standort, status FROM t_inventar WHERE id = %s'
        cursor.execute(sql, (inventar_id,))
        return cursor.fetchone()
    except mysql.connector.Error as err:
        print(f"Datenbankfehler beim Abrufen per ID: {err}")
        return None
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def insert_inventar(name, kategorie, standort, status):
    """Fügt einen neuen Datensatz ein und gibt die neue ID zurück."""
    for label, value in [("Name", name), ("Kategorie", kategorie), ("Standort", standort), ("Status", status)]:
        if value is None or str(value).strip() == "":
            raise ValueError(f"Feld '{label}' darf nicht leer sein.")

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO t_inventar (name, kategorie, standort, status) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (name.strip(), kategorie.strip(), standort.strip(), status.strip()))
        conn.commit()
        return cursor.lastrowid
    except mysql.connector.Error as err:
        # Nach oben weitergeben, damit GUI den Fehler anzeigen kann
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def update_inventar(inventar_id, name, kategorie, standort, status):
    """Aktualisiert einen Datensatz; gibt die Anzahl betroffener Zeilen zurück (0 = nicht gefunden)."""
    if not isinstance(inventar_id, int) or inventar_id <= 0:
        raise ValueError("ID muss eine positive ganze Zahl sein.")
    for label, value in [("Name", name), ("Kategorie", kategorie), ("Standort", standort), ("Status", status)]:
        if value is None or str(value).strip() == "":
            raise ValueError(f"Feld '{label}' darf nicht leer sein.")

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            UPDATE t_inventar
               SET name = %s, kategorie = %s, standort = %s, status = %s
             WHERE id = %s
        """
        cursor.execute(sql, (name.strip(), kategorie.strip(), standort.strip(), status.strip(), inventar_id))
        conn.commit()
        return cursor.rowcount
    except mysql.connector.Error as err:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

def delete_inventar(inventar_id):
    """Löscht einen Datensatz; gibt die Anzahl betroffener Zeilen zurück (0 = nicht gefunden)."""
    if not isinstance(inventar_id, int) or inventar_id <= 0:
        raise ValueError("ID muss eine positive ganze Zahl sein.")

    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM t_inventar WHERE id = %s"
        cursor.execute(sql, (inventar_id,))
        conn.commit()
        return cursor.rowcount
    except mysql.connector.Error as err:
        raise
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# --- GUI Hilfsfunktion ---
def clear_root():
    for widget in root.winfo_children():
        widget.destroy()

# --- GUI-Seiten ---
def zeige_inventar_anzeige_seite():
    clear_root()
    ctk.CTkLabel(master=root, text="Aktuelles Inventar", font=("Arial", 24)).pack(pady=20)

    top_bar = ctk.CTkFrame(master=root)
    top_bar.pack(fill="x", padx=20)
    ctk.CTkButton(top_bar, text="Aktualisieren", command=zeige_inventar_anzeige_seite).pack(side="left", padx=5, pady=10)
    ctk.CTkButton(top_bar, text="Hinzufügen", command=zeige_inventar_hinzufuegen_seite).pack(side="left", padx=5, pady=10)
    ctk.CTkButton(top_bar, text="Zurück zur Hauptseite", command=zeige_hauptanwendung).pack(side="right", padx=5, pady=10)

    inventar_daten = get_inventar_daten()

    if not inventar_daten:
        ctk.CTkLabel(master=root, text="Keine Inventardaten gefunden oder Fehler bei der Verbindung.",
                     font=("Arial", 16)).pack(pady=10)
    else:
        table_frame = ctk.CTkFrame(master=root)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        headers = ["ID", "Name", "Kategorie", "Standort", "Status", "Aktionen"]
        for col_idx, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(master=table_frame, text=header_text, font=("Arial", 14, "bold"))
            header_label.grid(row=0, column=col_idx, padx=5, pady=5, sticky="w")
            table_frame.grid_columnconfigure(col_idx, weight=1)

        for row_idx, item in enumerate(inventar_daten, start=1):
            ctk.CTkLabel(master=table_frame, text=item['id'], font=("Arial", 12)).grid(row=row_idx, column=0, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(master=table_frame, text=item['name'], font=("Arial", 12)).grid(row=row_idx, column=1, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(master=table_frame, text=item['kategorie'], font=("Arial", 12)).grid(row=row_idx, column=2, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(master=table_frame, text=item['standort'], font=("Arial", 12)).grid(row=row_idx, column=3, padx=5, pady=2, sticky="w")
            ctk.CTkLabel(master=table_frame, text=item['status'], font=("Arial", 12)).grid(row=row_idx, column=4, padx=5, pady=2, sticky="w")

            act_frame = ctk.CTkFrame(master=table_frame, fg_color="transparent")
            act_frame.grid(row=row_idx, column=5, padx=5, pady=2, sticky="w")
            ctk.CTkButton(act_frame, text="Bearbeiten", width=90,
                          command=lambda iid=item['id']: zeige_inventar_bearbeiten_seite(prefill_id=iid)).pack(side="left", padx=4)
            ctk.CTkButton(act_frame, text="Löschen", width=90,
                          command=lambda iid=item['id']: loesche_eintrag_mit_bestaetigung(iid)).pack(side="left", padx=4)

def zeige_inventar_hinzufuegen_seite():
    clear_root()

    ctk.CTkLabel(master=root, text="Inventar hinzufügen", font=("Arial", 24)).pack(pady=20)

    form = ctk.CTkFrame(master=root)
    form.pack(pady=10, padx=20)

    name_var = tk.StringVar()
    kat_var = tk.StringVar()
    standort_var = tk.StringVar()
    status_var = tk.StringVar()

    def row(label_text, var, r):
        ctk.CTkLabel(form, text=label_text, width=140, anchor="w").grid(row=r, column=0, padx=8, pady=6, sticky="w")
        ctk.CTkEntry(form, textvariable=var, width=300).grid(row=r, column=1, padx=8, pady=6, sticky="w")

    row("Name:", name_var, 0)
    row("Kategorie:", kat_var, 1)
    row("Standort:", standort_var, 2)
    row("Status:", status_var, 3)

    def speichern():
        try:
            new_id = insert_inventar(name_var.get(), kat_var.get(), standort_var.get(), status_var.get())
            messagebox.showinfo("Erfolg", f"Eintrag hinzugefügt. Neue ID: {new_id}")
            zeige_inventar_anzeige_seite()
        except ValueError as ve:
            messagebox.showwarning("Validierung", str(ve))
        except mysql.connector.Error as err:
            messagebox.showerror("Datenbankfehler", str(err))

    btns = ctk.CTkFrame(master=root, fg_color="transparent")
    btns.pack(pady=15)
    ctk.CTkButton(btns, text="Speichern", command=speichern).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Zurück zur Hauptseite", command=zeige_hauptanwendung).pack(side="left", padx=6)

def zeige_inventar_bearbeiten_seite(prefill_id=None):
    clear_root()

    ctk.CTkLabel(master=root, text="Inventar bearbeiten", font=("Arial", 24)).pack(pady=20)

    form = ctk.CTkFrame(master=root)
    form.pack(pady=10, padx=20)

    id_var = tk.StringVar(value=str(prefill_id) if prefill_id else "")
    name_var = tk.StringVar()
    kat_var = tk.StringVar()
    standort_var = tk.StringVar()
    status_var = tk.StringVar()

    def row(label_text, var, r):
        ctk.CTkLabel(form, text=label_text, width=140, anchor="w").grid(row=r, column=0, padx=8, pady=6, sticky="w")
        ctk.CTkEntry(form, textvariable=var, width=300).grid(row=r, column=1, padx=8, pady=6, sticky="w")

    row("ID:", id_var, 0)
    row("Name:", name_var, 1)
    row("Kategorie:", kat_var, 2)
    row("Standort:", standort_var, 3)
    row("Status:", status_var, 4)

    def laden():
        try:
            iid = int(id_var.get())
        except ValueError:
            messagebox.showwarning("Hinweis", "Bitte eine gültige ID eingeben.")
            return
        data = get_inventar_by_id(iid)
        if not data:
            messagebox.showinfo("Info", f"Kein Datensatz mit ID {iid} gefunden.")
            return
        name_var.set(data["name"])
        kat_var.set(data["kategorie"])
        standort_var.set(data["standort"])
        status_var.set(data["status"])

    def speichern():
        try:
            iid = int(id_var.get())
        except ValueError:
            messagebox.showwarning("Validierung", "ID muss eine Zahl sein.")
            return
        try:
            affected = update_inventar(iid, name_var.get(), kat_var.get(), standort_var.get(), status_var.get())
            if affected == 0:
                messagebox.showinfo("Info", f"Keine Zeile mit ID {iid} aktualisiert (nicht gefunden).")
            else:
                messagebox.showinfo("Erfolg", f"Datensatz ID {iid} aktualisiert.")
                zeige_inventar_anzeige_seite()
        except ValueError as ve:
            messagebox.showwarning("Validierung", str(ve))
        except mysql.connector.Error as err:
            messagebox.showerror("Datenbankfehler", str(err))

    btns = ctk.CTkFrame(master=root, fg_color="transparent")
    btns.pack(pady=15)
    ctk.CTkButton(btns, text="Laden", command=laden).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Speichern", command=speichern).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Zurück zur Hauptseite", command=zeige_hauptanwendung).pack(side="left", padx=6)

def zeige_inventar_loeschen_seite():
    clear_root()

    ctk.CTkLabel(master=root, text="Inventar löschen", font=("Arial", 24)).pack(pady=20)

    form = ctk.CTkFrame(master=root)
    form.pack(pady=10, padx=20)

    id_var = tk.StringVar()

    ctk.CTkLabel(form, text="ID:", width=140, anchor="w").grid(row=0, column=0, padx=8, pady=6, sticky="w")
    ctk.CTkEntry(form, textvariable=id_var, width=300).grid(row=0, column=1, padx=8, pady=6, sticky="w")

    def loeschen():
        try:
            iid = int(id_var.get())
        except ValueError:
            messagebox.showwarning("Validierung", "ID muss eine Zahl sein.")
            return

        if messagebox.askyesno("Bestätigung", f"Eintrag mit ID {iid} wirklich löschen?"):
            try:
                affected = delete_inventar(iid)
                if affected == 0:
                    messagebox.showinfo("Info", f"Keine Zeile mit ID {iid} gefunden.")
                else:
                    messagebox.showinfo("Erfolg", f"Datensatz mit ID {iid} gelöscht.")
                    zeige_inventar_anzeige_seite()
            except mysql.connector.Error as err:
                messagebox.showerror("Datenbankfehler", str(err))

    btns = ctk.CTkFrame(master=root, fg_color="transparent")
    btns.pack(pady=15)
    ctk.CTkButton(btns, text="Löschen", command=loeschen).pack(side="left", padx=6)
    ctk.CTkButton(btns, text="Zurück zur Hauptseite", command=zeige_hauptanwendung).pack(side="left", padx=6)

def loesche_eintrag_mit_bestaetigung(inventar_id):
    if messagebox.askyesno("Bestätigung", f"Eintrag mit ID {inventar_id} wirklich löschen?"):
        try:
            affected = delete_inventar(inventar_id)
            if affected == 0:
                messagebox.showinfo("Info", f"Keine Zeile mit ID {inventar_id} gefunden.")
            else:
                messagebox.showinfo("Erfolg", f"Datensatz mit ID {inventar_id} gelöscht.")
                zeige_inventar_anzeige_seite()
        except mysql.connector.Error as err:
            messagebox.showerror("Datenbankfehler", str(err))

# --- Aktionen für Buttons der Hauptanwendung ---
def bearbeiten_aktion():
    zeige_inventar_bearbeiten_seite()

def loeschen_aktion():
    zeige_inventar_loeschen_seite()

def hinzufuegen_aktion():
    zeige_inventar_hinzufuegen_seite()

def zeige_hauptanwendung():
    clear_root()

    ctk.CTkLabel(master=root, text="Willkommen im Poco Inventar!", font=("Arial", 24)).pack(pady=30)

    ctk.CTkButton(master=root, text="Inventar anzeigen", command=zeige_inventar_anzeige_seite).pack(pady=10)
    ctk.CTkButton(master=root, text="Inventar hinzufügen", command=hinzufuegen_aktion).pack(pady=10)
    ctk.CTkButton(master=root, text="Inventar bearbeiten", command=bearbeiten_aktion).pack(pady=10)
    ctk.CTkButton(master=root, text="Inventar löschen", command=loeschen_aktion).pack(pady=10)

# --- Login-Logik ---
def beim_klicken_passiert_das():
    eingegebener_pin = pin_eingabe.get()

    if eingegebener_pin == RICHTIGER_PIN:
        zeige_hauptanwendung()
    else:
        mymy_label.configure(text="Falscher PIN! Bitte erneut versuchen.")
        pin_eingabe.delete(0, ctk.END)

# --- Login-Start-Widgets ---
mymy_label = ctk.CTkLabel(master=root, text="Bitte PIN eingeben:", font=("Arial", 20))
mymy_label.pack(pady=20)

pin_eingabe = ctk.CTkEntry(master=root, placeholder_text="PIN", width=200, show="*")
pin_eingabe.pack(pady=10)

my_button = ctk.CTkButton(master=root, text="Anmelden", command=beim_klicken_passiert_das)
my_button.pack(pady=20)


# --- App starten ---

root.mainloop()