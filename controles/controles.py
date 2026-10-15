from database.actions import oradb
from datetime import datetime, timedelta
import importlib.util
import pandas as pd
import sys

class Control:

    def __init__(self):
        self.dwo = oradb('oracle_dwo')
        self.ipcdb  = oradb('oracle_ipcdb')
        self.sga  = oradb('oracle_sga')

    # Resto de tu código...
    def carga_variables(self,control):
        ruta =  f'/space/tareas/Proyecto_fija_asis/querys/{control}'
        spec = importlib.util.spec_from_file_location('variables',ruta)
        modulo = importlib.util.module_from_spec(spec)
        sys.modules['variables'] = modulo
        spec.loader.exec_module(modulo)
        return modulo

    def MDC001311(self):
        var = self.carga_variables('MDC001311.py')
        self.ipcdb.execute_truncate('BASE_SGA_VOD')
        for vod_sga in self.sga.execute_query_output_chunks(var.BASE_SGA_VOD,50000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_BASE_SGA_VOD,vod_sga)
        self.ipcdb.ejecutaPaquete(var.PROCESAR_PKG_INCOGNITO)
        self.ipcdb.execute_query(var.DELETE_BASE)
        self.ipcdb.execute_query(var.INSERTAR_CONTROL)
        return self.ipcdb.excute_query_output_df(var.REPORTE)

    def MDC001321(self):
        var = self.carga_variables('MDC001321.py')
        self.ipcdb.execute_query(var.DELETE_BASE)
        for sga in self.sga.execute_query_output_chunks(var.OBTENER_BASE_SGA,50000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_BASE,sga)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base        

    def MDC001246(self):
        var = self.carga_variables('MDC001246.py')
        self.ipcdb.execute_truncate('FIJA_BSCS_IX_VELOC')
        for bscs in self.dwo.execute_query_output_chunks(var.BASE_BSCS,50000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_BASE_BSCS_IX,bscs)
        for bscsix in self.dwo.execute_query_output_chunks(var.BASE_BSCSIX,50000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_BASE_BSCS_IX,bscsix)   
        for velocidad in self.dwo.execute_query_output_chunks(var.BASE_DE_VELOCIDADES,50000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_BASE_DE_VELOCIDADES,velocidad)
        self.ipcdb.ejecutaPaquete(var.PROCESAR_PKG_INCOGNITO)
        self.ipcdb.ejecutaPaquete(var.PROCESAR_BASE)
        base = self.ipcdb.excute_query_output_df(var.OBTENER_BASE)
        return base

    def MDC001363(self):
        var = self.carga_variables('MDC001363.py')
        self.ipcdb.execute_query(var.LIMPIAR_BASE)
        for sga in self.sga.execute_query_output_chunks(var.OBTENER_BASE,50000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_BASE,sga)
        base = self.ipcdb.excute_query_output_df(var.OBTENER_REPORTE)
        return base

    def MDC001353(self):
        var = self.carga_variables('MDC001353.py')
        self.ipcdb.execute_query(var.DELETE)
        for dwo in self.dwo.execute_query_output_chunks(var.QUERY_EJECT,50000):
            self.ipcdb.Insert_Update_table(var.INSERT,dwo)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC007762(self):
        var = self.carga_variables('MDC007762.py')
        self.ipcdb.execute_query(var.DELETE_BASE)
        now = datetime.utcnow()
        dia_anterior = (now - timedelta(days=1)).strftime("%Y%m%d")
        query = var.GENERAR_BASE.format(FECHA=dia_anterior)
        for dwo in self.dwo.execute_query_output_chunks(query,50000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_BASE,dwo)
        base = self.ipcdb.excute_query_output_df(var.OBTENER_REPORTE)
        return base

    def MDC001301(self):
        var = self.carga_variables('MDC001301.py')
        self.ipcdb.execute_query(var.DELETE_BASE)
        for sga in self.sga.execute_query_output_chunks(var.BASE_SGA,50000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_BASE,sga)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC001305(self):
        var = self.carga_variables('MDC001305.py')
        self.ipcdb.execute_query(var.DELETE_BASE)
        for sga in self.sga.execute_query_output_chunks(var.BASE_SGA,50000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_BASE,sga)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC001244(self):
        var = self.carga_variables('MDC001244.py')
        self.ipcdb.execute_truncate('FIJA_CUSTOMER')
        for bscs in self.dwo.execute_query_output_chunks(var.OBTENER_CUSTOMER,50000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_CUSTOMER,bscs)
        self.ipcdb.ejecutaPaquete(var.PROCESAR_BASE)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC001249(self):
        var = self.carga_variables('MDC001249.py')
        self.ipcdb.execute_truncate('FIJA_CORTE_SERVICIO_SGA')
        for sga in self.dwo.execute_query_output_chunks(var.OBTENER_BASE_SGA,50000):
            self.ipcdb.Insert_Update_table(var.INSERT_SGA,sga)
        self.ipcdb.ejecutaPaquete(var.PROCESAR_BASE)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
       
        return  len(base)

    def MDC007760(self):
        var = self.carga_variables('MDC007760.py')
        self.ipcdb.ejecutaPaquete(var.EJECUTAR_PKG)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC001347(self):
        var = self.carga_variables('MDC001347.py') 
        self.ipcdb.execute_query(var.DELETE_BASE)
        for sga in self.sga.execute_query_output_chunks(var.QUERY_EJEC,50000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_BASE,sga)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC990001(self):
        var = self.carga_variables('MDC990001.py')
        self.ipcdb.execute_truncate('FIJA_ACUERDOS')
        self.ipcdb.execute_query(var.PREV_INFORMACION)
        for ipcdb in self.ipcdb.execute_query_output_chunks(var.OBTENER_BASE,50000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_BASE,ipcdb)

    def DDS000000(self):
        var = self.carga_variables('DDS000000.py')
        self.ipcdb.execute_truncate('FIJA_PLUME_BSCS')
        for sga in self.sga.execute_query_output_chunks(var.QUERY_OUT_PLUME,50000):
            self.ipcdb.Insert_Update_table(var.INSERT_INTO,sga)
        return self.ipcdb.excute_query_output_df(var.EXECT_QUERY)

    def MDC001260(self):
        var = self.carga_variables('MDC001260.py')
        self.dwo.execute_query('delete from dds.base_table')
        base = self.ipcdb.execute_query(var.DELETE)
        now = datetime.utcnow()
        dia_anterior = (now - timedelta(days=1)).strftime("%Y%m%d")
        self.dwo.execute_query(var.QUERY)
        for dwo in self.dwo.execute_query_output_chunks(var.QUERY_EJEC.format(FECHA=dia_anterior),1000):
            self.ipcdb.Insert_Update_table(var.INSERT,dwo)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC001309(self):
        var = self.carga_variables('MDC001309.py')
        self.ipcdb.execute_query(var.DELETE)
        now = datetime.utcnow()
        dia_anterior = (now - timedelta(days=1)).strftime("%Y%m%d")
        q01 = var.QUERY.format(FECHA=dia_anterior)
        for dwo in self.dwo.execute_query_output_chunks(q01,1000):
            self.ipcdb.Insert_Update_table(var.INSERT,dwo)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC001322(self):
        var = self.carga_variables('MDC001322.py')
        self.ipcdb.execute_query(var.DELETE)
        for dwo in self.dwo.execute_query_output_chunks(var.QUERY_EJECT,1000):
            self.ipcdb.Insert_Update_table(var.INSERT,dwo)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC007767(self):
        var = self.carga_variables('MDC007767.py')
        self.ipcdb.execute_query(var.DELETE)
        for dwo in self.dwo.execute_query_output_chunks(var.QUERY,1000):
            self.ipcdb.Insert_Update_table(var.INSERT,dwo)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC001335(self):
        var = self.carga_variables('MDC001335.py')
        self.ipcdb.execute_query(var.DELETE)
        now = datetime.utcnow()
        dia_anterior = (now - timedelta(days=1)).strftime("%Y%m%d")
        q01 = var.QUERY.format(FECHA=dia_anterior)
        for dwo in self.dwo.execute_query_output_chunks(q01,1000):
            self.ipcdb.Insert_Update_table(var.INSERT,dwo)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC008018(self):
        var = self.carga_variables('MDC008018.py')
        base = self.ipcdb.execute_query(var.DELETE)
        for dwo in self.dwo.execute_query_output_chunks(var.QUERY,1000):
            self.ipcdb.Insert_Update_table(var.INSERT,dwo)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC008019(self):
        var = self.carga_variables('MDC008019.py')
        self.ipcdb.execute_query(var.DELETE)
        now = datetime.utcnow()
        dia_anterior = (now - timedelta(days=1)).strftime("%Y%m%d")
        q01 = var.QUERY.format(FECHA=dia_anterior)
        for dwo in self.dwo.execute_query_output_chunks(q01,1000):
            self.ipcdb.Insert_Update_table(var.INSERT,dwo)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC008020(self):
        var = self.carga_variables('MDC008020.py')
        self.ipcdb.execute_query(var.DELETE)
        now = datetime.utcnow()
        dia_anterior = (now - timedelta(days=1)).strftime("%Y%m%d")
        q01 = var.QUERY.format(FECHA=dia_anterior)
        for dwo in self.dwo.execute_query_output_chunks(q01,1000):
            self.ipcdb.Insert_Update_table(var.INSERT,dwo)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC008021(self):
        var = self.carga_variables('MDC008021.py')
        base = self.ipcdb.execute_query(var.DELETE)
        for dwo in self.dwo.execute_query_output_chunks(var.QUERY,1000):
            self.ipcdb.Insert_Update_table(var.INSERT,dwo)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC008022(self):
        var = self.carga_variables('MDC008022.py')
        self.ipcdb.execute_query(var.DELETE)
        now = datetime.utcnow()
        dia_anterior = (now - timedelta(days=1)).strftime("%Y%m%d")
        data = "'^\d{2}/\d{2}/\d{4}$'"
        q01 = var.QUERY.format(FECHA=dia_anterior,DATOS=data)
        for dwo in self.dwo.execute_query_output_chunks(q01,1000):
            self.ipcdb.Insert_Update_table(var.INSERT,dwo)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC008023(self):
        var = self.carga_variables('MDC008023.py')
        self.ipcdb.execute_query(var.DELETE)
        now = datetime.utcnow()
        dia_anterior = (now - timedelta(days=1)).strftime("%Y%m%d")
        data = "'^\d{2}/\d{2}/\d{4}$'"
        q01 = var.QUERY.format(FECHA=dia_anterior,DATOS=data)
        for dwo in self.dwo.execute_query_output_chunks(q01,1000):
            self.ipcdb.Insert_Update_table(var.INSERT,dwo)
        base = self.ipcdb.excute_query_output_df(var.REPORTE)
        return base

    def MDC008031(self):
        var = self.carga_variables('MDC008031.py')
        self.ipcdb.execute_query(var.DELETE_BASE)
        for pvu in self.pvu.execute_query_output_chunks(OBTENER_BASE,10000):
            self.ipcdb.Insert_Update_table(var.INSERTAR_BASE,pvu)
        return self.ipcdb.excute_query_output_df(var.OBTENER_BASE)

    def DDS000029(self):
        var = self.carga_variables('DDS000029.py')
        self.ipcdb.execute_truncate('CUSTOMER')
        self.ipcdb.execute_truncate('FIJA_PLUME_BSCS')
        for sga in self.sga.execute_query_output_chunks(var.QUERY_EJEC_SGA,10000):
            self.ipcdb.Insert_Update_table(var.INSERT_SGA,sga)
        for dwo in self.dwo.execute_query_output_chunks(var.EJECT_BSCS,10000):
            self.ipcdb.Insert_Update_table(var.INSERTT,dwo)
        #return self.ipcdb.excute_query_output_df(var.OBTENER_BASE)
