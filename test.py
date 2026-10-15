import oracledb

CONFIG = {
    "user": "energy_app",
    "password": "EnergyApp_2026",
    "dsn": "127.0.0.1:1521/XEPDB1",
}

SQL = """
SELECT
    USER AS usuario,
    SYS_CONTEXT('USERENV', 'SERVICE_NAME') AS servicio,
    SYSDATE AS fecha_servidor
FROM dual
"""

def main():
    try:
        with oracledb.connect(**CONFIG) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute(SQL)

                columnas = [columna[0] for columna in cursor.description]

                for fila in cursor:
                    print(dict(zip(columnas, fila)))

    except oracledb.Error as error:
        print(f"Error de Oracle: {error}")
        raise


if __name__ == "__main__":
    main()