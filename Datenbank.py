
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='tramspotters.ddnss.de',
        port=3306,
        user='kdm25',
        password='kdm25',
        database='kdm25_sql_uebung'
    )

# ---- Lesen ----
def Inventar_sehen():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = 'SELECT id, name, kategorie, standort, status FROM t_inventar'
        cursor.execute(sql)
        rows = cursor.fetchall()

        if not rows:
            print("Keine Datensätze gefunden.")
            return

        # Kopfzeile
        print("ID | Name | Kategorie | Standort | Status")
        print("-" * 70)

        # Zeilen ausgeben
        for row in rows:
            print(f"{row['id']} | {row['name']} | {row['kategorie']} | {row['standort']} | {row['status']}")

    except mysql.connector.Error as err:
        print(f"Datenbankfehler: {err}")
    finally:
        try:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        except NameError:
            pass

# ---- Hinzufügen ----
def Inventar_hinzufuegen(name: str, kategorie: str, standort: str, status: str):

    # einfache Validierung
    for label, value in [("name", name), ("kategorie", kategorie), ("standort", standort), ("status", status)]:
        if value is None or str(value).strip() == "":
            raise ValueError(f"Feld '{label}' darf nicht leer sein.")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO t_inventar (name, kategorie, standort, status)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (name.strip(), kategorie.strip(), standort.strip(), status.strip()))
        conn.commit()  # wichtig: Änderungen persistieren

        print(f"✅ Hinzugefügt: {name} ({kategorie}) @ {standort} – Status: {status}")
        print(f"Neue ID: {cursor.lastrowid}")  # liefert die neue ID, wenn AUTO_INCREMENT

    except mysql.connector.Error as err:
        print(f"Datenbankfehler beim Einfügen: {err}")
        # optional: conn.rollback()
    finally:
        try:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        except NameError:
            pass

# ---- (Optional) Status aktualisieren ----
def Inventar_aktualisieren_status(inventar_id: int, neuer_status: str):

    if not isinstance(inventar_id, int) or inventar_id <= 0:
        raise ValueError("inventar_id muss eine positive ganze Zahl sein.")
    if neuer_status is None or str(neuer_status).strip() == "":
        raise ValueError("neuer_status darf nicht leer sein.")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "UPDATE t_inventar SET status = %s WHERE id = %s"
        cursor.execute(sql, (neuer_status.strip(), inventar_id))
        conn.commit()

        if cursor.rowcount == 0:
            print(f"⚠️ Keine Zeile mit id={inventar_id} gefunden.")
        else:
            print(f"✅ Status für id={inventar_id} aktualisiert auf: {neuer_status}")

    except mysql.connector.Error as err:
        print(f"Datenbankfehler beim Aktualisieren: {err}")
    finally:
        try:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        except NameError:
            pass

# ---- (Optional) Löschen ----
def Inventar_loeschen(inventar_id: int):
    """
    Löscht einen Inventar-Datensatz anhand der ID.
    """
    if not isinstance(inventar_id, int) or inventar_id <= 0:
        raise ValueError("inventar_id muss eine positive ganze Zahl sein.")

    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM t_inventar WHERE id = %s"
        cursor.execute(sql, (inventar_id,))
        conn.commit()

        if cursor.rowcount == 0:
            print(f"⚠️ Keine Zeile mit id={inventar_id} gefunden.")
        else:
            print(f"🗑️ Gelöscht: Datensatz mit id={inventar_id}")

    except mysql.connector.Error as err:
        print(f"Datenbankfehler beim Löschen: {err}")
    finally:
        try:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        except NameError:
            pass

# ---- Kleines CLI-Menü für die Konsole ----
def menu():
    while True:
        print("\n=== Inventar-Tool ===")
        print("[1] Inventar anzeigen")
        print("[2] Eintrag hinzufügen")
        print("[3] Status ändern")
        print("[4] Eintrag löschen")
        print("[0] Beenden")

        choice = input("Auswahl: ").strip()

        if choice == "1":
            Inventar_sehen()
        elif choice == "2":
            name = input("Name: ").strip()
            kategorie = input("Kategorie: ").strip()
            standort = input("Standort: ").strip()
            status = input("Status: ").strip()  # z.B. 'aktiv', 'defekt', 'in Wartung'
            Inventar_hinzufuegen(name, kategorie, standort, status)
        elif choice == "3":
            try:
                inventar_id = int(input("ID: ").strip())
            except ValueError:
                print("Bitte eine gültige Zahl für die ID eingeben.")
                continue
            neuer_status = input("Neuer Status: ").strip()
            Inventar_aktualisieren_status(inventar_id, neuer_status)
        elif choice == "4":
            try:
                inventar_id = int(input("ID: ").strip())
            except ValueError:
                print("Bitte eine gültige Zahl für die ID eingeben.")
                continue
            Inventar_loeschen(inventar_id)
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Ungültige Auswahl.")

if __name__ == "__main__":
    # Direkt das Menü starten. Du kannst alternativ nur einzelne Funktionen aufrufen.
    menu()
