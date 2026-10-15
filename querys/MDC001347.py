QUERY_EJEC='''
    WITH V_UBICACIONES  as(
    
    select a.codubi,
        a.codpai,
        a.codpvc,
        trim(a.codest) codest,
        a.coddst,
        a.nomdst,
        b.nompvc,
        c.nomest,
        d.nompai,
        b.abrev abrpvc,
        c.nomabr abrest,
        d.abrev abrpai,
        a.nomdst || ' | ' || b.NOMPVC || ' | ' || c.nomabr as distrito_desc,
        ' ' as nomreg_atm,
        ' ' as nomarea_atm,
        ' ' as ciudadatm,
        ' ' as atm_codpai,
        ' ' as atm_codreg,
        ' ' as atm_codarea,
        ' ' as atm_codcity,
        b.filial,
        A.CODPOS codpos,
        c.nomabr_ceco
    from  vtatabdst a
    inner join vtatabpvc b
        on a.codpai = b.codpai
    and a.codest = b.codest
    and a.codpvc = b.codpvc
    inner join vtatabest c
        on a.codpai = c.codpai
    and a.codest = c.codest
    inner join vtatabpai d
        on a.codpai = d.codpai
    ), 
    
    
    TABLA_LINEAS_DISPONIBLES_1 AS
    (SELECT V.CODUBI,
            V.NOMEST DEPARTAMENTO,
            V.NOMDST DISTRITO,
            S.NUMINI,
            S.NUMFIN,
            S.CODZONA,
            COUNT(1) CANT
        FROM TELEFONIA.SERIETEL S, TELEFONIA.NUMTEL N, V_UBICACIONES V
        WHERE EXISTS (SELECT 'T'
                FROM TIPOPEDD A, OPEDD B
                WHERE A.TIPOPEDD = B.TIPOPEDD
                AND B.CODIGON = S.CODZONA
                AND A.ABREV = 'ZONATEL_NOT_AUTO')
        AND S.CODUBI = V.CODUBI
        AND N.TIPNUMTEL = 1
        AND N.ESTNUMTEL = 1
        AND TO_NUMBER(N.NUMERO) >= TO_NUMBER(S.NUMINI)
        AND TO_NUMBER(N.NUMERO) <= TO_NUMBER(S.NUMFIN)
        GROUP BY V.CODUBI, V.NOMEST, V.NOMDST, S.NUMINI, S.NUMFIN, S.CODZONA)
        
    SELECT T.DEPARTAMENTO, SUM(T.CANT) CANTIDAD
        FROM TABLA_LINEAS_DISPONIBLES_1 T
    GROUP BY T.DEPARTAMENTO
    ORDER BY SUM(T.CANT)
'''

DELETE_BASE='''
DELETE FROM FIJA_BASE_MDC001347 WHERE RESULT_TIME =TRUNC(SYSDATE,'DD')
'''


INSERTAR_BASE='''
INSERT INTO FIJA_BASE_MDC001347(
RESULT_TIME,
DEPARTAMENTO,
CANTIDAD
)
VALUES
(TRUNC(SYSDATE,'DD'),:1,:2)
'''

REPORTE= '''
SELECT A.DEPARTAMENTO,
        B.CANTIDAD AS CANTIDAD_ANTERIOR,
        A.CANTIDAD AS CANTIDAD,
        ROUND((A.CANTIDAD - B.CANTIDAD) / (B.CANTIDAD + B.CANTIDAD)*100,2) VARIACION,
        ROUND((B.CANTIDAD *
        (1 - ((A.CANTIDAD - B.CANTIDAD) / (B.CANTIDAD + B.CANTIDAD)))) / 24) DIAS
    FROM (SELECT DEPARTAMENTO, CANTIDAD
            FROM FIJA_BASE_MDC001347
            WHERE RESULT_TIME = TRUNC(SYSDATE, 'DD')) A
    LEFT JOIN (SELECT RESULT_TIME, DEPARTAMENTO, CANTIDAD
                FROM FIJA_BASE_MDC001347
                WHERE RESULT_TIME = (SELECT RESULT_TIME
                                        FROM (SELECT DISTINCT RESULT_TIME
                                                FROM FIJA_BASE_MDC001347
                                                WHERE RESULT_TIME > (SYSDATE - 10))
                                        ORDER BY RESULT_TIME DESC OFFSET 1 ROW
                                        FETCH NEXT 1 ROW ONLY)) B
        ON A.DEPARTAMENTO = B.DEPARTAMENTO    
        ORDER BY A.DEPARTAMENTO ASC
'''