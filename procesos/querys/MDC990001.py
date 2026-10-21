DELETE_BASE ='''

DELETE FROM FIJA_ACUERDOS_KPI WHERE RESULT_TIME =TRUNC(SYSDATE-1,'DD')
'''
PREV_INFORMACION='''INSERT INTO FIJA_ACUERDOS
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
                WHERE trunc(AC.CONTD_FECHA_CONTRATO, 'dd') > = trunc(sysdate -1,'dd')--TO_DATE(p_fecha_inicio,'dd/MM/yyyy HH24')
                AND trunc(AC.CONTD_FECHA_CONTRATO, 'dd') < trunc(sysdate ,'dd')
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
                WHERE trunc(FECUSU) >= trunc(sysdate -1,'dd') --temp.fecha'15/03/2025' -- TRUNC(SYSDATE) - 30
                AND trunc(FECUSU) < trunc(sysdate,'dd')),
            
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
                WHERE TRUNC(A.D_FECHA_REG) >= trunc(sysdate -1,'dd')
                AND TRUNC(A.D_FECHA_REG) < trunc(sysdate,'dd')) -- TRUNC(SYSDATE) - 30)
            
            SELECT /*+PARALLEL(20)*/
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
                        ON C.N_NROCONTRATO = A.CONTN_NUMERO_CONTRATO)
'''                      

OBTENER_BASE ='''
SELECT /*+PARALLEL(20)*/
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
            GROUP BY trunc(FEC_CONTRATO, 'dd'), OPERACION, APLICACION
'''

INSERTAR_BASE ='''
INSERT INTO FIJA_ACUERDOS_KPI
            (RESULT_TIME,
            OPERACION,
            PLATAFORMA,
            TOTAL,
            OBERVACION_HP,
            OBSERVACION_OSIPTEL,
            OBSERVACION_FIRMA)
    VALUES (:1,:2,:3,:4,:5,:6,:7)
'''