"""Desarrollado por C26734
Dios nos ilumine si el proceso falla
"""
import argparse
import sys
from controller import Controller

def ejecutar_control(controller, control):
    __init = getattr(controller, control, None)
    if callable(__init):
        __init()
    else:
        print(f"No se encontró : {control}")
        
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.usage = 'Proyecto ONE FIJA'
    parser.description = 'Procesos para FIJA,' \
                        'Conciliaciones'

    controles =['MDC001311','MDC001321','MDC001246','MDC001305','MDC007760','MDC001249',
                'MDC001363','MDC007762','MDC001301','MDC001244','MDC001322','MDC001347',
                'MDC001353','DDS000000','MDC001260','MDC001309','MDC007767','MDC001335',
                'MDC008018','MDC008019','MDC008020','MDC008021','MDC008022','MDC008023',
                'DDS000000','MDC008031','DDS000029']

    parser.add_argument('-c', '--control',
                        choices=controles,
                        help='Informacion de la plataforma')
                        

    parser.add_argument('-tc', '--tipo_carga',
                        choices=['C','R'],
                        help='Proceso de Carga')

    args = parser.parse_args()

    print(f"Control: {args.control}")
    print(f"Tipo de Carga: {args.tipo_carga}")
    controller = Controller(cod_control=args.control,
                            tipo_carga=args.tipo_carga) 

    if args.control is not None:
        ejecutar_control(controller, args.control)

# /space/tareas/Proyecto_fija_asis/venv/bin/python /space/tareas/Proyecto_fija_asis/main.py -c DDS000029 -tc C