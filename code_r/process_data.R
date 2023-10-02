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
# load packages
library(tidyr)
library(dplyr)
library(lubridate)
#library(tidyverse) 

# specify path where input data are
path_req <- '/home/siumichael.tang/bike_share/input_data/'
#path_req <- '/cloud/project/bike_share/input_data/'

# obtain a list of .csv input files in path specified
file_list <- list.files(path_req, pattern = '.csv')

# read each .csv file, remove entries under 6th to 8th columns as they are
# not complete, store data read in curr_df, 
# then use rbind() to append content in curr_df vertically to df_read
df_read <- data.frame()   # initialize var data as data frame
for (i in 1:length(file_list)){
  curr_df <- read.csv(paste(path_req, file_list[i], sep = '')) %>% select(-c(6:8))
  df_read <- rbind(df_read, curr_df)
}

# create additional columns, ride_length, day_of_week, month_of_yr, hour_of_day,
# ride_length = length of ride in seconds
# day_of_week/month_of_yr/hour_of_day = day of week/month/hour of the ride
# here wday() with week_start = 1 denotes monday as 1 and sunday as 7, store
# output in df, use as.POSIXlt() to convert chr to datetime type
df_tot <- mutate(df_read, ride_length = as.POSIXlt(ended_at) - as.POSIXlt(started_at)) %>%
  mutate(df_read, day_of_week = wday(as.POSIXlt(started_at), week_start = 1)) %>%
  mutate(df_read, month_of_yr = month(as.POSIXlt(started_at))) %>%
  mutate(df_read, hour_of_day = hour(as.POSIXlt(started_at)))

# as entries under 'start_station_name' are not complete across all input .csv files
# repeat the above but only store rows under 'start_station_name' and 'member_casual' for
# every .csv file in a separate dataframe, df_tot_st_name_mem_cas,
df_tot_st_name_mem_cas <- data.frame()   # initialize data frame, df_tot_st_name_mem_cas
for (i in 1:length(file_list)){
    curr_df <-read.csv(paste(path_req, file_list[i], sep = '')) %>% select(c(5, 13))
    df_tot_st_name_mem_cas <- rbind(df_tot_st_name_mem_cas, curr_df)
}

# as entries under 'start_station_name' contain '' empty values
# removing those rows, and store resultant df in df_tot_station_name_member_casual
df_tot_station_name_member_casual = df_tot_st_name_mem_cas[!(df_tot_st_name_mem_cas$start_station_name == ''), ]

# write processed dataframes, df_tot and df_tot_station_name_member_casual in .csv file,
# save file to path specified below
filedir_op <- '/home/siumichael.tang/bike_share/data_r/'
filename_op_df_tot <- 'trip_data_proc.csv'   # output filename of df_tot
filename_op_df_tot_station_name_member_casual <- 'trip_data_station_name_proc.csv'   # output filename of df_tot_station_name_member_casual

filepath_op_df_tot <- file.path(filedir_op, filename_op_df_tot)   # assemble output file path of df_tot
filepath_op_df_tot_station_name_member_casual <- file.path(filedir_op, filename_op_df_tot_station_name_member_casual)   # assemble output file path of df_tot_station_name_member_casual

write.csv(df_tot, filepath_op_df_tot)
write.csv(df_tot_station_name_member_casual, filepath_op_df_tot_station_name_member_casual)

# print message to console
print('done processing data')