BASE_SGA = '''
SELECT /*+ PARALLEL(7) */
 'DTH' AS TECNOLOGIA,
 A.CUSTOMER_ID,
 A.COD_ID,
 A.CODSOLOT,
 A.TIPTRA,
 B.DESCRIPCION,
 A.ESTSOL,
 A.CODCLI,
 'GENERADA' AS ESTADO,
 TRUNC(A.FECUSU) AS FECUSU
  FROM SOLOT A
 INNER JOIN TIPTRABAJO B
    ON A.TIPTRA = B.TIPTRA
 WHERE A.TIPTRA IN (425, 428, 432)
   AND A.ESTSOL = 10
   AND A.FECUSU < TRUNC(SYSDATE - 1)

UNION ALL

SELECT /*+ PARALLEL(7) */
 'FTTH' AS TECNOLOGIA,
 A.CUSTOMER_ID,
 A.COD_ID,
 A.CODSOLOT,
 A.TIPTRA,
 B.DESCRIPCION,
 A.ESTSOL,
 A.CODCLI,
 'GENERADA' AS ESTADO,
 TRUNC(A.FECUSU) AS FECUSU
  FROM SOLOT A
 INNER JOIN TIPTRABAJO B
    ON A.TIPTRA = B.TIPTRA
 WHERE A.TIPTRA IN (1032, 845, 843, 842)
   AND A.ESTSOL = 10
   AND A.FECUSU < TRUNC(SYSDATE - 1)

UNION ALL

SELECT /*+ PARALLEL(7) */
 'HFC' AS TECNOLOGIA,
 A.CUSTOMER_ID,
 A.COD_ID,
 A.CODSOLOT,
 A.TIPTRA,
 B.DESCRIPCION,
 A.ESTSOL,
 A.CODCLI,
 'GENERADA' AS ESTADO,
 TRUNC(A.FECUSU) AS FECUSU
  FROM SOLOT A
 INNER JOIN TIPTRABAJO B
    ON A.TIPTRA = B.TIPTRA
 WHERE A.TIPTRA IN (1014,
                    406,
                    448,
                    408,
                    677,
                    409,
                    442,
                    1015,
                    480,
                    729,
                    733,
                    731,
                    610,
                    417,
                    496,
                    410,
                    443,
                    445,
                    489,
                    444,
                    411,
                    441,
                    728,
                    732)
   AND A.ESTSOL = 10
   AND A.FECUSU < TRUNC(SYSDATE - 1)
'''


DELETE_BASE = '''
DELETE FROM FIJA_BASE_MDC001305 WHERE RESULT_TIME = TRUNC(SYSDATE,'DD')
'''
INSERTAR_BASE = '''
INSERT INTO  FIJA_BASE_MDC001305
(
  RESULT_TIME ,
  TECNOLOGIA  ,
  CUSTOMER_ID ,
  COD_ID      ,
  CODSOLOT    ,
  TIPTRA      ,
  DESCRIPCION ,
  ESTSOL      ,
  CODCLI      ,
  ESTADO      ,
  FECUSU     
) VALUES (TRUNC(SYSDATE,'DD'),:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)
'''

REPORTE = '''
SELECT TECNOLOGIA  ,
  CUSTOMER_ID ,
  COD_ID      ,
  CODSOLOT    ,
  TIPTRA      ,
  DESCRIPCION ,
  ESTSOL      ,
  CODCLI      ,
  ESTADO      ,
  FECUSU 
FROM FIJA_BASE_MDC001305 WHERE RESULT_TIME = TRUNC(SYSDATE,'DD')
'''
