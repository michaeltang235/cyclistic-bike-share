#--------------------------------------------------------------------
# This script read all .csv files in input data directory, then
# create processed dataframe, df_tot_tableau

# df_tot_tableau is created by,
# (i) concatenate df read from all .csv files vertically,
# (ii) remove columns containing incomplete data (i.e. missing lat, log data)
# (iii) compute the following new columns,
# (a) ride length, defined as ride end time - ride start time
# (iv) output processed data frame, df_tot to path specified
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
#for item in full_path_matched:   # for every path matched
for i in range(6, 12):  # for the last  paths matched
    df = pd.read_csv(full_path_matched[i], usecols=list(range(4)) + list(range(8, 13)))
    df_tot = pd.concat([df_tot, df], axis = 0, ignore_index = True)

# get ride length in seconds, store data to new column 'ride_length'
df_tot['ride_length'] = (pd.to_datetime(df_tot['ended_at']) -
                         pd.to_datetime(df_tot['started_at'])).dt.total_seconds()

# drop columns that aren't required in dashboard that's going to be made
df_tot = df_tot.drop(['ended_at', 'end_lat', 'end_lng'], axis = 1)

# obtain df_tot_tableau by removing rows with NULL values in df_tot
df_tot_tableau = df_tot.dropna()

# write processed data frame, df_tot and df_tot_station_name_member_casual in .csv files,
# save file to path specified below
direct_op = '/home/siumichael.tang/bike_share/data_tableau'   # dir. of output file
filename_op_df_tot_tableau = 'trip_data_proc_tableau.csv'   # output filename of df_tot_tableau

filepath_op_df_tot_tableau = os.path.join(direct_op, filename_op_df_tot_tableau)   # assemble full path of output file df_tot_tableau

df_tot_tableau.to_csv(filepath_op_df_tot_tableau)   # save df_tot_tableau to path

# print message to console
print('done processing data')