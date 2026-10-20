package PK_ONE_FIJA is
package body PK_ONE_FIJA is
  -- Author  : C27394
  PROCEDURE SP_CONFIG_CARGA IS
  -- Created : 17/01/2025 16:40:28
  BEGIN
    BEGIN
  -- Purpose : PK_ONE_FIJA
      INSERT INTO FIJA_SEGUIMIENTO
  ------------CARGAS--------------
        (NUM_PROCESO,
  PROCEDURE SP_CONFIG_CARGA;
  PROCEDURE SP_CARGA_ICG;
         FECHA_INSERCION,
  ----------ASIS--------------
         FECHA_PROCESAR,
  PROCEDURE FIJA_MDC001244;
         CONTROL,
  PROCEDURE FIJA_MDC001246;
         TIPO_CARGA,
  PROCEDURE FIJA_MDC008009;
         STATUS)
        SELECT NUM_PROCESO,
  PROCEDURE FIJA_MDC007760;
               FECHA_INSERCION,
  PROCEDURE FIJA_MDC001249;
               FECHA_PROCESAR,
  PROCEDURE FIJA_DDS000046 (p_rc OUT SYS_REFCURSOR);
  --------------ONE--------------
               CONTROL,
--PROCEDURE SP_FIJA_ACUERDOS_ALTAS(p_fecha_inicio VARCHAR2,
               TIPO_CARGA,
--                                p_fecha_fin    VARCHAR2);
               ESTATUS
--PROCEDURE SP_FIJA_PROVISION_ALTAS;
          FROM (SELECT (SELECT MAX(NUM_PROCESO) + 1 FROM FIJA_SEGUIMIENTO) +
                       (ROWNUM - 1) AS NUM_PROCESO,
                       TRUNC(SYSDATE, 'DD') FECHA_INSERCION,
end PK_ONE_FIJA;
                       TRUNC(SYSDATE, 'DD') FECHA_PROCESAR,
                       A.CONTROL,
                       'C' TIPO_CARGA,
                       0 ESTATUS
                  FROM FIJA_CONFIG_CARGA A
                 INNER JOIN (SELECT TO_NUMBER(TO_CHAR(SYSDATE, 'D')) DIA
                              FROM DUAL) B
                    ON A.DIA = B.DIA) A
         WHERE (A.CONTROL, FECHA_INSERCION) NOT IN
               (SELECT CONTROL, FECHA_INSERCION
                  FROM FIJA_SEGUIMIENTO
                 WHERE FECHA_INSERCION = TRUNC(SYSDATE, 'DD'));
      COMMIT;
    END;
  END SP_CONFIG_CARGA;
  PROCEDURE SP_CARGA_ICG IS
  BEGIN
    BEGIN
      EXECUTE IMMEDIATE 'TRUNCATE TABLE USRDDS.FIJA_SERVICIOS_ICG';
      --EXECUTE IMMEDIATE 'TRUNCATE TABLE USRDDS.BASE_VELOCIDADES';
      INSERT INTO FIJA_SERVICIOS_ICG
        (SERVICEID,
         SERVICEIDENTIFIER,
         ACCOUNTNUMBER,
         NOMBRE_CLIENTE,
         SERVICE_STATUS,
         NOMBRE_SERVICE,
         IDENTIFIER,
         LASTUPDATED,
         ENDDATE)
        SELECT S.SERVICEID,
               S.SERVICEIDENTIFIER,
               A.ACCOUNTNUMBER,
               SU.LASTNAME         NOMBRE_CLIENTE,
               RV.RANGETEXTVALUE   SERVICE_STATUS,
               ST.SERVICENAME      NOMBRE_SERVICE,
               EQ.IDENTIFIER,
               S.LASTUPDATED,
               S.ENDDATE
          FROM SAC.ACCOUNT@dbl_incdb_sby A
          LEFT JOIN SAC.SUBSCRIBER@dbl_incdb_sby SU
            ON SU.ACCOUNTID = A.ACCOUNTID
          LEFT JOIN SAC.SERVICE@dbl_incdb_sby S
            ON SU.SUBSCRIBERID = S.SUBSCRIBERID
          LEFT JOIN SAC.RANGE_VALUE@dbl_incdb_sby RV
            ON S.SERVICESTATUSID = RV.RANGEVALUEID
          LEFT JOIN SAC.SERVICE_TYPE@dbl_incdb_sby ST
            ON S.SERVICETYPEID = ST.SERVICETYPEID
          LEFT JOIN SAC.EQUIPMENT@dbl_incdb_sby EQ
            ON S.EQUIPMENTID = EQ.EQUIPMENTID
          LEFT JOIN SAC.RANGE_VALUE@dbl_incdb_sby RV2
            ON EQ.STATUSID = RV2.RANGEVALUEID
         WHERE RV.RANGENAME = 'SERVICE_STATUS_VALUES'
           AND RV.RANGETEXTVALUE = 'Active'
           AND RV2.RANGEVALUENAME NOT IN
               ('SUSPENDED', 'ACCOUNT_SUSPENDED', 'EQUIPMENT_SUSPENDED');
      COMMIT;
      MERGE INTO FIJA_SERVICIOS_ICG T
      USING (SELECT ETIQUETA,
                    MAX(TO_NUMBER(CASE
                                    WHEN CAPACIDAD LIKE ',%' THEN
                                     '0.' || SUBSTR(CAPACIDAD, 2, 6)
                                    ELSE
                                     CAPACIDAD
                                  END)) VELOCIDAD
               FROM BASE_VELOCIDADES
              WHERE CAPACIDAD IS NOT NULL
              GROUP BY ETIQUETA) K
      ON (T.NOMBRE_SERVICE = K.ETIQUETA)
      WHEN MATCHED THEN
        UPDATE SET T.VELOCIDAD = K.VELOCIDAD;
      COMMIT;
    END;
  END SP_CARGA_ICG;
  PROCEDURE FIJA_MDC001244 IS
  BEGIN
    BEGIN
      DELETE FROM FIJA_BASE_MDC001244
       WHERE RESULT_TIME = TRUNC(SYSDATE, 'DD');
      COMMIT;
      INSERT INTO FIJA_BASE_MDC001244
        (RESULT_TIME,
         CUSTOMER_ID,
         NOMBRE_CLIENTE,
         STATUS_BSCS,
         STATUS_ICG,
         NOMBRE_SERVICE)
        SELECT TRUNC(SYSDATE, 'DD') RESULT_TIME,
               A.CUSTOMER_ID,
               A.NOMBRE_CLIENTE,
               A.STATUS_BSCS,
               A.STATUS_ICG,
               A.NOMBRE_SERVICE
          FROM (SELECT ACCOUNTNUMBER CUSTOMER_ID,
                       NOMBRE_CLIENTE,
                       's' STATUS_BSCS,
                       SERVICE_STATUS STATUS_ICG,
                       NOMBRE_SERVICE
                  FROM FIJA_SERVICIOS_ICG
                 WHERE ACCOUNTNUMBER in
                       (SELECT to_char(customer_id) FROM FIJA_CUSTOMER)
                   AND (UPPER(NOMBRE_SERVICE) NOT LIKE '%TELEFONIA%' AND
                       NOMBRE_SERVICE NOT LIKE '%WIFI_PLUME%' AND
                       UPPER(NOMBRE_SERVICE) NOT LIKE '%FTTH_VIDEO%' AND
                       UPPER(NOMBRE_SERVICE) NOT LIKE '%HFC_IPTVVIDEO%')) A
          LEFT JOIN DMRED.SGAPRD_SOLOT@DBL_DWO B
            ON A.CUSTOMER_ID = to_char(B.CUSTOMER_ID)
           AND B.ESTSOL = 17
         WHERE B.CODSOLOT IS NULL;
      COMMIT;
      MERGE INTO FIJA_BASE_MDC001244 T
      USING (SELECT DISTINCT RESULT_TIME, CUSTOMER_ID
               FROM FIJA_BASE_MDC001244
              WHERE RESULT_TIME = (SELECT RESULT_TIME
                                     FROM (SELECT DISTINCT RESULT_TIME
                                             FROM FIJA_BASE_MDC001244
                                            WHERE RESULT_TIME > (SYSDATE - 10))
                                    ORDER BY RESULT_TIME DESC OFFSET 1 ROW
                                    FETCH NEXT 1 ROW ONLY)) K
      ON (T.CUSTOMER_ID = K.CUSTOMER_ID AND T.RESULT_TIME = TRUNC(SYSDATE, 'DD'))
      WHEN MATCHED THEN
        UPDATE SET T.REINCIDENCIA = 1;
      COMMIT;
    END;
  END FIJA_MDC001244;
  PROCEDURE FIJA_MDC001246 IS
  BEGIN
    BEGIN
      DELETE FROM FIJA_BASE_MDC001246
       WHERE RESULT_TIME = TRUNC(SYSDATE, 'DD');
      COMMIT;
      INSERT INTO FIJA_BASE_MDC001246
        (RESULT_TIME,
         FLUJO,
         CUSTOMER_ID,
         CO_ID,
         NOMBRE_CLIENTE,
         DESCRIPCION,
         VELOCIDAD_BSCS,
         ETIQUETA_ICG,
         VELOCIDAD_ICG,
         ESCENARIO)
    /* Se actualiza codigo porque mostraba varios registros fp@29/12/2025 */
    SELECT RESULT_TIME, FLUJO, CUSTOMER_ID, CO_ID, NOMBRE_CLIENTE, DESCRIPCION, VELOCIDAD_BSCS, ETIQUETA_ICG, VELOCIDAD_ICG, ESCENARIO
    FROM (
      SELECT TRUNC(SYSDATE, 'dd') RESULT_TIME,
           A.FLUJO,
           A.CUSTOMER_ID,
           A.CO_ID,
           A.NOMBRE_CLIENTE,
           A.DESCRIPCION,
           A.VELOCIDAD_BSCS,
           A.ETIQUETA_ICG,
           A.VELOCIDAD_ICG,
           A.ESCENARIO,
           ROW_NUMBER() OVER (PARTITION BY A.CUSTOMER_ID ORDER BY A.FLUJO) AS RN
      FROM (
        SELECT BS.FLUJO,
               BS.PLCODE,
               BS.CUSTOMER_ID,
               BS.CO_ID,
               ICG.NOMBRE_CLIENTE,
               BS.DES DESCRIPCION,
               BS.VELOCIDAD VELOCIDAD_BSCS,
               ICG.NOMBRE_SERVICE ETIQUETA_ICG,
               ICG.VELOCIDAD VELOCIDAD_ICG,
               CASE
                 WHEN BS.VELOCIDAD > ICG.VELOCIDAD THEN 'MENOR VELOCIDAD DE LO CONTRATADO'
                 WHEN BS.VELOCIDAD < ICG.VELOCIDAD THEN 'MAYOR VELOCIDAD DE LO CONTRATADO'
                 WHEN BS.VELOCIDAD = ICG.VELOCIDAD THEN 'OK'
                 ELSE 'OTRA OBSERVACION'
               END ESCENARIO
          FROM USRDDS.FIJA_BSCS_IX_VELOC BS
          LEFT JOIN USRDDS.FIJA_SERVICIOS_ICG ICG ON ICG.ACCOUNTNUMBER = TO_CHAR(BS.CUSTOMER_ID)
                                                 AND ICG.VELOCIDAD IS NOT NULL
         WHERE NOT ((LENGTH(BILLCYCLE) > 1 AND BILLCYCLE LIKE '9%') OR (BILLCYCLE = 13))
           AND ICG.ACCOUNTNUMBER IS NOT NULL
      ) A
      WHERE A.ESCENARIO <> 'OK'
    )
    WHERE RN = 1;
      COMMIT;
      MERGE INTO FIJA_BASE_MDC001246 T
      USING (SELECT DISTINCT RESULT_TIME, CUSTOMER_ID, CO_ID
               FROM FIJA_BASE_MDC001246
              WHERE RESULT_TIME = (SELECT RESULT_TIME
                                     FROM (SELECT DISTINCT RESULT_TIME
                                             FROM FIJA_BASE_MDC001246
                                            WHERE RESULT_TIME > (SYSDATE - 10))
                                    ORDER BY RESULT_TIME DESC OFFSET 1 ROW
                                    FETCH NEXT 1 ROW ONLY)) K
      ON (T.CUSTOMER_ID = K.CUSTOMER_ID AND T.CO_ID = K.CO_ID AND T.RESULT_TIME = TRUNC(SYSDATE, 'DD'))
      WHEN MATCHED THEN
        UPDATE SET T.REINCIDENCIA = 1;
      COMMIT;
    END;
  END FIJA_MDC001246;
  /* PROCEDURE FIJA_MDC001249 IS
  BEGIN
    BEGIN
      DELETE FROM FIJA_BASE_MDC001249
       WHERE RESULT_TIME = TRUNC(SYSDATE, 'DD');
      COMMIT;
      INSERT INTO FIJA_BASE_MDC001249
        (RESULT_TIME,
         CUSTOMER_ID,
         CO_ID,
         NOMBRE_CLIENTE,
         DESCRIPCION,
         VELOCIDAD_BSCS,
         ETIQUETA_ICG,
         VELOCIDAD_ICG,
         ESCENARIO)
        SELECT DISTINCT TRUNC(SYSDATE, 'dd') RESULT_TIME,
                        A.CUSTOMER_ID,
                        A.CO_ID,
                        A.NOMBRE_CLIENTE,
                        A.DESCRIPCION,
                        A.VELOCIDAD_BSCS,
                        A.ETIQUETA_ICG,
                        A.VELOCIDAD_ICG,
                        A.ESCENARIO
          FROM (SELECT BS.CUSTOMER_ID,
                       BS.CO_ID,
                       ICG.NOMBRE_CLIENTE,
                       BS.DES DESCRIPCION,
                       BS.VELOCIDAD VELOCIDAD_BSCS,
                       ICG.NOMBRE_SERVICE ETIQUETA_ICG,
                       ICG.VELOCIDAD VELOCIDAD_ICG,
                       CASE
                         WHEN ICG.ACCOUNTNUMBER IS NULL THEN
                          'CLIENTE NO APROVISIONADO'
                         ELSE
                          'OK'
                       END ESCENARIO
                  FROM FIJA_BASE_VELOCIDADES_BSCS BS
                  LEFT JOIN FIJA_SERVICIOS_ICG ICG
                    ON ICG.ACCOUNTNUMBER = TO_CHAR(BS.CUSTOMER_ID)
                   AND ICG.VELOCIDAD IS NOT NULL
                 WHERE NOT ((LENGTH(BILLCYCLE) > 1 AND BILLCYCLE LIKE '9%') OR
                        (BILLCYCLE = 13))
                   AND ICG.ACCOUNTNUMBER IS NULL) A
          LEFT JOIN DMRED.SGAPRD_SOLOT@DBL_DWO B
            ON A.CUSTOMER_ID = B.CUSTOMER_ID
           AND B.ESTSOL = 17
         WHERE A.ESCENARIO <> 'OK'
           AND B.CODSOLOT IS NULL;
      COMMIT;
      MERGE INTO FIJA_BASE_MDC001249 T
      USING (SELECT *
               FROM FIJA_BASE_MDC001249
              WHERE RESULT_TIME = (SELECT RESULT_TIME
                                     FROM (SELECT DISTINCT RESULT_TIME
                                             FROM FIJA_BASE_MDC001249
                                            WHERE RESULT_TIME > (SYSDATE - 10))
                                    ORDER BY RESULT_TIME DESC OFFSET 1 ROW
                                    FETCH NEXT 1 ROW ONLY)) K
      ON (T.CUSTOMER_ID = K.CUSTOMER_ID AND T.CO_ID = K.CO_ID AND T.RESULT_TIME = TRUNC(SYSDATE, 'DD'))
      WHEN MATCHED THEN
        UPDATE SET T.REINCIDENCIA = 1;
      COMMIT;
    END;
  END FIJA_MDC001249;*/
  PROCEDURE FIJA_MDC008009 IS
  BEGIN
    BEGIN
      DELETE FROM FIJA_BASE_MDC008009
       WHERE RESULT_TIME = TRUNC(SYSDATE, 'DD');
      COMMIT;
      INSERT INTO FIJA_BASE_MDC008009
        (RESULT_TIME,
         CODSOLOT,
         CUSTOMER_ID,
         CO_ID,
         CH_STATUS,
         DESCRIPCION,
         TIPO_SERVICIO,
         NOMBRE_CLIENTE,
         LASTUPDATED)
        SELECT TRUNC(SYSDATE, 'DD') RESULT_TIME,
               CODSOLOT,
               CUSTOMER_ID,
               CO_ID,
               CH_STATUS,
               DESCRIPCION,
               TIPO_SERVICIO,
               NOMBRE_CLIENTE,
               LASTUPDATED
          FROM (select a.CODSOLOT,
                       a.customer_id,
                       a.co_id,
                       A.CH_STATUS,
                       a.descripcion,
                       a.tipo_servicio,
                       b.NOMBRE_CLIENTE,
                       to_char(b.LASTUPDATED) LASTUPDATED
                  from fija_altas_sga a
                  left join fija_servicios_icg b
                    on to_char(a.customer_id) = b.accountnumber
                   and b.nombre_service like 'In%'
                 where tipo_servicio = 'Acceso Dedicado a Internet'
                   and b.NOMBRE_CLIENTE is null
                /*telefonia*/
                union all
                select a.CODSOLOT,
                       a.customer_id,
                       a.co_id,
                       A.CH_STATUS,
                       a.descripcion,
                       a.tipo_servicio,
                       b.NOMBRE_CLIENTE,
                       to_char(b.LASTUPDATED)
                  from fija_altas_sga a
                  left join fija_servicios_icg b
                    on to_char(a.customer_id) = b.accountnumber
                   and b.nombre_service like '%Telefonia_Servicio_Prepaid'
                 where tipo_servicio = 'Telefonia Fija'
                   and b.NOMBRE_CLIENTE is null
                union all
                /*cable*/
                SELECT A.CODSOLOT,
                       a.customer_id,
                       a.co_id,
                       A.CH_STATUS,
                       a.descripcion,
                       a.tipo_servicio,
                       cast(decode(B.SUSV_CUSTOMERID,
                                   null,
                                   c.nombre_cliente,
                                   B.SUSV_CUSTOMERID) as nvarchar2(40)) NOMBRE_CLIENTE,
                       to_char(B.SUSN_SERVICIOID)
                  FROM fija_altas_sga A
                  LEFT JOIN DMRED.IOTT_SUSCRIPCION@DBL_DWO B
                    ON TO_CHAR(A.CUSTOMER_ID) =
                       SUBSTR(REGEXP_SUBSTR(B.SUSV_LINEA, '\d+'),
                              1,
                              LENGTH(REGEXP_SUBSTR(B.SUSV_LINEA, '\d+')) - 1)
                   AND A.CODIGO_EXT = B.SUSN_SERVICIOID
                   and b.SUSC_ESTADO = 'A'
                  LEFT JOIN fija_servicios_icg C
                    on to_char(a.customer_id) = C.accountnumber
                   and C.nombre_service like 'Migra2'
                   AND A.CODIGO_EXT = 15
                 where trim(a.tipo_servicio) = 'Cable'
                   and (b.SUSV_LINEA is null and c.nombre_cliente is null));
      COMMIT;
    END;
  END FIJA_MDC008009;
  /*
  PROCEDURE SP_FIJA_PROVISION_ALTAS IS
  BEGIN
    BEGIN
      SP_CARGA_ICG;
      --EXECUTE IMMEDIATE 'TRUNCATE TABLE USRDDS.FIJA_ALTA_PROVICION';
      /*
      ----------------------------INCOGNITO-------------------------
                                                                  /
      INSERT INTO FIJA_ALTA_PROVICION
        (SERVICEIDENTIFIER,
         PLATAFORMA,
         CUSTOMER_ID,
         NOMBRE_CLIENTE,
         NOMBRE_SERVICE,
         VELOCIDAD,
         LASTUPDATED,
         POID,
         NUM)
        SELECT SERVICEIDENTIFIER,
               'INCOGNITO' PLATAFORMA,
               TO_NUMBER(ACCOUNTNUMBER) CUSTOMER_ID,
               NOMBRE_CLIENTE,
               NOMBRE_SERVICE,
               VELOCIDAD,
               LASTUPDATED,
               POID,
               NUM
          FROM FIJA_SERVICIOS_ICG
         WHERE ACCOUNTNUMBER IN (SELECT DISTINCT TO_CHAR(CUSTOMER_ID) CUSTOMER_ID
                                   FROM FIJA_ALTAS_SGA);
      COMMIT;
      -------ORDENAR SERVICIOS--------
      MERGE INTO FIJA_ALTA_PROVICION T
      USING (SELECT SERVICEIDENTIFIER,
                    CUSTOMER_ID,
                    NOMBRE_SERVICE,
                    RANK() OVER(PARTITION BY CUSTOMER_ID, NOMBRE_SERVICE ORDER BY LASTUPDATED ASC) R
               FROM FIJA_ALTA_PROVICION) K
      ON (T.SERVICEIDENTIFIER = K.SERVICEIDENTIFIER)
      WHEN MATCHED THEN
        UPDATE SET T.NUM = K.R;
      COMMIT;
      -------SERVICIOS TV SUPERIOR--------
      MERGE INTO FIJA_ALTA_PROVICION T
      USING (SELECT A.CUSTOMER_ID,
                    C.CBV_POIDADICIONAL,
                    RANK() OVER(PARTITION BY A.CUSTOMER_ID ORDER BY C.CBV_POIDADICIONAL ASC) AS ranking
               FROM FIJA_ALTAS_SGA A
               LEFT JOIN CB_SERVICIOS C
                 ON C.CBV_ID_SERV = A.IDSERVICIO_SISACT
              WHERE SUBSTR(C.CBI_CO_GRP_SERV, -2) = 28) K
      ON (T.NUM = K.ranking AND T.CUSTOMER_ID = K.CUSTOMER_ID AND T.NOMBRE_SERVICE = 'Migra2')
      WHEN MATCHED THEN
        UPDATE SET T.POID = K.CBV_POIDADICIONAL;
      COMMIT;
      -------SERVICIOS INTERNET--------
      MERGE INTO FIJA_ALTA_PROVICION T
      USING (SELECT A.CUSTOMER_ID,
                    C.CBV_POIDADICIONAL,
                    RANK() OVER(PARTITION BY A.CUSTOMER_ID ORDER BY C.CBV_POIDADICIONAL ASC) AS ranking
               FROM FIJA_ALTAS_SGA A
               LEFT JOIN CB_SERVICIOS C
                 ON C.CBV_ID_SERV = A.IDSERVICIO_SISACT
              WHERE C.CBI_CO_GRP_SERV in (26, 32)) K
      ON (T.NUM = K.ranking AND T.CUSTOMER_ID = K.CUSTOMER_ID AND T.VELOCIDAD IS NOT NULL)
      WHEN MATCHED THEN
        UPDATE SET T.POID = K.CBV_POIDADICIONAL;
      COMMIT;
      -------SERVICIOS PLUME--------
      MERGE INTO FIJA_ALTA_PROVICION T
      USING (SELECT A.CUSTOMER_ID,
                    C.CBV_POIDADICIONAL,
                    RANK() OVER(PARTITION BY A.CUSTOMER_ID ORDER BY C.CBV_POIDADICIONAL ASC) AS ranking
               FROM FIJA_ALTAS_SGA A
               LEFT JOIN CB_SERVICIOS C
                 ON C.CBV_ID_SERV = A.IDSERVICIO_SISACT
              WHERE C.CBI_CO_GRP_SERV = 127) K
      ON (T.NUM = K.ranking AND T.CUSTOMER_ID = K.CUSTOMER_ID AND T.NOMBRE_SERVICE LIKE 'WIFI_PLUM%')
      WHEN MATCHED THEN
        UPDATE SET T.POID = K.CBV_POIDADICIONAL;
      COMMIT;
      -------SERVICIOS TELEFONIA--------
      MERGE INTO FIJA_ALTA_PROVICION T
      USING (SELECT A.CUSTOMER_ID,
                    C.CBV_POIDADICIONAL,
                    C.CBV_DESCRIPCION,
                    RANK() OVER(PARTITION BY A.CUSTOMER_ID ORDER BY C.CBV_POIDADICIONAL ASC) AS ranking
               FROM FIJA_ALTAS_SGA A
               LEFT JOIN CB_SERVICIOS C
                 ON C.CBV_ID_SERV = A.IDSERVICIO_SISACT
              WHERE C.CBI_CO_GRP_SERV = 30) K
      ON (T.NUM = K.ranking AND T.CUSTOMER_ID = K.CUSTOMER_ID AND T.NOMBRE_SERVICE = K.CBV_DESCRIPCION)
      WHEN MATCHED THEN
        UPDATE SET T.POID = K.CBV_POIDADICIONAL;
      COMMIT;
      UPDATE FIJA_ALTA_PROVICION
         SET POID = 'telefonia1000_Hfc1Optb'
       WHERE NOMBRE_SERVICE = 'Telefonia_Servicio_Prepaid';
      UPDATE FIJA_ALTA_PROVICION
         SET POID = 'telefonia1000_Ftth1Optb'
       WHERE NOMBRE_SERVICE = 'FTTH_Telefonia_Servicio_Prepaid';
      COMMIT;
      -------SERVICIOS CABLE--------
      MERGE INTO FIJA_ALTA_PROVICION T
      USING (SELECT A.CUSTOMER_ID,
                    C.CBV_POIDADICIONAL,
                    C.CBV_DESCRIPCION,
                    RANK() OVER(PARTITION BY A.CUSTOMER_ID ORDER BY C.CBV_POIDADICIONAL ASC) AS ranking
               FROM FIJA_ALTAS_SGA A
               LEFT JOIN CB_SERVICIOS C
                 ON C.CBV_ID_SERV = A.IDSERVICIO_SISACT
              WHERE C.CBI_CO_GRP_SERV = 136) K
      ON (T.NUM = K.ranking AND T.CUSTOMER_ID = K.CUSTOMER_ID AND T.SERVICEIDENTIFIER = '99000001')
      --T.NOMBRE_SERVICE = K.CBV_DESCRIPCION)
      WHEN MATCHED THEN
        UPDATE SET T.POID = K.CBV_POIDADICIONAL;
      COMMIT;
    END;
  END SP_FIJA_PROVISION_ALTAS;*/
  /* PROCEDURE SP_FIJA_ACUERDOS_ALTAS(p_fecha_inicio VARCHAR2,
                                   p_fecha_fin    VARCHAR2) IS
  BEGIN
    Declare
      --err_msg           VARCHAR2(100);
      cursor c_dif is
        select distinct trunc(fecha, 'dd') fecha
          from (SELECT TRUNC(SYSDATE + 1 - LEVEL, 'DD') FECHA
                  FROM DUAL
                CONNECT BY LEVEL < 99999)
         WHERE FECHA >= TO_DATE(p_fecha_inicio, 'dd/MM/yyyy')
           AND FECHA < TO_DATE(p_fecha_fin, 'dd/MM/yyyy')
         ORDER BY trunc(fecha, 'dd');
    begin
      for temp in c_dif loop
        delete from FIJA_ACUERDOS_KPI
         WHERE result_time >= temp.fecha
           AND result_time < temp.fecha + 1;
        commit;
        EXECUTE IMMEDIATE 'TRUNCATE TABLE USRDDS.FIJA_ACUERDOS';
        INSERT INTO FIJA_ACUERDOS
          (RESULT_TIME,
           OPERACION,
           APLICACION,
           FLUJO_VENTA,
           NUMERO_CONTRATO,
           DESC_OFICINA_VENTA,
           NUMERO_PCS,
           FEC_CONTRATO,
           NUM_SEC,
           RESULTADO,
           TIPO_DOC,
           NRO_DOC,
           ID_DETALLE_HP,
           ID_REGISTRO_OSIPTE,
           FIRMA_DIGITAL,
           OBERVACION_HP,
           OBSERVACION_OSIPTEL)
          WITH BASE_CONTRATO AS
           (SELECT DECODE(SS.CAMPN_CODIGO,
                          '100',
                          'FIJA_ONE',
                          '99',
                          'FIJA_ASIS',
                          '98',
                          'FIJA_ASIS',
                          '') FLUJO_VENTA,
                   DECODE(AC.CONTV_MOTIVO_MIG,
                          NULL,
                          'ALTA REGULAR',
                          104,
                          'PORT IN',
                          21,
                          'MIGRACION PRE A POST',
                          'VENTA NORMAL / ALTA') OPERACION,
                   AC.*,
                   OV.TOFIC_CODIGO
              FROM USRPVU.SISACT_AP_CONTRATO@DBL_PVUDB_SBY AC
             INNER JOIN USRPVU.sect_solicitud@DBL_PVUDB_SBY SS
                ON SS.SOLIN_CODIGO = AC.CONTN_NUMERO_SEC
             INNER JOIN USRPVU.SECT_OFICINA_VENTA@DBL_PVUDB_SBY OV
                ON AC.CONTC_OFICINA_VENTA = OV.OVENC_CODIGO
             WHERE trunc(AC.CONTD_FECHA_CONTRATO, 'dd') > = temp.fecha --TO_DATE(p_fecha_inicio,'dd/MM/yyyy HH24')
               AND trunc(AC.CONTD_FECHA_CONTRATO, 'dd') < temp.fecha + 1
               AND CONTC_TIPO_PRODUCTO NOT IN ('01', '06')
                  --AND CONTC_TIPO_OPERACION NOT IN (01, 04)
               AND CONTC_ESTADO = 8 --IN (8, 6)
               and SS.CAMPN_CODIGO in ('100', '99', '98')),
          BASE_HP AS
           (
            SELECT A.*
              FROM USRPVU.SISACT_ACUERDOS_HP@DBL_PVUDB_SBY A
             INNER JOIN BASE_CONTRATO B
                ON B.CONTN_NUMERO_CONTRATO = A.NRO_CONTRATO
             WHERE trunc(FECUSU) >= temp.fecha --temp.fecha'15/03/2025' -- TRUNC(SYSDATE) - 30
               AND trunc(FECUSU) < temp.fecha + 1),
          BASE_OSIPTEL AS
           (SELECT A.N_IDREGISTRO,
                   A.V_GDOCCODIGO,
                   A.N_NROPEDIDO,
                   A.N_NROCONTRATO,
                   A.N_NROSOT,
                   A.N_NROSEC,
                   A.V_NROLINEA,
                   A.V_FLAGFIRMA,
                   A.V_NRODOCUMENTO,
                   A.V_FLAGENVIOCORREO,
                   A.V_FIRMA_DIGITAL,
                   A.V_TIPOOPERACION,
                   A.V_ESTADO,
                   A.V_ACUERDOSGENBRMS AS NRO_DOCU_OSIPTEL,
                   A.V_USUARIO_REG,
                   A.V_USUARIO_MODIF,
                   A.D_FECHA_REG,
                   A.D_FECHA_MODIF,
                   A.V_IDTRANSACCION,
                   A.V_IDCONTRATOEXPEDIENTE
              FROM USRACT.EAIT_CONTRATOS_OSIPTEL@DBL_TIMEAISBY A
             INNER JOIN BASE_CONTRATO B
                ON A.N_NROCONTRATO = B.CONTN_NUMERO_CONTRATO
             WHERE TRUNC(A.D_FECHA_REG) >= temp.fecha
               AND TRUNC(A.D_FECHA_REG) < temp.fecha + 1) -- TRUNC(SYSDATE) - 30)
          SELECT /*+PARALLEL(20)/
           *
            FROM (SELECT TRUNC(SYSDATE, 'DD') RESULT_TIME,
                         a.OPERACION,
                         DECODE(A.CONTV_USUARIO_CREACION,
                                'USRBIOMOVI',
                                'APK',
                                'SISACT') APLICACION,
                         A.FLUJO_VENTA,
                         A.CONTN_NUMERO_CONTRATO NUMERO_CONTRATO,
                         A.CONTV_OFICINA_VENTA_DESC DESC_OFICINA_VENTA,
                         A.CONTV_NUMERO_PCS NUMERO_PCS,
                         A.CONTD_FECHA_CONTRATO FEC_CONTRATO,
                         A.CONTN_NUMERO_SEC NUM_SEC,
                         A.CONTV_RESULTADO RESULTADO,
                         A.CONTC_TIPO_DOC_CLIENTE TIPO_DOC,
                         A.CONTV_NRO_DOC_CLIENTE NRO_DOC,
                         B.ID_DETALLE_HP,
                         C.N_IDREGISTRO ID_REGISTRO_OSIPTE,
                         C.V_FIRMA_DIGITAL FIRMA_DIGITAL,
                         DECODE(B.ID_DETALLE_HP,
                                NULL,
                                'NO REGISTRADO EN HP',
                                NULL) OBERVACION_HP,
                         DECODE(C.N_IDREGISTRO,
                                NULL,
                                'NO REGISTRADO EN LA BASE DE OSIPTEL',
                                NULL) OBSERVACION_OSIPTEL
                    FROM BASE_CONTRATO A
                    LEFT JOIN BASE_HP B
                      ON A.CONTN_NUMERO_CONTRATO = B.NRO_CONTRATO
                    LEFT JOIN BASE_OSIPTEL C
                      ON C.N_NROCONTRATO = A.CONTN_NUMERO_CONTRATO);
        COMMIT;
        INSERT INTO FIJA_ACUERDOS_KPI
          (RESULT_TIME,
           OPERACION,
           PLATAFORMA,
           TOTAL,
           OBERVACION_HP,
           OBSERVACION_OSIPTEL,
           OBSERVACION_FIRMA)
          SELECT /*+PARALLEL(20)/
           trunc(FEC_CONTRATO, 'dd') FEC_CONTRATO,
           OPERACION,
           APLICACION,
           count(1) total,
           sum(case
                 when OBERVACION_HP is null then
                  0
                 else
                  1
               end) OBERVACION_HP,
           sum(case
                 when OBSERVACION_OSIPTEL is null then
                  0
                 else
                  1
               end) OBSERVACION_OSIPTEL,
           sum(case
                 when ESCENARIO is null then
                  0
                 else
                  1
               end) OBSERVACION_FIRMA
            FROM (SELECT AP.*,
                         BB.BIOM_CODBIO,
                         CASE
                           WHEN BB.BIOM_CODBIO = 70006 AND
                                AP.FIRMA_DIGITAL IS NOT NULL THEN
                            'OK'
                           WHEN BB.BIOM_CODBIO <> 70006 AND
                                AP.FIRMA_DIGITAL IS NULL THEN
                            'OK'
                           WHEN BB.BIOM_CODBIO = 70006 AND
                                AP.FIRMA_DIGITAL IS NULL THEN
                            'REQUIERE FIRMA DIGITAL'
                           WHEN BB.BIOM_CODBIO <> 70006 AND
                                AP.FIRMA_DIGITAL IS NULL THEN
                            'NO REQUIERE FIRMA DIGITAL'
                         END ESCENARIO
                    FROM FIJA_ACUERDOS AP
                    LEFT JOIN USRPVU.BIOMT_GENDOC@DBL_PVUDB_SBY BG
                      ON AP.NUM_SEC = BG.GDOC_NROSEC
                    LEFT JOIN USRPVU.BIOMT_GENDOC_28574@DBL_PVUDB_SBY BGA
                      ON AP.NUM_SEC = BGA.GDOC_NROSEC
                    LEFT JOIN USRPVU.BIOMT_BIOMETRIA@DBL_PVUDB_SBY BB
                      ON (BG.GDOC_IDPADRE = BB.BIOM_IDPADRE OR
                         BGA.GDOC_IDPADRE = BB.BIOM_IDPADRE))
           GROUP BY trunc(FEC_CONTRATO, 'dd'), OPERACION, APLICACION;
        COMMIT;
      END LOOP;
    END;
  END SP_FIJA_ACUERDOS_ALTAS;*/
  PROCEDURE FIJA_MDC007760 IS
  BEGIN
    BEGIN
      DELETE FROM FIJA_BASE_MDC007760
       WHERE RESULT_TIME = TRUNC(SYSDATE, 'DD');
      COMMIT;
      INSERT INTO FIJA_BASE_MDC007760
        (RESULT_TIME,
         ACCOUNTNUMBER,
         NOMBRE_CLIENTE,
         SERVICE_STATUS,
         NOMBRE_SERVICE,
         ESTADO_CONTRATO)
        SELECT TRUNC(SYSDATE, 'DD') RESULT_TIME,
               ACCOUNTNUMBER,
               NOMBRE_CLIENTE,
               SERVICE_STATUS,
               NOMBRE_SERVICE,
               'd' ESTADO_CONTRATO
          FROM FIJA_SERVICIOS_ICG C
         INNER JOIN (select to_char(customer_id) customer_id
                       from bscs70_datos_cliente
                      where PLCODE = 1000
                      group by customer_id
                     having sum(case
                       when ch_status in ('a', 's', 'o') then
                        1
                       else
                        0
                     end) = 0) F
            ON C.ACCOUNTNUMBER = F.CUSTOMER_ID
         WHERE c.ACCOUNTNUMBER NOT IN
               (SELECT DISTINCT TO_CHAR(CU.CUSTOMER_ID)
                  FROM GGSTG.BSCSIX_CONTRACT_ALL CA
                 INNER JOIN GGSTG.BSCSIX_CUSTOMER_ALL CU
                    ON CA.CUSTOMER_ID = CU.CUSTOMER_ID
                 WHERE CA.PLCODE = 1007
                   AND CA.SCCODE = 6
                   AND CA.TMCODE = 45
                   AND CU.PRGCODE IN ('2', '5')
                   AND CA.CH_STATUS = 'a');
      COMMIT;
    END;
  END FIJA_MDC007760;
  PROCEDURE FIJA_MDC001249 IS
  BEGIN
    BEGIN
      DELETE FROM FIJA_BASE_MDC001249
       WHERE RESULT_TIME = TRUNC(SYSDATE, 'DD');
      COMMIT;
      INSERT INTO FIJA_BASE_MDC001249
        (RESULT_TIME,
         CODSOLOT,
         CUSTOMER_ID,
         NOMBRE_CLIENTE,
         COD_ID,
         ESTADO_CONTRATO,
         TIPTRA,
         DESCRIPCION,
         SERVICE_STATUS,
         NOMBRE_SERVICE)
        select TRUNC(SYSDATE, 'DD') RESULT_TIME,
               a.CODSOLOT,
               a.CUSTOMER_ID,
               b.NOMBRE_CLIENTE,
               a.COD_ID,
               a.ESTADO_CONTRATO,
               a.TIPTRA,
               a.DESCRIPCION,
               b.SERVICE_STATUS,
               b.NOMBRE_SERVICE
          from FIJA_CORTE_SERVICIO_SGA a
         inner join FIJA_SERVICIOS_ICG b
            on to_char(a.customer_id) = b.accountnumber;
      COMMIT;
    END;
  END FIJA_MDC001249;
  PROCEDURE FIJA_DDS000046 (p_rc OUT SYS_REFCURSOR) IS
  BEGIN
    BEGIN
      DELETE FROM FIJA_BASE_DDS000046
       WHERE RESULT_TIME = TRUNC(SYSDATE, 'DD');
      COMMIT;
      INSERT INTO FIJA_BASE_DDS000046
  (RESULT_TIME,
   ACCOUNTNUMBER,
   NOMBRE_CLIENTE,
   SERVICE_STATUS,
   NOMBRE_SERVICE,
   IDENTIFIER,
   ESCENARIO)
   SELECT RESULT_TIME,
         ACCOUNTNUMBER,
         NOMBRE_CLIENTE,
         SERVICE_STATUS,
         NOMBRE_SERVICE,
         IDENTIFIER,
         ESCENARIO FROM
  (SELECT TRUNC(SYSDATE, 'DD') RESULT_TIME,
         ACCOUNTNUMBER,
         NOMBRE_CLIENTE,
         SERVICE_STATUS,
         NOMBRE_SERVICE,
         IDENTIFIER,
         ESCENARIO
    FROM (SELECT /*+PARALLEL(8) */
           ACCOUNTNUMBER,
           NOMBRE_CLIENTE,
           SERVICE_STATUS,
           NOMBRE_SERVICE,
           IDENTIFIER,
           'CLIENTE PROVISIONADOS SIN CONTRATO ACTIVO' ESCENARIO
            FROM (SELECT A.ACCOUNTNUMBER,
                         A.NOMBRE_CLIENTE,
                         A.SERVICE_STATUS,
                         A.NOMBRE_SERVICE,
                         A.IDENTIFIER
                    FROM FIJA_SERVICIOS_ICG A
                    LEFT JOIN BSCS70_DATOS_CLIENTE B
                      ON TO_CHAR(B.CUSTOMER_ID) = A.ACCOUNTNUMBER
                     AND B.CH_STATUS IN ('a', 's')
                     AND B.PLCODE = 1000
                   WHERE A.ACCOUNTNUMBER NOT IN ('101','113','114','incogtest')
                     AND UPPER(A.ACCOUNTNUMBER) NOT LIKE '%AMERICA%MOVIL%'
                     AND A.VELOCIDAD IS NOT NULL
                     AND TRUNC(LASTUPDATED) < TRUNC(SYSDATE)
                     AND B.CUSTOMER_ID IS NULL) A
           WHERE A.ACCOUNTNUMBER NOT LIKE '0%') A
   WHERE A.ACCOUNTNUMBER NOT IN
         (SELECT DISTINCT TO_CHAR(CU.CUSTOMER_ID)
            FROM GGSTG.BSCSIX_CONTRACT_ALL CA
           INNER JOIN GGSTG.BSCSIX_CUSTOMER_ALL CU
              ON CA.CUSTOMER_ID = CU.CUSTOMER_ID
           WHERE CA.PLCODE = 1007
             AND CA.SCCODE = 6
             AND CA.TMCODE = 45
             AND CU.PRGCODE IN ('2', '5')
             AND CA.CH_STATUS = 'a'))
             WHERE ACCOUNTNUMBER NOT IN (SELECT TO_CHAR(CUSTOMER_ID) FROM DMRED.SGAPRD_SOLOT@DBL_DWO WHERE ESTSOL = 17);
     COMMIT;
    MERGE INTO FIJA_BASE_DDS000046 T
      USING (SELECT DISTINCT RESULT_TIME, ACCOUNTNUMBER
               FROM FIJA_BASE_DDS000046
              WHERE RESULT_TIME = (SELECT RESULT_TIME
                                     FROM (SELECT DISTINCT RESULT_TIME
                                             FROM FIJA_BASE_DDS000046
                                            WHERE RESULT_TIME > (SYSDATE - 10))
                                    ORDER BY RESULT_TIME DESC OFFSET 1 ROW
                                    FETCH NEXT 1 ROW ONLY)) K
      ON (T.ACCOUNTNUMBER = K.ACCOUNTNUMBER AND T.RESULT_TIME = TRUNC(SYSDATE, 'DD'))
      WHEN MATCHED THEN
        UPDATE SET T.REINCIDENCIA = 1;
      COMMIT;
      open p_rc for
           SELECT RESULT_TIME,
         ACCOUNTNUMBER,
         NOMBRE_CLIENTE,
         SERVICE_STATUS,
         NOMBRE_SERVICE,
         IDENTIFIER,
         ESCENARIO
         FROM FIJA_BASE_DDS000046
         WHERE RESULT_TIME = TRUNC(SYSDATE,'DD')
         AND REINCIDENCIA IS NULL;
    END;
  END FIJA_DDS000046;
end PK_ONE_FIJA;
