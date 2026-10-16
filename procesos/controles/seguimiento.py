from database.actions import oradb
#from config.logger_config import logger

class seguimiento:

    def __init__(self):
        self.ipcdb = oradb('oracle_ipcdb')

    def get_process_data(self,codigo_control,status,tipo_ejecucion,p_orden='DESC'):
        """Proceso que devuelve colas con el estado que se envia,
            Args:
                codigo_control (String): Control que se buscara en la tabla seguimineto
                tipo_ejecucion (String): Datos para ver si es una regular --> R
                                                            validacion --> V
                status (Int): Estado en el que se encuentra el proceso
                orden (String): Para ordenar la query
        """
        try:
            QUERY_GUIA = f'''
                select id,fecha_procesar from(
                    select
                        id,
                        fecha_procesar
                    from tx_r2_log a
                    where
                        status = {status}
                        and tipo_ejecucion = '{tipo_ejecucion}'
                        and codigo_control = '{codigo_control}'
                    order by fecha_procesar {p_orden}
                ) where rownum=1
            '''
            return self.ipcdb.excute_query_output(QUERY_GUIA)
        except Exception as e:
            # logger.error(f'seguimiento.get_process_data: {e}',extra={'control': codigo_control[0][0]})
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def iniciar_seguimiento(self,num_proceso):
        """Actualiza el num_proceso que se empieza a ejecutar
            Args:
                num_proceso (Int): Identificador unico para el procceso
        """
        try:
            SQL_CONTROL  = f'''select codigo_control from tx_r2_log where id = {num_proceso}'''
            codigo_control = self.ipcdb.excute_query_output(SQL_CONTROL)
            # logger.info('Iniciando proceso de ejecución...',extra={'control': codigo_control[0][0]})
            #print('Iniciando proceso de ejecución...')
            QUERY_UPDATE_SEGUIMIENTO = f'''
                UPDATE tx_r2_log SET STATUS = 2, FECHA_INICIO = SYSDATE
                WHERE ID = {num_proceso}
            '''
            self.ipcdb.execute_query(QUERY_UPDATE_SEGUIMIENTO)
            # logger.info('Se inicio el poceso de ejecución correctamente...',extra={'control': codigo_control[0][0]})
            #print('Se inicio el poceso de ejecución correctamente...')
        except Exception as e:
            # logger.error(f'seguimiento.iniciar_seguimiento: {e}',extra={'control': codigo_control[0][0]})
            #print(f'seguimiento.iniciar_seguimiento: {e}')
            raise Exception(f'SeguimientoCargas.iniciar_seguimiento: {e}')

    def finalizar_seguimiento(self,estado,mensaje_error,ticket,total_registros,txid,num_proceso):
        """Actualiza el num_proceso que se finaliza
            Args:
                num_proceso (Int): Identificador unico para el procceso
                mensaje_error (String): Detalle para la finalizacion del proceso
                estado (String):Para señallar el estado 4 --> Finalizado con errores
                                Para señallar el estado 3 --> Finalizado correctamente
        """
        if isinstance(mensaje_error, str):
            mensaje_error = mensaje_error.replace("'", '"')
        else:
            mensaje_error = str(mensaje_error).replace("'", '"')
        try:
            SQL_CONTROL  = f'''select codigo_control from tx_r2_log where id = {num_proceso}'''
            codigo_control = self.ipcdb.excute_query_output(SQL_CONTROL)
            # logger.info(f'Finalizando proceso de ejecución -> Proceso: {num_proceso} Estado: {estado}',extra={'control': codigo_control[0][0]})
            #print(f'Finalizando proceso de ejecución -> Proceso: {num_proceso} Estado: {estado}')
            QUERY_UPDATE_SEGUIMIENTO = f'''
                UPDATE tx_r2_log SET
                    STATUS = {estado}, FECHA_FIN = SYSDATE, MENSAJE_ERROR = '{mensaje_error}',
                    TICKET = '{ticket}', TOTAL_REGISTROS = {total_registros}, TXID = '{txid}'
                WHERE ID = {num_proceso}
            '''
            self.ipcdb.execute_query(QUERY_UPDATE_SEGUIMIENTO)
        except Exception as e:
            # logger.error(f'seguimiento.finalizar_seguimiento: {e}',extra={'control': codigo_control[0][0]})
            raise Exception(f'SeguimientoCargas.finalizar_seguimiento: {e}')