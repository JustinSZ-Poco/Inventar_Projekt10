import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host='tramspotters.ddnss.de',
        port=3306,
        user='kdm25',
        password='kdm25',
        database='kdm25_sql_uebung'
    )


conn = get_connection()
cursor = conn.cursor(dictionary=True)

sql = 'SELECT id, name, kategorie FROM t_einkaufsliste'
cursor.execute(sql)
rows = cursor.fetchall()