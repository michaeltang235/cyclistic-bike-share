#---------------------------------------------
# This script reads data from two processed .csv files,
# 'trip_data_proc.csv' and 'trip_data_station_name_proc.csv'.

# In df read from 'trip_data_proc.csv', 'ride_length' is grouped
# by the following column name(s), and output the corresponding sub-dataframe to path,
# year, called it stat_yr,
# month, called it stat_month,
# day_of_week, called it stat_day_of_week,
# hour_of_day, called it stat_hour_of_day,
# member_casual, called it stat_user,
# member_casual and month, called it stat_user_month,
# member_casual and day_of_week, called it stat_user_day_of_week,
# member_casual and hour_of_day, called it stat_user_hour_of_day.
# member_causal and rideable_type, called it stat_user_rideable_type

# In df read from 'trip_data_station_name_proc.csv', ride count percentage of every rider type
# in every station was obtained. Output df was generated by sorting the ride count perct in
# descending order for each rider type. Note, only stations with ride count >= mean ride count
# of each rider type were included in the output dfs.

# ref on categorical method of pd:
# https://saturncloud.io/blog/how-to-sort-pandas-dataframe-by-custom-order-on-string-index/
#---------------------------------------------

import os
import re
import pandas as pd
import numpy as np

# specify path where input data are
direct_req = '/home/siumichael.tang/bike_share/data_py/'
#path_req = '/cloud/project/bike_share/input_data/'

# enter format of processed trip data to be read
filename_tripdata = 'trip_data_proc.csv'
filename_tripdata_station_name = 'trip_data_station_name_proc.csv'

# obtain full path of processed data file
full_path_trip_data = os.path.join(direct_req, filename_tripdata)
full_path_trip_data_station_name = os.path.join(direct_req, filename_tripdata_station_name)

# read processed data into data frames, df_tot and df_tot_station_name
df_tot = pd.read_csv(full_path_trip_data)
df_tot_station_name = pd.read_csv(full_path_trip_data_station_name)

# get stats by year
stat_data_yr = df_tot['ride_length'].agg(['mean', 'max', 'count']).values
stat_yr = pd.DataFrame({'mean_ride_length': stat_data_yr[0] , 'max_ride_length': stat_data_yr[1],
                        'ride_count': stat_data_yr[2]}, index = [0])

# get stats by month, drop row index
stat_month = df_tot.groupby('month_of_year')['ride_length'].agg(['mean', 'max', 'count']).reset_index()
stat_month.rename(columns = {'mean': 'mean_ride_length', 'max': 'max_ride_length',\
                                'count': 'ride_count'}, inplace = True)

# create customized month_order to denote months go from May to Dec, then Jan to Apr
month_order = list(range(5, 13, 1)) + list(range(1, 5, 1))

# convert the column 'month_of_year' to categorical data with customized month order specified
stat_month['month_of_year'] = pd.Categorical(stat_month['month_of_year'], categories = month_order, ordered = True)

# update stat_month by the column 'month_of_year' with the customized month order
stat_month = stat_month.sort_values(by = ['month_of_year'])

# get stats by day of week when trip started, in pd, monday = 0, and sunday = 6
stat_day_of_week = df_tot.groupby('day_of_week')['ride_length'].agg(['mean', 'max', 'count']).reset_index()
stat_day_of_week.rename(columns = {'mean': 'mean_ride_length', 'max': 'max_ride_length',\
                                'count': 'ride_count'}, inplace = True)

# get stats by hour of when trip started, in pd, 00:00 = 0, and 23:00 = 23
stat_hour_of_day = df_tot.groupby('hour_of_day')['ride_length'].agg(['mean', 'max', 'count']).reset_index()
stat_hour_of_day.rename(columns = {'mean': 'mean_ride_length', 'max': 'max_ride_length',\
                                'count': 'ride_count'}, inplace = True)

# get stats by user type,
stat_user = df_tot.groupby('member_casual')['ride_length'].agg(['mean', 'max', 'count']).reset_index()
stat_user.rename(columns = {'mean': 'mean_ride_length', 'max': 'max_ride_length',\
                                'count': 'ride_count'}, inplace = True)
# rename column names, innplace = true, set changes to data frame permanently

# get stats by user type and month
stat_user_month = df_tot.groupby(['member_casual', 'month_of_year'])\
    ['ride_length'].agg(['mean', 'max', 'count']).reset_index()   # reset_index = convert row index to column
stat_user_month.rename(columns = {'mean': 'mean_ride_length', 'max': 'max_ride_length',\
                                'count': 'ride_count'}, inplace = True)   # set column names

# convert column 'month_of_year' in stat_user_month to categorical dtype with customized order of months
stat_user_month['month_of_year'] = pd.Categorical(stat_user_month['month_of_year'], \
                                                  categories = month_order, ordered = True)

# sort stat_user_month by 'member_casual' and 'month_of_year'
stat_user_month = stat_user_month.sort_values(by = ['member_casual', 'month_of_year'])

# get stats by user type and day of week
stat_user_day_of_week = df_tot.groupby(['member_casual', 'day_of_week'])\
    ['ride_length'].agg(['mean', 'max', 'count']).reset_index()   # reset_index = convert row index to column
stat_user_day_of_week.rename(columns = {'mean': 'mean_ride_length', 'max': 'max_ride_length',\
                                'count': 'ride_count'}, inplace = True)   # set column names

# get stats by user type and hour of day
stat_user_hour_of_day = df_tot.groupby(['member_casual', 'hour_of_day'])\
    ['ride_length'].agg(['mean', 'max', 'count']).reset_index()   # reset_index = convert row index to column
stat_user_hour_of_day.rename(columns = {'mean': 'mean_ride_length', 'max': 'max_ride_length',\
                                'count': 'ride_count'}, inplace = True)   # set column names

# get stats by user type and rideable type
stat_user_rideable_type = df_tot.groupby(['member_casual', 'rideable_type'])['ride_length'].agg(['count']).reset_index()
stat_user_rideable_type.rename(columns = {'count': 'ride_count'}, inplace = True)   # set column names


# get ride count percentage (in descending order) of each rider type in every station:

# group rows by columns, member_casual and start_station_name, and get their ride count
df_user_start_station_name = df_tot_station_name.groupby(['member_casual', 'start_station_name'])\
    ['start_station_name'].agg(['count']).reset_index()
df_user_start_station_name.rename(columns = {'count': 'ride_count'}, inplace = True)   # set column names

# obtain subsets of the grouped dataframe as df_casual_user_station and df_member_user_station, where
# df_casual_user_station contains ride count of casual riders for each station, while
# df_casual_member_station contains ride count of member riders for each station
df_casual_user_station = df_user_start_station_name.loc[df_user_start_station_name['member_casual'] == 'casual']
df_member_user_station = df_user_start_station_name.loc[df_user_start_station_name['member_casual'] == 'member']

# perform inner join between the two dataframes on column 'start_station_name', store result in df_user_station_merged
# df_user_station_merged contains ride counts of casual and member riders of every station
df_user_station_merged = df_casual_user_station.merge(df_member_user_station, how = 'inner', on = 'start_station_name',
                                                      suffixes = ('_casual', '_member'))

# get percentage of ride count by rider type for every station, store values under new column named
# 'ride_count_perct_casual' and 'ride_count_perct_member'
df_user_station_merged['ride_count_perct_casual'] = \
    df_user_station_merged['ride_count_casual'] / (df_user_station_merged['ride_count_casual'] + \
                                                   df_user_station_merged['ride_count_member'])

df_user_station_merged['ride_count_perct_member'] = \
    df_user_station_merged['ride_count_member'] / (df_user_station_merged['ride_count_casual'] + \
                                                   df_user_station_merged['ride_count_member'])

# obtain mean ride count across all stations for each rider type
mean_ride_count_casual = df_user_station_merged['ride_count_casual'].mean()
mean_ride_count_member = df_user_station_merged['ride_count_member'].mean()

# filter df_user_station_merged by selecting rows with
# (i) ride_count_casual >= mean_ride_count_casual, and
# (ii) ride_count_member >= mean_ride_count_member,
# store filtered df in df_user_station_filtered
# df_user_station_filtered contains ride count for each rider type only for stations with ride counts >= mean ride
# count of each rider type
df_user_station_filtered = df_user_station_merged.loc[(df_user_station_merged['ride_count_casual'] >= mean_ride_count_casual) \
                                                        & (df_user_station_merged['ride_count_member'] >= mean_ride_count_member)]

# sort ride count percentage of each rider type in descending order, store resultant df in
# stat_casual_station_filtered_sorted and stat_member_station_filtered_sorted
# stat_casual(OR member)_station_filtered_sorted contains ride count for every station that has ride count >= mean ride
# count of each rider type, and rows are sorted in descending order of casual(OR member) ride count percentage,
stat_casual_station_filtered_sorted = df_user_station_filtered.sort_values(by = ['ride_count_perct_casual'], ascending = False)
stat_member_station_filtered_sorted = df_user_station_filtered.sort_values(by = ['ride_count_perct_member'], ascending = False)

# note: stations with high ride count percentages for each rider type did not necessarily mean that the stations
# were popular among riders, therefore, only those with ride count >= mean ride count of every rider type were
# considered. Afterward, the df was sorted in descending order by ride count percentage of each rider type,
# generating one df for casual riders (i.e. stat_casual_station_filtered_sorted) and one for
# member riders (i.e. stat_member_station_filtered_sorted).


# write each of the analyzed dataframes above in a .csv file,

# save file to path specified below
direct_op = '/home/siumichael.tang/bike_share/data_py'   # dir. of output file
filename_op_month = 'stat_month.csv'   # output filename of stat_month
filename_op_day_of_week = 'stat_day_of_week.csv'   # output filename of stat_day_of_week
filename_op_hour_of_day = 'stat_hour_of_day.csv'   # output filename of stat_hour_of_day
filename_op_user = 'stat_user.csv'   # output filename of stat_user
filename_op_user_month = 'stat_user_month.csv'   # output filename of stat_user_month
filename_op_user_day_of_week = 'stat_user_day_of_week.csv'   # output filename of stat_user_day_of_week
filename_op_user_hour_of_day = 'stat_user_hour_of_day.csv'   # output filename of stat_user_hour_of_day
filename_op_user_rideable_type = 'stat_user_rideable_type.csv'   # output filename of stat_user_rideable_type
filename_op_casual_station_filtered_sorted = 'stat_casual_station_filtered_sorted.csv'   # output filename of stat_casual_station_filtered_sorted
filename_op_member_station_filtered_sorted = 'stat_member_station_filtered_sorted.csv'   # output filename of stat_member_station_filtered_sorted

# assemble full path of output file for each of the dataframes
filepath_op_month = os.path.join(direct_op, filename_op_month)   # assemble full path of stat_month
filepath_op_day_of_week = os.path.join(direct_op, filename_op_day_of_week)   # assemble full path of stat_day_of_week
filepath_op_hour_of_day = os.path.join(direct_op, filename_op_hour_of_day)   # assemble full path of stat_hour_of_day
filepath_op_user = os.path.join(direct_op, filename_op_user)   # assemble full path of stat_user
filepath_op_user_month = os.path.join(direct_op, filename_op_user_month)   # assemble full path of stat_user_month
filepath_op_user_day_of_week = os.path.join(direct_op, filename_op_user_day_of_week)   # assemble full path of stat_user_day_of_week
filepath_op_user_hour_of_day = os.path.join(direct_op, filename_op_user_hour_of_day)   # assemble full path of stat_user_hour_of_day
filepath_op_user_rideable_type = os.path.join(direct_op, filename_op_user_rideable_type)   # assemble full path of stat_user_rideable_type
filepath_op_casual_station_filtered_sorted = os.path.join(direct_op, filename_op_casual_station_filtered_sorted)   # assemble full path of stat_casual_station_filtered_sorted
filepath_op_member_station_filtered_sorted = os.path.join(direct_op, filename_op_member_station_filtered_sorted)   # assemble full path of stat_member_station_filtered_sorted

# save each dataframe to path, remove row index
stat_month.to_csv(filepath_op_month, index=False)   # save stat_month to path, remove row index
stat_day_of_week.to_csv(filepath_op_day_of_week, index=False)   # save stat_day_of_week to path, remove row index
stat_hour_of_day.to_csv(filepath_op_hour_of_day, index=False)   # save stat_hour_of_day to path, remove row index
stat_user.to_csv(filepath_op_user, index=False)   # save stat_user to path, remove row index
stat_user_month.to_csv(filepath_op_user_month, index=False)   # save stat_user_month to path, remove row index
stat_user_day_of_week.to_csv(filepath_op_user_day_of_week, index=False)   # save stat_user_day_of_week to path, remove row index
stat_user_hour_of_day.to_csv(filepath_op_user_hour_of_day, index=False)   # save stat_user_hour_of_day to path, remove row index
stat_user_rideable_type.to_csv(filepath_op_user_rideable_type, index=False)   # save stat_user_rideable_type to path, remove row index
stat_casual_station_filtered_sorted.to_csv(filepath_op_casual_station_filtered_sorted, index=False)   # save stat_casual_station_filtered_sorted to path, remove row index
stat_member_station_filtered_sorted.to_csv(filepath_op_member_station_filtered_sorted, index=False)   # save stat_member_station_filtered_sorted to path, remove row index

# print message to console
print('done analyzing data and outputting dataframes')