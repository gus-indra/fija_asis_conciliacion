# BASE_BSCS = '''
#     with 
    # base_velocidades as
    # (
    #       select a.servv_id_bscs     as sncode_vel,
    #              a.servv_descripcion,
    #              a.servv_capacidad   as velocidad,
    #              e.descripcion       as etiqueta,
    #              d.abrev,
    #              c.idservicio_sisact,
    #              d.codsrv,
    #              e.idconfigitw
    #         from dmred.pvu_sisact_ap_servicio a
    #   inner join dws.sa_servicio_sisact         c on c.idservicio_sisact = a.servv_codigo
    #   inner join dws.sa_tystabsrv               d on d.codsrv            = c.codsrv
    #   inner join dmred.sgaprd_configuracion_itw e on to_char(e.idconfigitw) = d.codigo_ext
    # ),
    # base_clientes as 
    # (     SELECT CU.PRGCODE,
    #              CA.CUSTOMER_ID,
    #              CA.CO_ID,
    #              CH.CH_VALIDFROM,
    #              CH.CH_STATUS,
    #              CA.PLCODE,
    #              CA.TMCODE,
    #              CU.BILLCYCLE
    #         FROM DMRED.CONTRACT_ALL CA
    #   INNER JOIN DMRED.CONTRACT_HISTORY CH ON CA.CO_ID = CH.CO_ID
    #   INNER JOIN DMRED.CUSTOMER_ALL     CU ON CU.CUSTOMER_ID = CA.CUSTOMER_ID
    #   INNER JOIN DWS.SA_SOLOT SOL ON SOL.CUSTOMER_ID = CU.CUSTOMER_ID
    #                              AND SOL.ESTSOL     IN (12,29)
    #                              AND SOL.FECULTEST  >= TRUNC(SYSDATE -1) 
    #                              AND SOL.FECULTEST  <  TRUNC(SYSDATE)
    #        WHERE CA.PLCODE       =  1000 -- FIJA
    #          AND CA.SCCODE       =  6
    #          AND CH.CH_STATUS    =  'a'
    #          AND CH.CH_PENDING   IS NULL
    #          AND CU.PRGCODE      IN ('2', '5')
    #          AND CH.CH_VALIDFROM <  TRUNC(SYSDATE)
    #          AND ca.tmcode       not in (1497) -- Telefonia  -- FP@18/12/2025
    #          AND CH.CH_SEQNO     =  (SELECT MAX(CH2.CH_SEQNO) FROM DMRED.CONTRACT_HISTORY CH2 WHERE CH2.CO_ID = CH.CO_ID)
    # ),
    # base_servicio_bscs as
    # (
    #       select ps.co_id
    #            , mp.des
    #            , ps.sncode
    #            , ps.entry_date
    #            , sh.status
    #         from dmred.PROFILE_SERVICE ps
    #            , dmred.PR_SERV_STATUS_HIST sh
    #            , DMRED.MPUSNTAB mp
    #        where 1 = 1
    #          and ps.CO_ID = sh.co_id
    #          and ps.sncode = sh.sncode
    #          and ps.status_histno = sh.histno
    #          and sh.status   not in ('D', 'S')
    #          and ps.sncode = mp.sncode
    # )
    # select 'AS IS' as flujo
    #      , bf.PRGCODE
    #      , bf.customer_id
    #      , bf.co_id
    #      , bf.CH_VALIDFROM
    #      , bf.CH_STATUS
    #      , bf.PLCODE
    #      , bf.TMCODE
    #      , bf.BILLCYCLE
    #      , bf.DES
    #      , bf.VELOCIDAD
    #      , bf.STATUS
    #      , bf.ETIQUETA
    #      , bf.SNCODE
    #      , bf.TECH
    #   from (
    #         select bv.*
    #              , bs.*
    #              , bc.CH_VALIDFROM
    #              , bc.CH_STATUS
    #              , bc.PLCODE
    #              , bc.TMCODE
    #              , bc.BILLCYCLE
    #              , bc.customer_id
    #              , bc.prgcode
    #              , row_number() over(partition by bs.co_id order by bs.entry_date desc) as item
    #              , CASE WHEN bs.DES     LIKE '%FTTH%' THEN 'FTTH'
    #                     WHEN bs.DES NOT LIKE '%FTTH%' THEN 'HFC'
    #                                                   ELSE 'OTRO'
    #                 END TECH
    #           from base_clientes bc
    #              , base_servicio_bscs bs
    #              , base_velocidades bv
    #          where 1 = 1 
    #            and bc.co_id       = bs.co_id
    #            and bs.sncode      = bv.sncode_vel
    #            and bv.velocidad  is not null
    #            and bv.etiqueta not in ('JANUS', 'CBIO_PROD')
    #        ) bf
    #  where bf.item = 1
# '''

# BASE_BSCSIX = '''
# WITH CONTRACT_SEQNO AS
#     (SELECT A.CO_ID, MAX(A.CH_SEQNO) CH_SEQNO
#         FROM DMRED.BSCSIX_CONTRACT_HISTORY A
#     WHERE CO_ID IN (SELECT DISTINCT CA.CO_ID
#                         FROM DMRED.BSCSIX_CUSTOMER_ALL CU
#                         INNER JOIN DMRED.BSCSIX_CONTRACT_ALL CA
#                         ON CA.CUSTOMER_ID = CU.CUSTOMER_ID
#                         WHERE CA.PLCODE = 1007
#                         AND CA.SCCODE = 6
#                         AND CA.TMCODE = 45
#                         AND CU.PRGCODE IN ('2', '5'))
#     GROUP BY CO_ID),
# VELOCIDADES AS
# (SELECT PO_ID, VELOCIDAD
#     FROM (SELECT CBV_POIDADICIONAL PO_ID, TO_NUMBER(MAX(SERVV_CAPACIDAD))  VELOCIDAD
#             FROM DWS.SA_CB_SERVICIOS CB
#             LEFT JOIN DWS.SA_TYSTABSRV T
#             ON T.CODIGO_EXT = CB.CBV_COD_EXT
#             LEFT JOIN DWS.SA_SERVICIO_SISACT SS
#             ON T.CODSRV = SS.CODSRV
#             LEFT JOIN DMRED.PVU_SISACT_AP_SERVICIO SA
#             ON SA.SERVV_CODIGO = SS.IDSERVICIO_SISACT
#         GROUP BY CBV_POIDADICIONAL)
# WHERE VELOCIDAD IS NOT NULL),
#     BASSE AS
#     (SELECT /*+ PARALLEL (8) */
#     DISTINCT DAT.*,
#             MP.DES,
#             BH.BILLCYCLE,
#             SH.STATUS,
#             SH.SNCODE,
#             MM.EXTERNAL_SERVICE_PACKAGE_NAME,
#             CASE
#                 WHEN MP.DES LIKE '%FTTH%' THEN
#                 'FTTH'
#                 WHEN MP.DES NOT LIKE '%FTTH%' THEN
#                 'HFC'
#                 ELSE
#                 'OTRO'
#             END TECH
#         FROM (
#             SELECT CU.PRGCODE,
#                     CA.CUSTOMER_ID,
#                     CA.CO_ID,
#                     CH.CH_VALIDFROM,
#                     CH.CH_STATUS,
#                     CA.PLCODE,
#                     CA.TMCODE
#                 FROM DMRED.BSCSIX_CONTRACT_ALL CA
#             INNER JOIN DMRED.BSCSIX_CONTRACT_HISTORY CH
#                 ON CA.CO_ID = CH.CO_ID
#             INNER JOIN DMRED.BSCSIX_CUSTOMER_ALL CU
#                 ON CU.CUSTOMER_ID = CA.CUSTOMER_ID
#             INNER JOIN DMRED.BSCSIX_CCONTACT_ALL CCA
#                 ON CCA.CUSTOMER_ID = CU.CUSTOMER_ID
#             INNER JOIN CONTRACT_SEQNO CH2
#                 ON CH.CO_ID = CH2.CO_ID
#                 AND CH2.CH_SEQNO = CH.CH_SEQNO
#             WHERE CA.PLCODE = 1007
#                 AND CA.SCCODE = 6
#                 AND CA.TMCODE = 45
#                 AND CH.CH_PENDING IS NULL
#                 AND CU.PRGCODE IN ('2', '5')
#                 AND CH.CH_VALIDFROM < TRUNC(SYSDATE)) DAT
#     INNER JOIN DMRED.BSCSIX_PROFILE_SERVICE PS
#         ON PS.CO_ID = DAT.CO_ID
#     INNER JOIN DMRED.BSCSIX_MPUSNTAB MP
#         ON PS.SNCODE = MP.SNCODE
#     INNER JOIN DMRED.BSCSIX_PR_SERV_SPCODE_HIST PP
#         ON PP.CO_ID = PS.CO_ID
#         AND PP.HISTNO = PS.SPCODE_HISTNO
#         LEFT JOIN DWS.SA_BSCSIX_MPUSPTAB MM
#         ON PP.SPCODE = MM.SPCODE
#     INNER JOIN DMRED.BSCSIX_PR_SERV_STATUS_HIST SH
#         ON PS.CO_ID = SH.CO_ID
#         AND PS.SNCODE = SH.SNCODE
#         AND PS.STATUS_HISTNO = SH.HISTNO
#     INNER JOIN (SELECT CUSTOMER_ID,MAX(SEQNO) SEQNO , MAX(BILLCYCLE)KEEP(DENSE_RANK LAST ORDER BY  SEQNO) BILLCYCLE
#     FROM DWS.SA_BILLCYCLE_ASSIGNMENT_HISTORY
#     GROUP BY CUSTOMER_ID) BH
#     ON BH.CUSTOMER_ID =DAT.CUSTOMER_ID
#     WHERE PS.SRV_SUBTYPE = 'J'
#         AND SH.STATUS = 'A'
#         AND MM.PRODUCTOFFERING_TYPE IN ('O', 'A')
#         AND DAT.CH_STATUS = 'a')
#     SELECT 'ONE FIJA' FLUJO,
#         PRGCODE,
#         CUSTOMER_ID,
#         CO_ID,
#         CH_VALIDFROM,
#         CH_STATUS,
#         PLCODE,
#         TMCODE,
#         BILLCYCLE,
#         DES,
#         VELOCIDAD,
#         STATUS,
#         PO_ID,
#         SNCODE,
#         TECH
#     FROM (SELECT A.*,
#                 B.*,
#                 ROW_NUMBER() OVER(PARTITION BY CUSTOMER_ID ORDER BY TO_NUMBER(VELOCIDAD) DESC) RN
#             FROM BASSE A
#             LEFT JOIN VELOCIDADES B
#                 ON A.EXTERNAL_SERVICE_PACKAGE_NAME = B.PO_ID
#             WHERE B.VELOCIDAD IS NOT NULL)
#     WHERE RN = 1
# '''

BASE_BSCS = '''
    with 
    base_velocidades as
    (
          select a.servv_id_bscs     as sncode_vel,
                 a.servv_descripcion,
                 a.servv_capacidad   as velocidad,
                 e.descripcion       as etiqueta,
                 d.abrev,
                 c.idservicio_sisact,
                 d.codsrv,
                 e.idconfigitw
            from dmred.pvu_sisact_ap_servicio a
      inner join dws.sa_servicio_sisact         c on c.idservicio_sisact = a.servv_codigo
      inner join dws.sa_tystabsrv               d on d.codsrv            = c.codsrv
      inner join dmred.sgaprd_configuracion_itw e on to_char(e.idconfigitw) = d.codigo_ext
    ),
    base_clientes as 
    (     SELECT CU.PRGCODE,
                 CA.CUSTOMER_ID,
                 CA.CO_ID,
                 CH.CH_VALIDFROM,
                 CH.CH_STATUS,
                 CA.PLCODE,
                 CA.TMCODE,
                 CU.BILLCYCLE
            FROM DMRED.CONTRACT_ALL CA
      INNER JOIN DMRED.CONTRACT_HISTORY CH ON CA.CO_ID = CH.CO_ID
      INNER JOIN DMRED.CUSTOMER_ALL     CU ON CU.CUSTOMER_ID = CA.CUSTOMER_ID
      INNER JOIN DWS.SA_SOLOT SOL ON SOL.CUSTOMER_ID = CU.CUSTOMER_ID
                                 AND SOL.ESTSOL     IN (12,29)
                                 AND SOL.FECULTEST  >= TRUNC(SYSDATE -1) 
                                 AND SOL.FECULTEST  <  TRUNC(SYSDATE)
           WHERE CA.PLCODE       =  1000 -- FIJA
             AND CA.SCCODE       =  6
             AND CH.CH_STATUS    =  'a'
             AND CH.CH_PENDING   IS NULL
             AND CU.PRGCODE      IN ('2', '5')
             AND CH.CH_VALIDFROM <  TRUNC(SYSDATE)
             AND ca.tmcode       not in (1497) -- Telefonia  -- FP@18/12/2025
             AND CH.CH_SEQNO     =  (SELECT MAX(CH2.CH_SEQNO) FROM DMRED.CONTRACT_HISTORY CH2 WHERE CH2.CO_ID = CH.CO_ID)
    ),
    base_servicio_bscs as
    (
          select ps.co_id
               , mp.des
               , ps.sncode
               , ps.entry_date
               , sh.status
            from dmred.PROFILE_SERVICE ps
               , dmred.PR_SERV_STATUS_HIST sh
               , DMRED.MPUSNTAB mp
           where 1 = 1
             and ps.CO_ID = sh.co_id
             and ps.sncode = sh.sncode
             and ps.status_histno = sh.histno
             and sh.status   not in ('D', 'S')
             and ps.sncode = mp.sncode
    )
    select 'AS IS' as flujo
         , bf.PRGCODE
         , bf.customer_id
         , bf.co_id
         , bf.CH_VALIDFROM
         , bf.CH_STATUS
         , bf.PLCODE
         , bf.TMCODE
         , bf.BILLCYCLE
         , bf.DES
         , bf.VELOCIDAD
         , bf.STATUS
         , bf.ETIQUETA
         , bf.SNCODE
         , bf.TECH
      from (
            select distinct 
                   bv.*
                 , bs.*
                 , bc.CH_VALIDFROM
                 , bc.CH_STATUS
                 , bc.PLCODE
                 , bc.TMCODE
                 , bc.BILLCYCLE
                 , bc.customer_id
                 , bc.prgcode
                 , dense_rank() over(partition by bs.co_id order by to_number(bv.velocidad) desc, bs.entry_date desc) as item
                 , CASE WHEN bs.DES     LIKE '%FTTH%' THEN 'FTTH'
                        WHEN bs.DES NOT LIKE '%FTTH%' THEN 'HFC'
                                                      ELSE 'OTRO'
                    END TECH
              from base_clientes bc
                 , base_servicio_bscs bs
                 , base_velocidades bv
             where 1 = 1 
               and bc.co_id       = bs.co_id
               and bs.sncode      = bv.sncode_vel
               and bv.velocidad  is not null
               and bv.etiqueta not in ('JANUS', 'CBIO_PROD')
           ) bf
     where bf.item = 1
'''

BASE_BSCSIX = '''
WITH CONTRACT_SEQNO AS
    (SELECT A.CO_ID, MAX(A.CH_SEQNO) CH_SEQNO
        FROM DMRED.BSCSIX_CONTRACT_HISTORY A
    WHERE CO_ID IN (SELECT DISTINCT CA.CO_ID
                        FROM DMRED.BSCSIX_CUSTOMER_ALL CU
                        INNER JOIN DMRED.BSCSIX_CONTRACT_ALL CA
                        ON CA.CUSTOMER_ID = CU.CUSTOMER_ID
                        WHERE CA.PLCODE = 1007
                        AND CA.SCCODE = 6
                        AND CA.TMCODE = 45
                        AND CU.PRGCODE IN ('2', '5'))
    GROUP BY CO_ID),
VELOCIDADES AS
(SELECT PO_ID, VELOCIDAD
    FROM (SELECT CBV_POIDADICIONAL PO_ID, TO_NUMBER(MAX(SERVV_CAPACIDAD))  VELOCIDAD
            FROM DWS.SA_CB_SERVICIOS CB
            LEFT JOIN DWS.SA_TYSTABSRV T
            ON T.CODIGO_EXT = CB.CBV_COD_EXT
            LEFT JOIN DWS.SA_SERVICIO_SISACT SS
            ON T.CODSRV = SS.CODSRV
            LEFT JOIN DMRED.PVU_SISACT_AP_SERVICIO SA
            ON SA.SERVV_CODIGO = SS.IDSERVICIO_SISACT
        GROUP BY CBV_POIDADICIONAL)
WHERE VELOCIDAD IS NOT NULL),
    BASSE AS
    (SELECT /*+ PARALLEL (8) */
    DISTINCT DAT.*,
            MP.DES,
            BH.BILLCYCLE,
            SH.STATUS,
            SH.SNCODE,
            MM.EXTERNAL_SERVICE_PACKAGE_NAME,
            CASE
                WHEN MP.DES LIKE '%FTTH%' THEN
                'FTTH'
                WHEN MP.DES NOT LIKE '%FTTH%' THEN
                'HFC'
                ELSE
                'OTRO'
            END TECH
        FROM (
            SELECT CU.PRGCODE,
                    CA.CUSTOMER_ID,
                    CA.CO_ID,
                    CH.CH_VALIDFROM,
                    CH.CH_STATUS,
                    CA.PLCODE,
                    CA.TMCODE
                FROM DMRED.BSCSIX_CONTRACT_ALL CA
            INNER JOIN DMRED.BSCSIX_CONTRACT_HISTORY CH
                ON CA.CO_ID = CH.CO_ID
            INNER JOIN DMRED.BSCSIX_CUSTOMER_ALL CU
                ON CU.CUSTOMER_ID = CA.CUSTOMER_ID
            INNER JOIN DMRED.BSCSIX_CCONTACT_ALL CCA
                ON CCA.CUSTOMER_ID = CU.CUSTOMER_ID
            INNER JOIN CONTRACT_SEQNO CH2
                ON CH.CO_ID = CH2.CO_ID
                AND CH2.CH_SEQNO = CH.CH_SEQNO
            INNER JOIN DWS.SA_SOLOT SOL
                ON SOL.CUSTOMER_ID = CU.CUSTOMER_ID
                AND SOL.ESTSOL IN (12,29)
                AND SOL.FECULTEST >= TRUNC(SYSDATE -1) AND SOL.FECULTEST < TRUNC(SYSDATE)
            WHERE CA.PLCODE = 1007
                AND CA.SCCODE = 6
                AND CA.TMCODE = 45
                AND CH.CH_PENDING IS NULL
                AND CU.PRGCODE IN ('2', '5')
                AND CH.CH_VALIDFROM < TRUNC(SYSDATE)) DAT
    INNER JOIN DMRED.BSCSIX_PROFILE_SERVICE PS
        ON PS.CO_ID = DAT.CO_ID  AND PS.STATUS_HISTNO = (SELECT MAX(PS2.STATUS_HISTNO) 
                                                                                                 FROM DMRED.PROFILE_SERVICE PS2 
                                                                                                WHERE PS2.CO_ID = PS.CO_ID) -- FP@18/12/2025
    INNER JOIN DMRED.BSCSIX_MPUSNTAB MP
        ON PS.SNCODE = MP.SNCODE
    INNER JOIN DMRED.BSCSIX_PR_SERV_SPCODE_HIST PP
        ON PP.CO_ID = PS.CO_ID
        AND PP.HISTNO = PS.SPCODE_HISTNO
        LEFT JOIN DWS.SA_BSCSIX_MPUSPTAB MM
        ON PP.SPCODE = MM.SPCODE
    INNER JOIN DMRED.BSCSIX_PR_SERV_STATUS_HIST SH
        ON PS.CO_ID = SH.CO_ID
        AND PS.SNCODE = SH.SNCODE
        AND PS.STATUS_HISTNO = SH.HISTNO
    INNER JOIN (SELECT CUSTOMER_ID,MAX(SEQNO) SEQNO , MAX(BILLCYCLE)KEEP(DENSE_RANK LAST ORDER BY  SEQNO) BILLCYCLE
    FROM DWS.SA_BILLCYCLE_ASSIGNMENT_HISTORY
    GROUP BY CUSTOMER_ID) BH
    ON BH.CUSTOMER_ID =DAT.CUSTOMER_ID
    WHERE PS.SRV_SUBTYPE = 'J'
        AND SH.STATUS = 'A'
        AND MM.PRODUCTOFFERING_TYPE IN ('O', 'A')
        AND DAT.CH_STATUS = 'a')
    SELECT 'ONE FIJA' FLUJO,
        PRGCODE,
        CUSTOMER_ID,
        CO_ID,
        CH_VALIDFROM,
        CH_STATUS,
        PLCODE,
        TMCODE,
        BILLCYCLE,
        DES,
        VELOCIDAD,
        STATUS,
        PO_ID,
        SNCODE,
        TECH
    FROM (SELECT A.*,
                B.*,
                ROW_NUMBER() OVER(PARTITION BY CUSTOMER_ID ORDER BY TO_NUMBER(VELOCIDAD) DESC) RN
            FROM BASSE A
            LEFT JOIN VELOCIDADES B
                ON A.EXTERNAL_SERVICE_PACKAGE_NAME = B.PO_ID
            WHERE B.VELOCIDAD IS NOT NULL)
    WHERE RN = 1
'''

INSERTAR_BASE_BSCS_IX = '''
INSERT INTO FIJA_BSCS_IX_VELOC (
    FLUJO       ,
    PRGCODE      ,
    CUSTOMER_ID  ,
    CO_ID        ,
    CH_VALIDFROM ,
    CH_STATUS    ,
    PLCODE       ,
    TMCODE       ,
    BILLCYCLE    ,
    DES          ,
    VELOCIDAD    ,
    STATUS       ,
    ETIQUETA     ,
    SNCODE       ,
    TECH         
)
VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15)
'''

BASE_DE_VELOCIDADES = '''
    SELECT A.SERVV_ID_BSCS     SNCODE_VEL,
            A.SERVV_DESCRIPCION,
            A.SERVV_CAPACIDAD,
            E.DESCRIPCION    ETIQUETA
        FROM DMRED.PVU_SISACT_AP_SERVICIO A
    INNER JOIN DWS.SA_SERVICIO_SISACT C
        ON C.idservicio_sisact = A.SERVV_CODIGO
    INNER JOIN DWS.SA_TYSTABSRV D
        ON D.CODSRV = C.CODSRV
    INNER JOIN DMRED.SGAPRD_CONFIGURACION_ITW E
        ON TO_CHAR(E.IDCONFIGITW) = D.CODIGO_EXT
'''

INSERTAR_BASE_DE_VELOCIDADES = '''
INSERT INTO base_velocidades (
sncode ,
descc ,
capacidad  ,
etiqueta )
VALUES (:1,:2,:3,:4)
'''

PROCESAR_PKG_INCOGNITO = '''
PK_ONE_FIJA.SP_CARGA_ICG
'''

PROCESAR_BASE = '''
PK_ONE_FIJA.FIJA_MDC001246   
'''

OBTENER_BASE ='''
SELECT  FLUJO,
        CUSTOMER_ID,
        CO_ID,
        NOMBRE_CLIENTE,
        DESCRIPCION,
        VELOCIDAD_BSCS,
        ETIQUETA_ICG,
        VELOCIDAD_ICG,
        ESCENARIO
        FROM FIJA_BASE_MDC001246 WHERE RESULT_TIME = TRUNC(SYSDATE,'DD')-- AND REINCIDENCIA IS NULL
'''