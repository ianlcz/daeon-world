import mysql.connector

mydb = mysql.connector.connect(
    host="localhost", user="root", passwd="root", database="daeon-world"
)


def select(table, fetch="all", element="*", join=None):
    """
    Récupérer les données d'une table.
    """
    cursor = mydb.cursor()
    sql_requet = (
        f"SELECT {element} FROM {table}"
        if not join
        else f"SELECT {element} FROM {table} {join}"
    )
    cursor.execute(sql_requet)
    row_headers = [x[0] for x in cursor.description]
    result = (
        cursor.fetchone()
        if fetch == "one"
        else cursor.fetchmany()
        if fetch == "many"
        else cursor.fetchall()
    )
    return dict(zip(row_headers, result))
