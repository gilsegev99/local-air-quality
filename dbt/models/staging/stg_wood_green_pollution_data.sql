
with pollutiondata as (
    select *,
        'WoodGreen' as location,
        row_number() over(partition by lon, lat, `time`) as rn
    from {{ source('staging', 'raw_woodgreen')}}
    where lon is not null
        and lat is not null
        and `time` is not null
)

select
    -- identifiers
    {{ dbt_utils.generate_surrogate_key(['location', 'lon', 'lat', 'time']) }} as measurementid,
    location,

    -- measurement parameters
    {{ dbt.safe_cast("lon", api.Column.translate_type("float")) }} as lon,
    {{ dbt.safe_cast("lat", api.Column.translate_type("float")) }} as lat,
    TIMESTAMP_SECONDS(safe_cast(`time` as integer)) as measurement_time,

    -- measurment data
    {{ dbt.safe_cast("aqi", api.Column.translate_type("integer")) }} as aqi,
    {{ get_aqi_category("aqi") }} as aqi_category,
    co,
    `no`,
    no2,
    o3,
    so2,
    pm2_5,
    pm10,
    nh3
from pollutiondata
where rn = 1

-- dbt build --select <model_name> --vars '{'is_test_run': 'false'}'
{% if var('is_test_run', default=true) %}

   limit 100

{% endif %}
