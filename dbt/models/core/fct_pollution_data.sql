{{ config(
    materialized = 'table',
    partition_by = {
        'field': 'measurement_time',
        'data_type': 'timestamp'
    },
    cluster_by = ['location']
) }}

SELECT * FROM {{ ref('stg_finchley_pol_data') }}
UNION ALL
SELECT * FROM {{ ref('stg_finsburypark_pol_data') }}
UNION ALL
SELECT * FROM {{ ref('stg_stpauls_pol_data') }}
UNION ALL
SELECT * FROM {{ ref('stg_woodgreen_pol_data') }}
