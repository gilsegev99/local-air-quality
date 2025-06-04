{{ config(materialized='table') }}

with pollution_data as (
    select * from {{ ref('fct_pollution_data') }}
),
daily_avg_pivoted as (
    select date(measurement_time) as `date`,
        location,
        avg(co) as daily_co_avg,
        avg(`no`) as daily_no_avg,
        avg(no2) as daily_no2_avg,
        avg(o3) as daily_o3_avg,
        avg(so2) as daily_so2_avg,
        avg(pm2_5) as daily_pm2_5_avg,
        avg(pm10) as daily_pm10_avg,
        avg(nh3) as daily_nh3_avg
        from pollution_data
        group by date(measurement_time), location
)

select `date`, location, pollutant, daily_avg from daily_avg_pivoted
unpivot (
  daily_avg for pollutant in (
    daily_co_avg as 'co',
    daily_no_avg as 'no',
    daily_no2_avg as 'no2',
    daily_so2_avg as 'so2',
    daily_pm2_5_avg as 'pm2_5',
    daily_pm10_avg as 'pm10',
    daily_nh3_avg as 'nh3'
  )
)
