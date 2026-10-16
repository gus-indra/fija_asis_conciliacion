"""Desarrollado por C26734
Dios nos ilumine si el proceso falla
"""
import argparse
import logging 
import sys 
 
from procesos.controller import Controller 
 
CONTROLES = ( 
    "MDC001311", "MDC001321", "MDC001246", "MDC001305", 
    "MDC007760", "MDC001249", "MDC001363", "MDC007762", 
    "MDC001301", "MDC001244", "MDC001322", "MDC001347", 
    "MDC001353", "DDS000000", "MDC001260", "MDC001309", 
    "MDC007767", "MDC001335", "MDC008018", "MDC008019", 
    "MDC008020", "MDC008021", "MDC008022", "MDC008023", 
    "MDC008031", "DDS000029", 
) 

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

def crear_parser(): 
    parser = argparse.ArgumentParser( 
        prog="Proyecto ONE FIJA", 
        description="Procesos FIJA - Conciliaciones", 
    ) 
    parser.add_argument("-c", "--control", choices=CONTROLES, required=True) 
    parser.add_argument("-tc", "--tipo-carga", choices=("C", "R"), required=True) 
    parser.add_argument("--run-id", required=True) 
    parser.add_argument("--interval-start", required=True) 
    parser.add_argument("--interval-end", required=True) 
    return parser 
 

def ejecutar_control(controller, control): 
    metodo = getattr(controller, control, None) 
    if not callable(metodo): 
        raise AttributeError(f"Control no implementado: {control}") 
    return metodo() 



def main(): 
    args = crear_parser().parse_args() 
    logging.basicConfig( 
        level=logging.INFO, 
        format="%(asctime)s %(levelname)s %(name)s %(message)s", 
    ) 
    logger = logging.getLogger("Proyecto ONE fija_asis, Conciliaciones") 
    print(f"Iniciando ejecución del control: {args.run_id}")
    try: 
        controller = Controller( 
            cod_control=args.control, 
            tipo_carga=args.tipo_carga, 
            run_id=args.run_id, 
            interval_start=args.interval_start, 
            interval_end=args.interval_end, 
        ) 
        resultado = ejecutar_control(controller, args.control) 
        filas = len(resultado) if resultado is not None else 0 
        logger.info( 
            "control=%s run_id=%s estado=SUCCESS filas=%s", 
            args.control, args.run_id, filas, 
        ) 
        return 0 
    except Exception: 
        logger.exception( 
            "control=%s run_id=%s estado=FAILED", 
            args.control, args.run_id, 
        ) 
        return 1 
 
 
if __name__ == "__main__": 
    sys.exit(main()) 
