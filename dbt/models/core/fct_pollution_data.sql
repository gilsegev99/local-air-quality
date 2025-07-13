 {{ config(
    materialized = 'incremental',
    unique_key='measurementid',
    partition_by = {
        'field': 'measurement_time',
        'data_type': 'timestamp',
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


{% if is_incremental() %}

  -- this filter will only be applied on an incremental run
  -- (uses >= to include records arriving later on the same day as the last run of this model)
  where measurement_time >= (select coalesce(max(measurement_time), timestamp("2020-11-27 00:00:00+00")) from {{ this }})

{% endif %}