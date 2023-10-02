# https://saturncloud.io/blog/how-to-sort-pandas-dataframe-by-custom-order-on-string-index/
#https://github.com/sam-is-curious/Google-Data-Analytics-Capstone-Project-Cyclistic-Bike-Share
# https://public.tableau.com/app/profile/tucker.trost/viz/CyclisticCaseStudy-GoogleDataAnalysticsCertificate/CyclisticCaseStudy

#--------------------------------------
# This script does the following,
# (1)
# intakes a set of stat_user_TIME.csv from database, where
# TIME denotes 'month', 'day_of_week', and 'hour_of_day' in the filename,
# and makes subplots comparing mean ride length [min] between casual and member
# riders in every month, every day of the week, and every hour of the day.
# Here, TIME denotes 'month', 'day_of_week', and 'hour_of_day' in the filename
# (2)
# intakes 'stat_TYPE_station_filtered_sorted.csv' from database, where TYPE
# denotes 'casual' and 'member' in the filename, and makes subplots
# comparing ride count percentage between casual and member riders in their
# top 20 most popular starting stations. Note, only starting stations with
# ride count >= mean ride count of both causal and member riders are considered.
#--------------------------------------

import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# specify path where input data are
#direct_req = '/home/siumichael.tang/bike_share/data_py/'
direct_req = 'C:\\Users\\siumichael.tang\\Downloads\\bike_share\\data_py'

# enter format of stats dataframes to be read
filename_stat_user_month = 'stat_user_month.csv'
filename_stat_user_day_of_week = 'stat_user_day_of_week.csv'
filename_stat_user_hour_of_day = 'stat_user_hour_of_day.csv'

filename_stat_casual_station_filtered_sorted = 'stat_casual_station_filtered_sorted.csv'
filename_stat_member_station_filtered_sorted = 'stat_member_station_filtered_sorted.csv'

# obtain full path of input .csv files
full_path_stat_user_month =  os.path.join(direct_req, filename_stat_user_month)
full_path_stat_user_day_of_week =  os.path.join(direct_req, filename_stat_user_day_of_week)
full_path_stat_user_hour_of_day =  os.path.join(direct_req, filename_stat_user_hour_of_day)

full_path_stat_casual_station_filtered_sorted =  os.path.join(direct_req, filename_stat_casual_station_filtered_sorted)
full_path_stat_member_station_filtered_sorted =  os.path.join(direct_req, filename_stat_member_station_filtered_sorted)

# read .csv files into dataframes
stat_user_month = pd.read_csv(full_path_stat_user_month)
stat_user_day_of_week = pd.read_csv(full_path_stat_user_day_of_week)
stat_user_hour_of_day = pd.read_csv(full_path_stat_user_hour_of_day)

stat_casual_station_filtered_sorted = pd.read_csv(full_path_stat_casual_station_filtered_sorted)
stat_member_station_filtered_sorted = pd.read_csv(full_path_stat_member_station_filtered_sorted)

# obtain subset of every dataframe, filtered by membership type
stat_user_month_casual = stat_user_month.loc[stat_user_month['member_casual'] == 'casual']
stat_user_month_member = stat_user_month.loc[stat_user_month['member_casual'] == 'member']

stat_user_day_of_week_casual = stat_user_day_of_week.loc[stat_user_day_of_week['member_casual'] == 'casual']
stat_user_day_of_week_member = stat_user_day_of_week.loc[stat_user_day_of_week['member_casual'] == 'member']

stat_user_hour_of_day_casual = stat_user_hour_of_day.loc[stat_user_hour_of_day['member_casual'] == 'casual']
stat_user_hour_of_day_member = stat_user_hour_of_day.loc[stat_user_hour_of_day['member_casual'] == 'member']

#--------------------------------------
# make subplots (time series, line plots)

# create x data arrays for each subplot
x_month = range(0, 12, 1)
x_day_of_week = range(0, 7, 1)
x_hour_of_day = range(0, 24, 1)
x_hour_of_day_tick = range(0, 24, 2)

# initialize subplot handle
fig1, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3, sharex = 'col', sharey = 'row')
fig1.tight_layout()

# set figure window size
fig1.set_figwidth(15)
fig1.set_figheight(15/3)

# plot each subplot
ax1.plot(x_month, stat_user_month_casual['mean_ride_length']/60, color = 'royalblue', label = 'casual')
ax1.plot(x_month, stat_user_month_member['mean_ride_length']/60, color = 'orangered', label = 'member')

ax2.plot(x_day_of_week, stat_user_day_of_week_casual['mean_ride_length']/60, color = 'royalblue', label = 'casual')
ax2.plot(x_day_of_week, stat_user_day_of_week_member['mean_ride_length']/60, color = 'orangered', label = 'member')

ax3.plot(x_hour_of_day, stat_user_hour_of_day_casual['mean_ride_length']/60, color = 'royalblue', label = 'casual')
ax3.plot(x_hour_of_day, stat_user_hour_of_day_member['mean_ride_length']/60, color = 'orangered', label = 'member')

ax4.plot(x_month, stat_user_month_casual['ride_count'], color = 'royalblue', label = 'casual')
ax4.plot(x_month, stat_user_month_member['ride_count'], color = 'orangered', label = 'member')

ax5.plot(x_day_of_week, stat_user_day_of_week_casual['ride_count'], color = 'royalblue', label = 'casual')
ax5.plot(x_day_of_week, stat_user_day_of_week_member['ride_count'], color = 'orangered', label = 'member')

ax6.plot(x_hour_of_day, stat_user_hour_of_day_casual['ride_count'], color = 'royalblue', label = 'casual')
ax6.plot(x_hour_of_day, stat_user_hour_of_day_member['ride_count'], color = 'orangered', label = 'member')

# set axes labels
ax1.set_ylabel('Mean ride length [min]')
ax4.set_ylabel('Ride count')
ax4.set_xlabel('Months')
ax5.set_xlabel('Day of week')
ax6.set_xlabel('Hour of day [HH]')

# set tick positions and tick labels
month_str = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr']
ax4.set_xticks(x_month)
ax4.set_xticklabels(month_str)

day_of_week_str = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
ax5.set_xticks(x_day_of_week)
ax5.set_xticklabels(day_of_week_str)

#hour_of_day_str = ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', \
#                   '16:00', '18:00', '20:00', '22:00']
hour_of_day_str = ['00', '02', '04', '06', '08', '10', '12', '14', '16', '18', '20', '22']
ax6.set_xticks(x_hour_of_day_tick)
ax6.set_xticklabels(hour_of_day_str)

# set new y-ticks and labels
curr_ax4_y_tick = ax4.get_yticks()
y_ride_count = curr_ax4_y_tick[curr_ax4_y_tick >= 0]
ride_count_str = ['{}'.format(int(item/1000)) + 'K' for item in y_ride_count]
ride_count_str.pop(0)
ride_count_str = ['0'] + ride_count_str

# update y-ticks and labels on ax4
ax4.set_yticks(y_ride_count)
ax4.set_yticklabels(ride_count_str)

# show legend on ax3
ax3.legend()

# set aspect ratio for each subplot
ax1.set_box_aspect(1/2.5)
ax2.set_box_aspect(1/2.5)
ax3.set_box_aspect(1/2.5)
ax4.set_box_aspect(1/2.5)
ax5.set_box_aspect(1/2.5)
ax6.set_box_aspect(1/2.5)

# set spacing between subplots
hdiff = 0.01   # horizontal spacing
vdiff = 0.03   # vertical spacing

ax1_pos = ax1.get_position()   # get position handle of ax1 and ax4
ax4_pos = ax4.get_position()

# adjust position of every subplot according to ax4 and ax1 positions
ax1.set_position([ax1_pos.x0, ax4_pos.y0 + ax4_pos.height + vdiff, ax1_pos.width, ax1_pos.height])
ax2.set_position([ax1_pos.x0 + ax1_pos.width + hdiff, ax4_pos.y0 + ax4_pos.height + vdiff, ax1_pos.width, ax1_pos.height])
ax3.set_position([ax1_pos.x0 + 2*(ax1_pos.width + hdiff), ax4_pos.y0 + ax4_pos.height + vdiff, ax1_pos.width, ax1_pos.height])

ax5.set_position([ax4_pos.x0 + ax4_pos.width + hdiff, ax4_pos.y0, ax4_pos.width, ax4_pos.height])
ax6.set_position([ax4_pos.x0 + 2*(ax4_pos.width + hdiff), ax4_pos.y0, ax4_pos.width, ax4_pos.height])

# display figure
fig1.show()

#--------------------------------------
# make horizontal bar chart

# note:
# static_casual(OR member)_station_filtered_sorted contains ride count percentage (sorted in descending order) of
# casual (OR member) riders for every station with a ride count >= mean ride counts of both casual and member riders.

# obtain the first 20 entries from sorted df
stat_casual_station_req = stat_casual_station_filtered_sorted.head(20)   # top 20 stations among casual riders
stat_member_station_req = stat_member_station_filtered_sorted.head(20)   # top 20 stations among member riders

# initialize figure and subplot handle
fig2, (ax21, ax22) = plt.subplots(1, 2)
fig2.tight_layout()

# set figure window size
fig2.set_figwidth(12)
fig2.set_figheight(6)

# obtain start station name, ride count percentage of casual and member riders from the sorted casual rider df
# '_casual' and '_casual_member' denotes var obtained from the casual riders df
station_name_casual = stat_casual_station_req['start_station_name']
ride_perct_casual = stat_casual_station_req['ride_count_perct_casual']
ride_perct_casual_member = stat_casual_station_req['ride_count_perct_member']

# make horizontal stacked bar chart, invert y-axis
b1_casual = ax21.barh(station_name_casual, ride_perct_casual, color = 'royalblue')
b2_casual = ax21.barh(station_name_casual, ride_perct_casual_member, left = ride_perct_casual, color = 'orangered')
ax21.legend([b1_casual, b2_casual], ['casual', 'member'])
ax21.invert_yaxis()

# obtain start station name, ride count percentage of casual and member riders from the sorted member rider df
# '_member' and '_member_casual' denotes var obtained from the member riders df
station_name_member = stat_member_station_req['start_station_name']
ride_perct_member = stat_member_station_req['ride_count_perct_member']
ride_perct_member_casual = stat_member_station_req['ride_count_perct_casual']

# make horizontal stacked bar chart, invert y-axis
b1_member = ax22.barh(station_name_member, ride_perct_member_casual, color = 'royalblue')
b2_member = ax22.barh(station_name_member, ride_perct_member, left = ride_perct_member_casual, color = 'orangered')
ax22.legend([b1_member, b2_member], ['casual', 'member'])
ax22.invert_yaxis()

# set x-label for each subplot
ax21.set_xlabel('Ride count percentage ($\%$)')
ax22.set_xlabel('Ride count percentage ($\%$)')

# set x-ticks and x-tick labels for each subplot
ax21.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax21.set_xticklabels([0, 20, 40, 60, 80, 100])

ax22.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
ax22.set_xticklabels([0, 20, 40, 60, 80, 100])

# set aspect ratio for subplot boxes
ax21.set_box_aspect(2.5)
ax22.set_box_aspect(2.5)

# set spacing between subplots
hdiff_2 = 0.2   # horizontal spacing

# adjust position of subplots to remove spacing between them
ax21_pos = ax21.get_position()   # get position handle of ax21

# adjust position of subplot on the right according to ax21 positions
ax22.set_position([ax21_pos.x0 + ax21_pos.width + hdiff_2, ax21_pos.y0, ax21_pos.width, ax21_pos.height])

# display figure
fig2.show()

#--------------------------------------
# specify output directory
fig_output_dir = 'C:\\Users\\siumichael.tang\\Downloads\\bike_share\\plots_py'
fig_filename_stat_ts_eps = 'stat_time_series' + '.eps'   # filename of stat_ts (fig 1) in eps format
fig_filename_stat_ts_png = 'stat_time_series' + '.png'   # filename of stat_ts (fig 1) in png format

fig_filename_stat_perct_barh_eps = 'stat_perct_barh' + '.eps'   # filename of stat_perct_barh (fig 2) in eps format
fig_filename_stat_perct_barh_png = 'stat_perct_barh' + '.png'   # filename of stat_perct_barh (fig 2) in png format

# assemble full path of figures
fig_output_path_stat_ts_eps = os.path.join(fig_output_dir, fig_filename_stat_ts_eps)
fig_output_path_stat_ts_png = os.path.join(fig_output_dir, fig_filename_stat_ts_png)

fig_output_path_stat_perct_barh_eps = os.path.join(fig_output_dir, fig_filename_stat_perct_barh_eps)
fig_output_path_stat_perct_barh_png = os.path.join(fig_output_dir, fig_filename_stat_perct_barh_png)

# save figures to each format listed above
fig1.savefig(fig_output_path_stat_ts_eps, format = 'eps', bbox_inches='tight')
fig1.savefig(fig_output_path_stat_ts_png, format = 'png', bbox_inches='tight')

fig2.savefig(fig_output_path_stat_perct_barh_eps, format = 'eps', bbox_inches='tight')
fig2.savefig(fig_output_path_stat_perct_barh_png, format = 'png', bbox_inches='tight')


# get ride percentage (OR number of ride count) for each station by member type,
# note df obtained includes stations with ride count >= mean ride count of each rider type

# put it in a table for dashboard
# get percentage of ride count for each stattion by member type, put it in horizontal bar chart