SELECT
    
    DISTINCT TABLE_NAME
FROM USER_TAB_COLUMNS
WHERE TABLE_NAME IN (
    'DMRED_CUSTOMER_ALL',
    'DMRED_CONTRACT_ALL',
    'DMRED_CONTRACT_HISTORY',
    'DWS_SA_CONTRACT_HISTORY'
)
ORDER BY TABLE_NAME;

SELECT *
FROM DMRED_CUSTOMER_ALL;

INSERT INTO DMRED_CUSTOMER_ALL (
    CUSTOMER_ID,
    NOMBRE_CLIENTE,
    PRGCODE
)
VALUES (
    1001,
    'Cliente Demo Alfa',
    '1'
);

INSERT INTO DMRED_CONTRACT_ALL (
    CO_ID,
    CUSTOMER_ID,
    PLCODE,
    SCCODE,
    NOMBRE_SERVICE
)
VALUES (
    2001,
    1001,
    1000,
    6,
    'Internet Fibra 300 Mbps'
);

INSERT INTO DMRED_CONTRACT_HISTORY (
    CO_ID,
    CH_SEQNO,
    CH_PENDING,
    CH_VALIDFROM,
    CH_STATUS
)
VALUES (
    2001,
    1,
    NULL,
    TRUNC(SYSDATE) - 30,
    's'
);



INSERT INTO DWS_SA_CONTRACT_HISTORY (
    CO_ID,
    CH_SEQNO
)
VALUES (
    2001,
    1
);

COMMIT;
SELECT 
*FROM tx_r2_log


INSERT ALL
    INTO tx_r2_log (
        id, fecha_procesar, status, tipo_ejecucion, codigo_control
    ) VALUES (
        1, TO_DATE('2026-10-15 09:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        0, 'AUTOMATICO', 'CTRL_R2'
    )

    INTO tx_r2_log (
        id, fecha_procesar, status, tipo_ejecucion, codigo_control
    ) VALUES (
        2, TO_DATE('2026-10-15 10:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        0, 'AUTOMATICO', 'CTRL_R2'
    )

    INTO tx_r2_log (
        id, fecha_procesar, status, tipo_ejecucion, codigo_control
    ) VALUES (
        3, TO_DATE('2026-10-15 11:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        0, 'AUTOMATICO', 'CTRL_R2'
    )

    INTO tx_r2_log (
        id, fecha_procesar, status, tipo_ejecucion, codigo_control
    ) VALUES (
        4, TO_DATE('2026-10-15 12:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        0, 'AUTOMATICO', 'CTRL_R2'
    )

    INTO tx_r2_log (
        id, fecha_procesar, status, tipo_ejecucion, codigo_control
    ) VALUES (
        5, TO_DATE('2026-10-15 13:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        0, 'AUTOMATICO', 'CTRL_R2'
    )

    INTO tx_r2_log (
        id, fecha_procesar, status, tipo_ejecucion, codigo_control
    ) VALUES (
        6, TO_DATE('2026-10-15 08:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        1, 'AUTOMATICO', 'CTRL_R2'
    )

    INTO tx_r2_log (
        id, fecha_procesar, status, tipo_ejecucion, codigo_control
    ) VALUES (
        7, TO_DATE('2026-10-14 22:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        2, 'AUTOMATICO', 'CTRL_R2'
    )

    INTO tx_r2_log (
        id, fecha_procesar, status, tipo_ejecucion, codigo_control
    ) VALUES (
        8, TO_DATE('2026-10-15 07:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        0, 'MANUAL', 'CTRL_R2'
    )

    INTO tx_r2_log (
        id, fecha_procesar, status, tipo_ejecucion, codigo_control
    ) VALUES (
        9, TO_DATE('2026-10-15 06:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        0, 'AUTOMATICO', 'CTRL_R3'
    )

    INTO tx_r2_log (
        id, fecha_procesar, status, tipo_ejecucion, codigo_control
    ) VALUES (
        10, TO_DATE('2026-10-15 14:05:00', 'YYYY-MM-DD HH24:MI:SS'),
        1, 'MANUAL', 'CTRL_R3'
    )
SELECT 1 FROM dual;

COMMIT;