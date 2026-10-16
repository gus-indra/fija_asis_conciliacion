from controles.controles import Control
from controles.seguimiento import seguimiento
# from report.report import remedy
# from report.report import envio_correo
from datetime import datetime
#from ml.detectar_anomalias import DeteccionAnomalias
#import matplotlib.pyplot as plt
#import seaborn as sns
from io import BytesIO
import base64
#import pandas as pd
import dataclasses
import sys

@dataclasses.dataclass
class Controller:

    cod_control: str
    tipo_carga: str

    def __post_init__(self):
        self.control = Control()
        self.seguimiento =seguimiento()
        # self.remedy = remedy()
        # self.envio_correo= envio_correo()

    def _init_seguimiento(self):
        """ Valida si hay cargas pendientes de ejecutar
        """
        estado_encolamiento = 0
        array_encolados = self.seguimiento.get_process_data(self.cod_control,estado_encolamiento,self.tipo_carga)
        if len(array_encolados) > 0:
            estado_encolamiento = 1
            v_cantidad = self.seguimiento.get_process_data(self.cod_control,estado_encolamiento,self.tipo_carga)
            if len(v_cantidad) == 0:
                del v_cantidad
                return array_encolados[0][0], array_encolados[0][1]
            else:
                print('Hay procesos ejecutandose')
                sys.exit()
        else:
            print('No hay cola')
            sys.exit()
    
    def MDC001311(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC001311()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001311','C27394',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC001311',len(base),base)
            self.envio_correo.enviar_correo('MDC001311',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001311',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001311','C27394',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC001321(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC001321()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001321','C27394',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC001321',len(base),base)
            self.envio_correo.enviar_correo('MDC001321',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001321',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001321','C27394',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')  

    def MDC001246(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base = self.control.MDC001246()
            print("Ejecutado")
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001246','C27394',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC001246',len(base),base)
            self.envio_correo.enviar_correo('MDC001246',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001246',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001246','C27394',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')       

    def MDC001363(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC001363()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001363','C27394',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC001363',len(base),base)
            self.envio_correo.enviar_correo('MDC001363',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001363',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001363','C27394',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC007762(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC007762()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC007762','C27394',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC007762',len(base),base)
            self.envio_correo.enviar_correo('MDC007762',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC007762',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC007762','C27394',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')
    
    def MDC001301(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC001301()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001301','C27495',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC001301',len(base),base)
            self.envio_correo.enviar_correo('MDC001301',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001301',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001301','C27495',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC001305(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC001305()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001305','C27394',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC001305',len(base),base)
            self.envio_correo.enviar_correo('MDC001305',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001305',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001305','C27394',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC001244(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC001244()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001244','C27394',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC001244',len(base.drop_duplicates(subset='CUSTOMER_ID')),base)
            self.envio_correo.enviar_correo('MDC001244',len(base.drop_duplicates(subset='CUSTOMER_ID')),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001244',inc,len(base.drop_duplicates(subset='CUSTOMER_ID'))])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001244','C27394',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base.drop_duplicates(subset='CUSTOMER_ID')),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')
            
    def MDC001353(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC001353()
            DeteccionAnomalias('MDC001353', len(base))
            # En caso de bases muy altas, y SOLO los 1 de cada mes Y antes de las 16 horas
            ahora = datetime.now()
            if ahora.hour < 10:
                self.seguimiento.reiniciar_seguimiento(v_num_proceso)
                sys.exit()
            if len(base) >= 4000 and ahora.day in (28, 29, 30, 1, 2) and ahora.hour < 16:
                self.seguimiento.reiniciar_seguimiento(v_num_proceso)
                sys.exit()
            if len(base) >= 200:
                self.seguimiento.finalizar_seguimiento(4,'Base elevada, revisar','',len(base),v_num_proceso)
                sys.exit()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001353','C27394',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            pivot_table = base.pivot_table(values='ESTSOL', index=['FECHA','DESCRIPCION'], columns='TEC', aggfunc='count')
            global_style = {
                "selector": "table, th, td",
                "props": '''
                    font-family: sans-serif;
                    border-style: solid;
                    border-color: black;
                    border-width: 1px;
                    border-collapse: collapse;
                    text-align: center;
                    width: 400px;
                '''
            }
            pivot_table = pivot_table.fillna('').round(0).astype(str)
            gg = f'{len(base)} clientes afectados.<br/><br/> {pivot_table.style.set_table_styles([global_style], axis=None).to_html()}'
            inc  = self.remedy.remedy_init('MDC001353',len(base),base)
            self.envio_correo.enviar_correo('MDC001353',gg,inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001353',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001353','C27394',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC001249(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC001249()
            if len(base)==0:
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001249','C27394',500,0,None,''])
                sys.exit()
            inc  = self.remedy.remedy_init('MDC001249',len(base.drop_duplicates(subset='CUSTOMER_ID')),base)
            self.envio_correo.enviar_correo('MDC001249',len(base.drop_duplicates(subset='CUSTOMER_ID')),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001249',inc,len(base.drop_duplicates(subset='CUSTOMER_ID'))])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001249','C27394',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base.drop_duplicates(subset='CUSTOMER_ID')),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')        

    def MDC007760(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC007760()
            if len(base)==0:
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC007760','C27394',500,0,None,''])
                sys.exit()
            inc  = self.remedy.remedy_init('MDC007760',len(base.drop_duplicates(subset='ACCOUNTNUMBER')),base)
            self.envio_correo.enviar_correo('MDC007760',len(base.drop_duplicates(subset='ACCOUNTNUMBER')),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC007760',inc,len(base.drop_duplicates(subset='ACCOUNTNUMBER'))])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC007760','C27394',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base.drop_duplicates(subset='ACCOUNTNUMBER')),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC001347(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC001347()
            DeteccionAnomalias('MDC001347', len(base))
            if len(base)==0:
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001347','C27394',500,0,None,''])
                sys.exit()
            sns.set(style="whitegrid")
            plt.figure(figsize=(10, 6))
            sns.lineplot(x='DEPARTAMENTO', y='DIAS', data=base, marker='o')
            plt.title('Stock de lineas')
            plt.xlabel('Departamento')
            plt.ylabel('Dias')
            plt.xticks(rotation=90)
            plt.legend()
            buffer = BytesIO()
            plt.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
            plt.close()
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            inc  = self.remedy.remedy_init('MDC001347',len(base),base)
            self.envio_correo.enviar_correo('MDC001347',image_base64,inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001347',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001347','C27394',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC990001(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            self.control.MDC990001()
            self.seguimiento.finalizar_seguimiento(2,'Proceso termino con exito','',0,v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def DDS000000(self):
        #v_num_proceso, v_procesar = self._init_seguimiento()
        #self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base = self.control.DDS000000()
            print(base)
            #self.seguimiento.finalizar_seguimiento(2,'Proceso termino con exito','',0,v_num_proceso)
        except Exception as e:
            #self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')        

    def MDC001260(self):
        #v_num_proceso, v_procesar = self._init_seguimiento()
        #self.seguimiento.iniciar_seguimiento(v_num_proceso)        
        try:
            base  = self.control.MDC001260()
            if len(base)==0:
                #self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001260','C27394',500,0,None,''])
                #self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)                
                sys.exit()
            print(base)
            #inc  = self.remedy.remedy_init('MDC001260',len(base.drop_duplicates(subset='CUSTOMER_ID')),base)
            #self.envio_correo.enviar_correo('MDC001260',len(base.drop_duplicates(subset='CUSTOMER_ID')),inc,base)
            #self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001260',inc,len(base.drop_duplicates(subset='CUSTOMER_ID'))])
            #self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001260','C27394',500,1,inc,''])
            #self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base.drop_duplicates(subset='CUSTOMER_ID')),v_num_proceso)
        except Exception as e:
            #self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)            
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC001309(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)        
        try:
            base  = self.control.MDC001309()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001309','E758275',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)                 
                sys.exit()
            inc  = self.remedy.remedy_init('MDC001309',len(base),base)
            self.envio_correo.enviar_correo('MDC001309',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001309',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001309','E758275',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)            
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC001322(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)        
        try:
            base  = self.control.MDC001322()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001322','E758275',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)                 
                sys.exit()
            inc  = self.remedy.remedy_init('MDC001322',len(base),base)
            self.envio_correo.enviar_correo('MDC001322',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001322',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001322','E758275',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)            
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC007767(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)        
        try:
            base  = self.control.MDC007767()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC007767','E758275',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)                 
                sys.exit()
            inc  = self.remedy.remedy_init('MDC007767',len(base),base)
            self.envio_correo.enviar_correo('MDC007767',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC007767',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC007767','E758275',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)            
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC001335(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)        
        try:
            base  = self.control.MDC001335()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001335','E758275',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)                 
                sys.exit()
            inc  = self.remedy.remedy_init('MDC001335',len(base),base)
            self.envio_correo.enviar_correo('MDC001335',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC001335',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC001335','E758275',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)            
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC008018(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)        
        try:
            base  = self.control.MDC008018()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008018','E758275',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)                 
                sys.exit()
            inc  = self.remedy.remedy_init('MDC008018',len(base),base)
            self.envio_correo.enviar_correo('MDC008018',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC008018',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008018','E758275',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)            
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC008019(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC008019()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008019','E758275',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC008019',len(base),base)
            self.envio_correo.enviar_correo('MDC008019',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC008019',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008019','E758275',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC008020(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC008020()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008020','E758275',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC008020',len(base),base)
            self.envio_correo.enviar_correo('MDC008020',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC008020',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008020','E758275',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC008021(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC008021()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008021','E758275',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC008021',len(base),base)
            self.envio_correo.enviar_correo('MDC008021',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC008021',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008021','E758275',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC008022(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC008022()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008022','E758275',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC008022',len(base),base)
            self.envio_correo.enviar_correo('MDC008022',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC008022',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008022','E758275',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC008023(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC008023()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008023','E758275',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC008023',len(base),base)
            self.envio_correo.enviar_correo('MDC008023',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC008023',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008023','E758275',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def MDC008031(self):
        v_num_proceso, v_procesar = self._init_seguimiento()
        self.seguimiento.iniciar_seguimiento(v_num_proceso)
        try:
            base  = self.control.MDC008031()
            if len(base)==0:
                self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008031','C27394',500,0,None,''])
                self.seguimiento.finalizar_seguimiento(2,'No hay base','',0,v_num_proceso)
                sys.exit()
            inc  = self.remedy.remedy_init('MDC008031',len(base),base)
            self.envio_correo.enviar_correo('MDC008031',len(base),inc,base)
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_BITACORA',['MDC008031',inc,len(base)])
            self.control.ipcdb.ejecutaPaquete_variabes('SP_REGISTRA_EJECUCION',['MDC008031','C27394',500,1,inc,''])
            self.seguimiento.finalizar_seguimiento(2,'Reportado',inc,len(base),v_num_proceso)
        except Exception as e:
            self.seguimiento.finalizar_seguimiento(3,e,'',0,v_num_proceso)
            raise Exception(f'SeguimientoCargas.get_process_data: {e}')

    def DDS000029(self):
        self.control.DDS000029()