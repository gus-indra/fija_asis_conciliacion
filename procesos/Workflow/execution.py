from procesos.database.actions import oradb
from datetime import datetime, timedelta
import importlib.util
import pandas as pd
import uuid
from config.logger_config import logger
import sys

class controles:

    def __init__(self):
        self.ipcdb = oradb('oracle_ipcdb')
        self.timeai = oradb('oracle_timeai')
        self.rtx70 = oradb('oracle_rtx70')
        self.oac = oradb('oracle_oac')
        self.dwo = oradb('oracle_dwo')
        self.dwo_ds = oradb('oracle_dwo_ds')
        self.onbs = oradb('oracle_onbs')
        self.pvu = oradb('oracle_pvu')
        self.trcker = oradb('oracle_trcker')
        self.bscsix = oradb('oracle_bscsix')

    def carga_variables(self,tabla):
        nombre_modulo = 'variables'
        ruta =  f'/space/tareas/proyecto_airflow_dev/queries/{tabla}'
        spec = importlib.util.spec_from_file_location(nombre_modulo, ruta)
        modulo = importlib.util.module_from_spec(spec)
        sys.modules[nombre_modulo] = modulo
        spec.loader.exec_module(modulo)
        return modulo

    def MDC007548(self):
        var = self.carga_variables('MDC007548.py')
        transaction_id = str(uuid.uuid4())
        self.ipcdb.execute_truncate('TMP_DDS000000_OAC')
        lote = 10000
        lotes_por_commit = 3
        lote_contador = 0
        for data in self.oac.execute_query_output_chunks_com(var.EXC_OAC,10000):
            lote_contador += 1
            commit_now = (lote_contador % lotes_por_commit == 0)
            self.ipcdb.Insert_Update_table_commit(var.INSERT_INTO_OUT_OAC,data,commit=commit_now)
        self.ipcdb.db.commit()

    def DDS000058(self):
        var = self.carga_variables('DDS000058.py')
        transaction_id = str(uuid.uuid4())
        self.dwo.ejecutaPaquete_variabes('DS.SP_TRUNCATE_TABLE_ESQUEMA',['DDS000058_BASE_COLAB'])
        data_obtener_colab = self.dwo.excute_query_output(var.QRY_OBTENER_COLAB)
        self.dwo.Insert_Update_table(var.INSERT_BASE_COLAB, data_obtener_colab)
        self.dwo.execute_query(var.QRY_OBTENER_FACT)
        data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL)
        data_id = [(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9],d[10],transaction_id) for d in data_control]
        self.ipcdb.Insert_Update_table(var.INSERT_CONTROL, data_id)
        return self.ipcdb.excute_query_output_df(var.REPORTAR.format(txid = transaction_id)), transaction_id

    def MDC000089(self):
        var = self.carga_variables('MDC000089.py')
        transaction_id = str(uuid.uuid4())
        data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
        data_id = [d + (transaction_id,) for d in data_control]
        #data_id = [(d[0],d[1],d[2],d[3],d[4],d[5],d[6],d[7],d[8],d[9],transaction_id) for d in data_control]
        self.ipcdb.Insert_Update_table(var.INSERT_CONTROL, data_id)
        return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id

    def MDC000078(self):
        var = self.carga_variables('MDC000078.py')
        transaction_id = str(uuid.uuid4())
        data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
        data_id = [d + (transaction_id,) for d in data_control]
        campos = ['CICLO_FACTURACION','PRODUCTO','CUSTOMER_ID','CO_ID','ESTADO','TICKLER_STATUS','SNCODE','DESCRIPCION_SERVICIO','SNCODE_STATUS','FECHA_ACTIVACION_SNCODE','TIPO_PRODUCTO','TMCODE','TXID']
        self.ipcdb.insertar_tabla('MDC000078',campos,data_id)
        return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id

    def MDC000001(self):
        var = self.carga_variables('MDC000001.py')
        transaction_id = str(uuid.uuid4())
        self.ipcdb.execute_query(var.QRY_OBTENER_CONTROL)
        return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR), transaction_id

    def MDC000080(self):
        var = self.carga_variables('MDC000080.py')
        transaction_id = str(uuid.uuid4())
        data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL)
        data_id = [d + (transaction_id,) for d in data_control]
        campos = ['CICLO_FACTURACION','PRODUCTO','CUSTOMER_ID','CO_ID','ESTADO','TICKLER_STATUS','SNCODE','DESCRIPCION_SERVICIO','SNCODE_STATUS','FECHA_ACTIVACION_SNCODE','TIPOPRODUCTO','TMCODE','ADV_CHARGE','TXID']
        self.ipcdb.insertar_tabla('MDC000080',campos,data_id)
        return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id

    def MDC000090(self):
        var = self.carga_variables('MDC000090.py')
        transaction_id = str(uuid.uuid4())
        data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
        data_id = [d + (transaction_id,) for d in data_control]
        campos = ['CO_ID','PRIMERA_FACTURACION','STATUS','CICLO','CUOTA','DES','TMCODE','SNCODE','OHENTDATE','OTNAME','MONTO_BASE','MONTO_FACTURADO','OBSERVACION','TXID']
        self.ipcdb.insertar_tabla('MDC000090',campos,data_id)
        return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id

    def MDC000122(self):
        var = self.carga_variables('MDC000122.py')
        transaction_id = str(uuid.uuid4())
        data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
        data_id = [d + (transaction_id,) for d in data_control]
        campos = ['PLAN','SNCODE','CO_ID','LINEA','CF_PASADO','CF_ADELANTADO','TXID']
        self.ipcdb.insertar_tabla('MDC000122',campos,data_id)
        return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id

    def MDC000126(self):
        v_control = 'MDC000126'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
        data_id = [d + (transaction_id,) for d in data_control]
        self.ipcdb.insertar_tabla_columna(v_control,data_id)
        return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id

    def MDC000145(self):
        v_control = 'MDC000145'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        data_control = self.dwo_ds.excute_query_output(var.QRY_OBTENER_CONTROL)
        data_id = [d + (transaction_id,) for d in data_control]
        self.ipcdb.insertar_tabla_columna(v_control,data_id)
        return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id

    def MDC000146(self):
        v_control = 'MDC000146'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL)
        data_id = [d + (transaction_id,) for d in data_control]
        self.ipcdb.insertar_tabla_columna(v_control,data_id)
        return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id

    def DDS000068(self):
        v_control = 'DDS000068'
        esquema_dwo = 'C27990'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        self.ipcdb.execute_query(var.QRY_VALIDA_CLI)
        data_oac = self.ipcdb.excute_query_output(var.QRY_OBTENER_OAC)
        self.dwo.ejecutaPaquete_variabes('C27990.SP_TRUNCATE_TABLE_ESQUEMA',['DDS000068_OAC'])
        self.dwo.insertar_tabla_columna('DDS000068_OAC',data_oac,esquema=esquema_dwo)
        self.dwo.execute_query(var.QRY_VALIDA_DEUDA.format(esquema = esquema_dwo))
        data_deuda = self.dwo.excute_query_output(var.QRY_OBTENER_DEUDA.format(esquema = esquema_dwo))
        self.ipcdb.execute_query('truncate table DDS000068_PRE')
        self.ipcdb.insertar_tabla_columna('DDS000068_PRE',data_deuda)
        data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
        data_id = [d + (transaction_id,) for d in data_control]
        self.ipcdb.insertar_tabla_columna(v_control,data_id)
        return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id

    def MDC000076(self):
        v_control = 'MDC000076'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000097(self):
        v_control = 'MDC000097'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000147(self):
        v_control = 'MDC000147'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC007721(self):
        v_control = 'MDC007721'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.dwo_ds.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000111(self):
        v_control = 'MDC000111'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000112(self):
        v_control = 'MDC000112'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000179(self):
        v_control = 'MDC000179'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            self.ipcdb.execute_query(var.QRY_PVU)
            self.ipcdb.execute_query('truncate table MDC000179_ONBS')
            data_onbs = self.onbs.excute_query_output(var.QRY_ONBS)
            self.ipcdb.insertar_tabla_columna('MDC000179_ONBS',data_onbs,esquema='USRDDS')
            data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna('MDC000179_2',data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def DDS000089(self):
        v_control = 'DDS000089'
        esquema_dwo = 'C27990'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            self.dwo.ejecutaPaquete_variabes('C27990.SP_TRUNCATE_TABLE_ESQUEMA',['DDS000089_OAC'])
            data_anul = self.ipcdb.excute_query_output(var.QRY_OBTENER_ANUL)
            self.dwo.insertar_tabla_columna('DDS000089_OAC',data_anul,esquema=esquema_dwo)
            data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL.format(esquema=esquema_dwo))
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})
    
    def MDC000113(self):
        v_control = 'MDC000113'
        esquema_dwo = 'C27990'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            self.dwo.ejecutaPaquete_variabes('C27990.SP_TRUNCATE_TABLE_ESQUEMA',['MDC000113_PVU'])
            data_pvu = self.pvu.excute_query_output(var.QRY_OBTENER_PVU)
            self.dwo.insertar_tabla_columna('MDC000113_PVU',data_pvu,esquema=esquema_dwo)
            data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL.format(esquema=esquema_dwo))
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC007558(self):
        v_control = 'MDC007558'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000091(self):
        v_control = 'MDC000091'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000092(self):
        v_control = 'MDC000092'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000093(self):
        v_control = 'MDC000093' #cambiar por codigo control
        v_campo_llave = 'CUSTOMER_ID' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000101(self):
        v_control = 'MDC000101' #cambiar por codigo control
        v_campo_llave = 'CUSTOMER_ID' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000117(self):
        v_control = 'MDC000117' #cambiar por codigo control
        v_campo_llave = 'CUSTOMER_ID' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000119(self):
        v_control = 'MDC000119' #cambiar por codigo control
        v_campo_llave = 'CO_ID' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000121(self):
        v_control = 'MDC000121' #cambiar por codigo control
        v_campo_llave = 'CO_ID' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000123(self):
        v_control = 'MDC000123' #cambiar por codigo control
        v_campo_llave = 'CUSTOMER_ID' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000124(self):
        v_control = 'MDC000124' #cambiar por codigo control
        v_campo_llave = 'DN_NUM' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000125(self):
        v_control = 'MDC000125' #cambiar por codigo control
        v_campo_llave = 'DN_NUM' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.rtx70.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC007539(self):
        v_control = 'MDC007539' #cambiar por codigo control
        v_campo_llave = 'CUSTOMER_ID' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.dwo.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000070(self):
        v_control = 'MDC000070' #cambiar por codigo control
        v_campo_llave = 'OHENTDATE' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000153(self):
        v_control = 'MDC000153' #cambiar por codigo control
        v_campo_llave = 'CO_ID' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            self.dwo_ds.execute_query(var.QRY_OBTENER_DATA)
            data_control = self.dwo_ds.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def DDS000104(self):
        v_control = 'DDS000104' #cambiar por codigo control
        v_campo_llave = 'NUMSUT' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            self.dwo_ds.execute_query(var.QRY_OBTENER_DATA)
            data_control = self.dwo_ds.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def DDS000105(self):
        v_control = 'DDS000105' #cambiar por codigo control
        v_campo_llave = 'LPCUNO' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def DDS000107(self):
        v_control = 'DDS000107' #cambiar por codigo control
        v_campo_llave = 'LPCUNO' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def DDS000109(self):
        v_control = 'DDS000109' #cambiar por codigo control
        v_campo_llave = 'CUSTOMER_ID' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_bscs7 = self.dwo_ds.excute_query_output(var.QRY_OBTENER_BSCS7)
            self.ipcdb.execute_query('truncate table DDS000109_BSCS7')
            self.ipcdb.insertar_tabla_columna('DDS000109_BSCS7',data_bscs7)
            data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000140(self):
        v_control = 'MDC000140' #cambiar por codigo control
        v_campo_llave = 'CUSTOMER_ID' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            self.dwo_ds.execute_query(var.QRY_OBTENER_DATA)
            data_control = self.dwo_ds.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def DDS000111(self):
        v_control = 'DDS000111' #cambiar por codigo control
        v_campo_llave = 'CUSTNUM' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_bscsix = self.dwo_ds.excute_query_output(var.QRY_OBTENER_BSCSIX)
            self.ipcdb.execute_query('truncate table DDS000111_BSCSIX')
            self.ipcdb.insertar_tabla_columna('DDS000111_BSCSIX',data_bscsix)
            data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def DDS000112(self):
        v_control = 'DDS000112' #cambiar por codigo control
        v_campo_llave = 'COD_CLI' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_trcker = self.trcker.excute_query_output(var.QRY_OBTENER_TRCKER)
            self.ipcdb.execute_query('truncate table DDS000112_TRCKER')
            self.ipcdb.insertar_tabla_columna('DDS000112_TRCKER',data_trcker)
            data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC007594(self):
        v_control = 'MDC007594' #cambiar por codigo control
        v_campo_llave = 'CO_ID' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.dwo_ds.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def DDS000115(self):
        v_control = 'DDS000115' #cambiar por codigo control
        v_campo_llave = 'LINEA_PREPAGO' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_trcker = self.trcker.excute_query_output(var.QRY_OBTENER_TRCKER)
            self.ipcdb.execute_query('truncate table DDS000115_TRCKER')
            self.ipcdb.insertar_tabla_columna('DDS000115_TRCKER',data_trcker)
            self.ipcdb.execute_query(var.QRY_OBTENER_DATA)
            data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def DDS000116(self):
        v_control = 'DDS000116' #cambiar por codigo control
        v_campo_llave = 'LINEA_PREPAGO' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def DDS000119(self):
        v_control = 'DDS000119' #cambiar por codigo control
        v_campo_llave = 'CUENTA_POSTPAGO' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_trcker = self.trcker.excute_query_output(var.QRY_OBTENER_TRCKER)
            self.ipcdb.execute_query('truncate table DDS000119_TRCKER')
            self.ipcdb.insertar_tabla_columna('DDS000119_TRCKER',data_trcker)
            self.ipcdb.execute_query(var.QRY_OBTENER_DATA)
            data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def DDS000120(self):
        v_control = 'DDS000120' #cambiar por codigo control
        v_campo_llave = 'CUENTA_POSTPAGO' #cambiar por campo llave
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control,data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC000174(self):
        v_control = 'MDC000174'
        v_campo_llave = 'CO_ID'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            self.dwo_ds.execute_query(var.QRY_OBTENER_DATA)
            data_control = self.dwo_ds.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control, data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def MDC007924(self):
        v_control = 'MDC007924'
        v_campo_llave = 'CO_ID'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_bscsix = self.bscsix.excute_query_output(var.QRY_OBTENER_DATA)
            self.dwo_ds.execute_query('truncate table MDC007924_BSCSIX')
            self.dwo_ds.insertar_tabla_columna('MDC007924_BSCSIX', data_bscsix)
            data_control = self.dwo_ds.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control, data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})

    def DDS000130(self):
        v_control = 'DDS000130'
        v_campo_llave = 'TRAV_IDTRANSACCION'
        var = self.carga_variables(f'{v_control}.py')
        transaction_id = str(uuid.uuid4())
        try:
            data_trcker = self.trcker.excute_query_output(var.QRY_OBTENER_TRCKER)
            self.ipcdb.execute_query('truncate table DDS000130_TRCKER')
            self.ipcdb.insertar_tabla_columna('DDS000130_TRCKER', data_trcker)
            data_control = self.ipcdb.excute_query_output(var.QRY_OBTENER_CONTROL)
            data_id = [d + (transaction_id,) for d in data_control]
            self.ipcdb.insertar_tabla_columna(v_control, data_id)
            return self.ipcdb.excute_query_output_df(var.QRY_REPORTAR.format(tabla_final = v_control, campo_llave = v_campo_llave, txid = transaction_id)), v_campo_llave, transaction_id
        except Exception as e:
            logger.error(f'{e}',extra={'control': v_control, 'txid': transaction_id})