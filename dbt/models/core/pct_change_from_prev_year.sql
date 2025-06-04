{{ config(materialized='table') }}

with pollution_data as (
    select * from {{ ref('fct_pollution_data') }}
),
location_latest_recorded_full_day as (
    select location,
        date(date_sub(max(measurement_time), interval 1 day)) as location_latest_recorded_day
    from pollution_data
    group by location
),
latest_day_data as (
    select date(measurement_time) as latest_day,
            pollution_data.location,
            avg(co) as current_co_avg,
            avg(`no`) as current_no_avg,
            avg(no2) as current_no2_avg,
            avg(o3) as current_o3_avg,
            avg(so2) as current_so2_avg,
            avg(pm2_5) as current_pm2_5_avg,
            avg(pm10) as current_pm10_avg,
            avg(nh3) as current_nh3_avg
        from pollution_data
        join location_latest_recorded_full_day llrfd on llrfd.location = pollution_data.location
        where date(measurement_time) = llrfd.location_latest_recorded_day
        group by date(measurement_time), pollution_data.location
),
same_day_previous_year_data as (
    select date(measurement_time),
            pollution_data.location,
            avg(co) as prev_co_avg,
            avg(`no`) as prev_no_avg,
            avg(no2) as prev_no2_avg,
            avg(o3) as prev_o3_avg,
            avg(so2) as prev_so2_avg,
            avg(pm2_5) as prev_pm2_5_avg,
            avg(pm10) as prev_pm10_avg,
            avg(nh3) as prev_nh3_avg
        from pollution_data
        join location_latest_recorded_full_day llrfd on llrfd.location = pollution_data.location
        where date(measurement_time) = date_sub(llrfd.location_latest_recorded_day, interval 1 year)
        group by date(measurement_time), pollution_data.location
)

select ldd.location,
    ldd.latest_day,
    100*(current_co_avg - prev_co_avg)/current_co_avg as co_pct_change,
    100*(current_no_avg - prev_no_avg)/current_no_avg as no_pct_change,
    100*(current_no2_avg - prev_no2_avg)/current_no2_avg as no2_pct_change,
    100*(current_o3_avg - prev_o3_avg)/current_o3_avg as o3_pct_change,
    100*(current_so2_avg - prev_so2_avg)/current_so2_avg as so2_pct_change,
    100*(current_pm2_5_avg - prev_pm2_5_avg)/current_pm2_5_avg as pm2_5_pct_change,
    100*(current_pm10_avg - prev_pm10_avg)/current_pm10_avg as pm10_pct_change,
    100*(current_nh3_avg - prev_nh3_avg)/current_nh3_avg as nh3_pct_change
from latest_day_data ldd
join same_day_previous_year_data sdpyd on sdpyd.location = ldd.location
