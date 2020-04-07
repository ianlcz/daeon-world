import mysql.connector

mydb = mysql.connector.connect(
    host="localhost", user="root", passwd="root", database="daeon-world"
)

cursor = mydb.cursor(buffered=True)


def select(table, fetch="one", element="*", join=None):
    """
    Récupérer les données d'une table
    """
    cursor.execute(
        f"SELECT {element} FROM {table}"
        if not join
        else f"SELECT {element} FROM {table} {join}"
    )

    if fetch == "all":
        results = []
        for data in cursor.fetchall():
            results.append(dict(zip([x[0] for x in cursor.description], data)))
        return results
    else:
        for row in cursor:
            return dict(zip([x[0] for x in cursor.description], row))


def update(table, columns, where):
    """
    Modifier une donnée d'une table
    """
    cursor.execute(f"UPDATE {table} SET {columns} WHERE {where}")
    mydb.commit()


def delete(table, conditions):
    """
    Supprimer des données d'une table
    """
    cursor.execute(f"DELETE FROM {table} WHERE {conditions}")
    mydb.commit()
