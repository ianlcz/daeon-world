import mysql.connector
import json

mydb = mysql.connector.connect(
    host="localhost", user="root", passwd="root", database="daeon-world"
)


def select(table, fetch="all", element="*", join=None):
    """
    Récupérer les données d'une table
    """
    cursor = mydb.cursor()
    sql_requet = (
        f"SELECT {element} FROM {table}"
        if not join
        else f"SELECT {element} FROM {table} {join}"
    )
    cursor.execute(sql_requet)
    row_headers = [x[0] for x in cursor.description]

    if fetch == "one":
        return dict(zip(row_headers, cursor.fetchone()))
    elif fetch == "many":
        result = cursor.fetchmany()
    else:
        results = []
        for data in cursor.fetchall():
            results.append(dict(zip(row_headers, data)))
        return results
