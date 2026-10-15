OBTENER_BASE ='''
with TempExpediente2 AS
 (
  
  SELECT SAC.CONTN_NUMERO_SEC AS Sec,
          SAC.CONTN_NUMERO_CONTRATO AS NroContrato,
          SEV.SEVN_PEDIN_SINERGIA AS NroPedido,
          PRO.PRDC_CODIGO AS CodTipoProducto,
          'POSTPAGO' AS Producto,
          DECODE(SAC.CONTV_MOTIVO_MIG,
                 NULL,
                 'VENTA NORMAL / ALTA',
                 104,
                 'PORT IN',
                 21,
                 'MIGRACION PRE A POST',
                 'VENTA NORMAL / ALTA') AS Motivo,
          PRO.PRDC_CODIGO AS CodTipoProducto,
          SDE.TELEFONO AS Linea,
          PRO.PRDV_DESCRIPCION AS TipoProducto,
          SAD.DOCV_DESCRIPCION AS NombreDocumento,
          SAC.CONTV_NRO_DOC_CLIENTE AS Numerodocumento,
          TRUNC(SEV.SEVD_FECHA_CREACION, 'DD') AS ExpeCreation,
          SEV.SEVD_FECHA_CREACION AS ExpeCreationDate,
          SEV.SEVN_ID AS SevId,
          SEV.SEVN_TIPO_EXPEDIENTE AS TipoExpediente,
          CASE
            WHEN (SELECT MIN(BIOM_CODBIO)
                    FROM usrpvu.BIOMT_BIOMETRIA BB2
                   WHERE BB2.BIOM_IDPADRE = BB.BIOM_IDPADRE
                     AND BB2.BIOM_CODBIO = '70006') = '70006' THEN
             '2'
            ELSE
             '1'
          END AS TipoExpedienteCorrecto
    FROM USRPVU.SISACT_EXPEDIENTES_VENTA  SEV
   INNER JOIN USRPVU.SISACT_AP_CONTRATO_Det SDE
      ON SDE.ID_CONTRATO = SEV.SEVV_ID_CONTRATO
   INNER JOIN USRPVU.SISACT_AP_CONTRATO SAC
      ON SAC.CONTN_NUMERO_CONTRATO = SEV.SEVV_ID_CONTRATO
   INNER JOIN USRPVU.SISACT_AP_DOCUMENTO SAD
      ON SAD.DOCC_CODIGO = SAC.CONTC_TIPO_DOC_CLIENTE
   INNER JOIN USRPVU.SISACT_AP_PRODUCTO PRO
      ON PRO.PRDC_CODIGO = SEV.SEVV_PRODUCTO
    LEFT JOIN USRPVU.BIOMT_GENDOC BIO
      ON BIO.GDOC_NROSEC = SAC.CONTN_NUMERO_SEC
    LEFT JOIN USRPVU.BIOMT_GENDOC_28574 BG2
      ON BG2.GDOC_NROSEC = SAC.CONTN_NUMERO_SEC
    LEFT JOIN USRPVU.BIOMT_BIOMETRIA BB
      ON BIO.GDOC_IDPADRE = BB.BIOM_IDPADRE
      OR BG2.GDOC_IDPADRE = BB.BIOM_IDPADRE
   WHERE trunc(SEV.SEVD_FECHA_CREACION, 'DD') >= trunc(SYSDATE - 7, 'DD')
     AND trunc(SEV.SEVD_FECHA_CREACION, 'DD') < trunc(SYSDATE, 'DD')
     AND SEVN_TIPO_PRODUCTO = '01'
     AND SAC.CONTC_ESTADO NOT IN ('4')
     AND SEV.SEVV_ID_CONTRATO <> '6655072'
  )

SELECT T.SEC                    AS Sec,
       T.NroContrato            AS NroContrato,
       T.NroPedido              AS NroPedido,
       T.Producto               AS Producto,
       T.Motivo                 AS Motivo,
       T.linea                  AS Linea,
       T.tipoproducto           AS TipoProducto,
       T.nombredocumento        AS NombreDocumento,
       T.numerodocumento        AS NumeroDocumento,
       T.expecreationdate       AS ExpeCreationDate,
       T.tipoexpediente         AS TipoExpediente,
       T.tipoexpedientecorrecto AS TipoExpedienteCorrecto
  FROM TempExpediente2 T
 WHERE T.TIPOEXPEDIENTE <> T.TipoExpedienteCorrecto
   and T.TIPOPRODUCTO <> 'MOVIL'  
'''

INSERTAR_BASE = '''
INSERT INTO FIJA_BASE_MDC008029
  (RESULT_TIME,
   SEC,
   NROCONTRATO,
   NROPEDIDO,
   PRODUCTO,
   MOTIVO,
   LINEA,
   TIPOPRODUCTO,
   NOMBREDOCUMENTO,
   NUMERODOCUMENTO,
   EXPECREATIONDATE,
   TIPOEXPEDIENTE,
   TIPOEXPEDIENTECORRECTO)
VALUES
  (TRUNC(SYSDATE, 'DD'), :1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12)
'''
DELETE_BASE='''
DELETE FROM FIJA_BASE_MDC008031 WHERE RESULT_TIME = TRUNC(SYSDATE,'DD')
'''
OBTENER_BASE ='''
SELECT  SEC,
        NROCONTRATO,
        NROPEDIDO,
        PRODUCTO,
        MOTIVO,
        LINEA,
        TIPOPRODUCTO,
        NOMBREDOCUMENTO,
        NUMERODOCUMENTO,
        EXPECREATIONDATE,
        TIPOEXPEDIENTE,
        TIPOEXPEDIENTECORRECTO
        FROM FIJA_BASE_MDC008031 WHERE RESULT_TIME = TRUNC(SYSDATE,'DD')
'''