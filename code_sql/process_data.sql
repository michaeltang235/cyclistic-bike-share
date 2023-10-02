
/* This query was run on BigQuery free tier server, with no DML allowed, 
-- i.e. UPDATE, DELETE, etc., are not permitted

-- This script read all .csv files in database, then
-- create temp table, df_tot_temp, and from there, 
-- create two processed tables, trip_data_proc and trip_data_station_name_proc.

-- trip_data_proc is created by,
--(i) concatenate table read from all .csv files vertically,
-- (ii) remove columns containing incomplete data
-- (iii) compute the following new columns,
-- (a) ride length, defined as ride end time - ride start time
-- (b) day of the week of ride start time
-- (c) month of year of ride start time
-- (d) hour of ride start time
-- (iv) output processed data frame, df_tot to path specified

-- trip_data_station_name_proc is created by
-- (i) vertically concatenating columns 'start_station_name' and 'member_casual'
-- from each .csv file
-- (ii) removing rows with Null or NaN entries under 'start_station_name'

-- BigQuery's timestamp function:
-- https://cloud.google.com/bigquery/docs/reference/standard-sql/timestamp_functions
--------------------------------------------------------------------------
*/


-- drop tables if they already exist in database
DROP TABLE IF EXISTS `my-project-41210.bike_share.trip_data_proc`;
DROP TABLE IF EXISTS `my-project-41210.bike_share.trip_data_station_name_proc`;


-- create temp table, df_tot_temp (temp table will be dropped after session) 
-- by first selecting
-- all columns from every table available
-- vertically concatenate tables using UNION ALL

CREATE TEMP TABLE df_tot_temp  AS 
SELECT *
FROM `my-project-41210.bike_share.202211-divvy-tripdata` 
UNION ALL
SELECT * 
FROM `my-project-41210.bike_share.202212-divvy-tripdata` 
UNION ALL
SELECT *
FROM `my-project-41210.bike_share.202301-divvy-tripdata` 
UNION ALL
SELECT *
FROM `my-project-41210.bike_share.202302-divvy-tripdata` 
UNION ALL
SELECT * 
FROM `my-project-41210.bike_share.202303-divvy-tripdata` 
UNION ALL
SELECT *
FROM `my-project-41210.bike_share.202304-divvy-tripdata`;


-- alter df_tot_temp created by dropping incomplete columns,
-- which contain missing entries

ALTER TABLE df_tot_temp
DROP COLUMN start_station_name,
DROP COLUMN start_station_id, 
DROP COLUMN end_station_name, 
DROP COLUMN end_station_id;


-- create new table named trip_data_proc in database, which contains
-- all columns in df_tot_temp, with the following additional columns
-- ride_length = ended_at - started_at in seconds,
-- day_of_week = day of week of started_at (1 = sunday, 7 = saturday),
-- month_of_year = month of year of started_at,
-- hour_of_day = hour of day of started at

-- here, started_at and ended_at are columns of TIMESTAMP value,
-- use TIMESTAMP_DIFF() and EXTRACT() to get info,
-- DAYOFWEEK() function returns 1 = sunday and 7 = saturday

CREATE TABLE `my-project-41210.bike_share.trip_data_proc` AS
SELECT *, 
  TIMESTAMP_DIFF(ended_at, started_at, SECOND) AS ride_length, 
  EXTRACT(DAYOFWEEK FROM started_at) AS day_of_week, 
  EXTRACT(MONTH FROM started_at) AS month_of_year, 
  EXTRACT(HOUR FROM started_at) AS hour_of_day
FROM df_tot_temp;


-- next, create table, trip_data_station_name_proc, which contains
-- only start_station_name and member_casual from every table input,
-- remove all rows with NULL (empty) under start_station_name,
-- use UNION ALL to allow duplicate rows (here only 2 columns are considered)

CREATE TABLE `my-project-41210.bike_share.trip_data_station_name_proc` AS
SELECT *
FROM (
  SELECT start_station_name, member_casual
  FROM `my-project-41210.bike_share.202211-divvy-tripdata`
  UNION ALL
  SELECT start_station_name, member_casual
  FROM `my-project-41210.bike_share.202212-divvy-tripdata`
  UNION ALL
  SELECT start_station_name, member_casual
  FROM `my-project-41210.bike_share.202301-divvy-tripdata`
  UNION ALL
  SELECT start_station_name, member_casual
  FROM `my-project-41210.bike_share.202302-divvy-tripdata`
  UNION ALL
  SELECT start_station_name, member_casual
  FROM `my-project-41210.bike_share.202303-divvy-tripdata`
  UNION ALL
  SELECT start_station_name, member_casual
  FROM `my-project-41210.bike_share.202304-divvy-tripdata`
)
WHERE start_station_name IS NOT NULL;

