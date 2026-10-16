import dataclasses
import oracledb
import pandas as pd
from config.cfg import ConfigProyect

@dataclasses.dataclass
class oradb:
    """ Clase de conexion para db ORACLE
    """
    db_name : str

    def __post_init__(self):
        oracledb.init_oracle_client()
        config = ConfigProyect()
        self.host = config.obtiene_conexion(self.db_name).host
        self.port = config.obtiene_conexion(self.db_name).port
        self.service_name = config.obtiene_conexion(self.db_name).database
        self.user = config.obtiene_conexion(self.db_name).user
        self.password = config.obtiene_conexion(self.db_name).password
        self.dsn = oracledb.makedsn(host=self.host,
                                    port=self.port,
                                    service_name=self.service_name)
        self.db = oracledb.connect(user=self.user,
                                    password=self.password,
                                    dsn=self.dsn)
        self.cursor = self.db.cursor()

    def execute_query(self, query):
        """Proceso de ejecucion de queries
        Args:
            query(String): Query a ejecutarse
        """
        self.cursor.execute(query)
        self.db.commit()

    def execute_truncate(self, tabla):
        """Proceso de ejecucion de queries
        Args:
            tabla(String): tabla a truncar
        """
        query = f'TRUNCATE TABLE {tabla}'
        self.cursor.execute(query)

    def excute_query_output(self, query):
        """Proceso de ejecucion de queries con output - lista
        Args:
            query(String): Query a ejecutarse
        Returns:
            _type_: Array
        """
        retorno = []
        for row in self.cursor.execute(query):
            retorno.append(row)
        return retorno

    def excute_query_output_df(self, query):
        """Proceso de ejecucion de queries con output - df
        Args:
            query(String): Query a ejecutarse
        Returns:
            _type_: DataFrame
        """
        retorno = []
        for row in self.cursor.execute(query):
            retorno.append(row)
        columns = [desc[0]for desc in self.cursor.description]
        df = pd.DataFrame(retorno,columns=columns)
        return df

    def Insert_Update_table(self, query, data):
        """Actualizacion/Insercion de tabla
        Args:
            query (String): query para actualizacion
            data (_type_): datos fuente [:1, :2, :3]
        """
        self.cursor.executemany(query, data)
        self.db.commit()

    def Insert_Update_table_df(self, query, df):
        """Actualizacion/Insercion de tabla (Dataframe)
        Args:
            query (String): query para actualizacion
            df (_type_): datos fuente [:1, :2, :3]
        """
        data = df.values.tolist()
        data = [[None if pd.isna(val) else val for val in row] for row in data]
        self.cursor.executemany(query, data)
        self.db.commit()

    def ejecutaPaquete_output(self, query, params):
        """Proceso de ejecucion de paquete con output
        Args:
            query(String): Paquete a ejecutarse
            params(Array): variables del paquete
        Returns:
            _type_: Array
        """
        l_cur = self.cursor.var(oracledb.CURSOR)
        params.append(l_cur)
        l_query = self.cursor.callproc(query, params)
        l_results = l_query[-1]
        objectsArray = []
        for row in l_results.fetchall():
            objectsArray.append(row)
        return objectsArray

    def ejecutaPaquete_variabes(self, query, variables):
        """Proceso de ejecucion de paquete
        Args:
            query(String): Paquete a ejecutarse
            variables(Array): variables del paquete
        """
        self.cursor.callproc(query, variables)

    def ejecutaPaquete(self, query):
        """Proceso de ejecucion de paquete
        Args:
            query(String): Paquete a ejecutarse
            variables(Array): variables del paquete
        """
        self.cursor.callproc(query)

    def execute_query_output_chunks(self, query, chunks):
        self.cursor.execute(query)
        while True:
            rows = self.cursor.fetchmany(chunks)
            if not rows:
                break  
            yield rows