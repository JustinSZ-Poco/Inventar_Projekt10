
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host='tramspotters.ddnss.de',
        port=3306,
        user='kdm25',
        password='kdm25',
        database='kdm25_sql_uebung'
    )

def main():
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
        print("ID | Name | Kategorie")
        print("-" * 40)

        # Zeilen ausgeben
        for row in rows:
            print(f"{row['id']} | {row['name']} | {row['kategorie']} | {row['standort']} | {row['status']}")

    except mysql.connector.Error as err:
        print(f"Datenbankfehler: {err}")
    finally:
        # Ressourcen sauber schließen
        try:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()
        except NameError:
            pass

if __name__ == "__main__":
    main()
