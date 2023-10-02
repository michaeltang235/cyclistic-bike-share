#--------------------------------------------------------------------
# This script read all .csv files in input data directory, then
# create two processed dataframes, df_tot and df_tot_station_name_member_casual.

# df_tot is created by,
# (i) concatenate df read from all .csv files vertically,
# (ii) remove columns containing incomplete data
# (iii) compute the following new columns,
# (a) ride length, defined as ride end time - ride start time
# (b) day of the week of ride start time
# (c) month of year of ride start time
# (d) hour of ride start time
# (iv) output processed data frame, df_tot to path specified

# df_tot_station_name_member_casual is created by
# (i) vertically concatenating columns 'start_station_name' and 'member_casual'
# from each .csv file
# (ii) removing rows with Null or NaN entries under 'start_station_name'
#--------------------------------------------------------------------

import os
import re
import pandas as pd
import numpy as np

# specify path where input data are
direct_req = '/home/siumichael.tang/bike_share/input_data/'
#path_req = '/cloud/project/bike_share/input_data/'

# enter format of input files to be read
filename_tripdata = '.*\.csv'  # file containing mni coord. of all electrode pairs

# obtain a list of .csv files from input data directory

# identify all files within directory input
file_list = os.listdir(direct_req)

full_path_matched = []   # initialize list of full_path_matched

for item in file_list:  # for every filename in input data dir.
    # obtain match object
    cur_filename = re.search(filename_tripdata, item)
    # if matched object is found, obtain its full path
    if cur_filename:
        full_path = os.path.join(direct_req, cur_filename.string)
        full_path_matched.append(full_path)  # append info to output list

# read .csv input data, omit 4th to 7th columns as they are not complete
# concatenate vertically each data frame read
df_tot = pd.DataFrame()   # initialize data frame, df_tot
for item in full_path_matched:   # for every path matched
    df = pd.read_csv(item, usecols=list(range(4)) + list(range(8, 13)))
    df_tot = pd.concat([df_tot, df], axis = 0, ignore_index = True)

# get ride length in seconds, store data to new column 'ride_length'
df_tot['ride_length'] = (pd.to_datetime(df_tot['ended_at']) - pd.to_datetime(df_tot['started_at'])).dt.total_seconds()

# get day of week of started_at, monday = 0, and sunday = 6, store data to new
# column 'day_of_week'
df_tot['day_of_week'] = pd.to_datetime(df_tot['started_at']).dt.dayofweek

# get month of year of started_at, store data to column, 'month_of_year'
df_tot['month_of_year'] = pd.to_datetime(df_tot['started_at']).dt.month

# get hour of day of started_at,store data to column, 'hour_of_day'
df_tot['hour_of_day'] = pd.to_datetime(df_tot['started_at']).dt.hour

# as entries under 'start_station_name' are not complete across all input .csv files
# repeat the above but only store rows under 'start_station_name' and 'member_casual' for
# every .csv file in a separate dataframe, df_tot_st_name_mem_cas,
df_tot_st_name_mem_cas = pd.DataFrame()   # initialize data frame, df_tot_st_name_mem_cas
for item in full_path_matched:   # for every path matched
    df = pd.read_csv(item, usecols=[4, 12])
    df_tot_st_name_mem_cas = pd.concat([df_tot_st_name_mem_cas, df], axis = 0, ignore_index = True)

# as entries under 'start_station_name' contain Null, None, NaN, NaT values,
# removing those rows, and store resultant df in df_tot_station_name_member_casual
df_tot_station_name_member_casual = df_tot_st_name_mem_cas.dropna()

# write processed data frame, df_tot and df_tot_station_name_member_casual in .csv files,
# save file to path specified below
direct_op = '/home/siumichael.tang/bike_share/data_py'   # dir. of output file
filename_op_df_tot = 'trip_data_proc.csv'   # output filename of df_tot
filename_op_df_tot_station_name_member_casual = 'trip_data_station_name_proc.csv'   # output filename of df_tot_station_name_member_casual

filepath_op_df_tot = os.path.join(direct_op, filename_op_df_tot)   # assemble full path of output file df_tot
filepath_op_df_tot_station_name_member_casual = os.path.join(direct_op, filename_op_df_tot_station_name_member_casual)   # assemble full path of output file df_tot_station_name_member_casual

df_tot.to_csv(filepath_op_df_tot)   # save df_tot to path
df_tot_station_name_member_casual.to_csv(filepath_op_df_tot_station_name_member_casual)   # save df_tot_station_name_member_casual to path

# print message to console
print('done processing data')