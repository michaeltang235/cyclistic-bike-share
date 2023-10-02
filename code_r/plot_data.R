# load packages
#library(tidyr)
library(dplyr)
#library(lubridate)
#library(tidyverse)
library(ggplot2)
library(cowplot)

# specify path where input data are
direct_req <- '/cloud/project/bike_share/data_r/'
#direct_req <- '/home/siumichael.tang/bike_share/data_r/'

# enter format of stats dataframes to be read
filename_stat_user_month <- 'stat_user_month.csv'
filename_stat_user_day_of_week <- 'stat_user_day_of_week.csv'
filename_stat_user_hour_of_day <- 'stat_user_hour_of_day.csv'

filename_stat_casual_station_filtered_sorted <- 'stat_casual_station_filtered_sorted.csv'
filename_stat_member_station_filtered_sorted <- 'stat_member_station_filtered_sorted.csv'

# read .csv files into dataframes
stat_user_month <- read.csv((paste(direct_req, filename_stat_user_month, sep = '')))
stat_user_day_of_week <- read.csv((paste(direct_req, filename_stat_user_day_of_week, sep = '')))
stat_user_hour_of_day <- read.csv((paste(direct_req, filename_stat_user_hour_of_day, sep = '')))

stat_casual_station_filtered_sorted <- read.csv((paste(direct_req,
                                                       filename_stat_casual_station_filtered_sorted, 
                                                       sep = '')))
stat_member_station_filtered_sorted <- read.csv((paste(direct_req,
                                                       filename_stat_member_station_filtered_sorted, 
                                                       sep = '')))

# obtain subset of every dataframe, filtered by membership type
stat_user_month_casual <- subset(stat_user_month, member_casual == 'casual')
stat_user_month_member <- subset(stat_user_month, member_casual == 'member')

stat_user_day_of_week_casual <- subset(stat_user_day_of_week, member_casual == 'casual')
stat_user_day_of_week_member <- subset(stat_user_day_of_week, member_casual == 'member')

stat_user_hour_of_day_casual <- subset(stat_user_hour_of_day, member_casual == 'casual')
stat_user_hour_of_day_member <- subset(stat_user_hour_of_day, member_casual == 'member')

#--------------------------------------
# make subplots (time series, line plots)

# create x data vector for every plot
x_data_month <- c(1:12)
x_data_day_of_week <- c(1:7)
x_data_hour_of_day <- c(1:24)
x_hour_of_day_tick <- seq(from = 0, to = 22, by = 2)

# make subplot (p11), mean ride length vs month
p11 <- ggplot() + 
  geom_line(data = stat_user_month_casual, 
            mapping = aes(x = x_data_month, y = mean_ride_length/60), 
            color = 'blue') +
  geom_line(data = stat_user_month_member, 
            mapping = aes(x = x_data_month, y = mean_ride_length/60), 
            color = 'red')

# make subplot (p12), mean ride length vs day of week
p12 <- ggplot() + 
  geom_line(data = stat_user_day_of_week_casual, 
            mapping = aes(x = x_data_day_of_week, y = mean_ride_length/60), 
            color = 'blue') +
  geom_line(data = stat_user_day_of_week_member, 
            mapping = aes(x = x_data_day_of_week, y = mean_ride_length/60), 
            color = 'red') 

# make subplot (p13), mean ride length vs hour of day
# for p13, map 'color' aesthetic to string (i.e. 'casual' and 'member'), 
# then specify 'breaks' and 'values' in scale_color_manual()
p13 <- ggplot() + 
  geom_line(data = stat_user_hour_of_day_casual, 
            mapping = aes(x = x_data_hour_of_day, 
                          y = mean_ride_length/60, 
                          color = 'casual')) +
  geom_line(data = stat_user_hour_of_day_member, 
            mapping = aes(x = x_data_hour_of_day, 
                          y = mean_ride_length/60, 
                          color = 'member')) + 
  scale_color_manual(name = NULL,
                     breaks = c('casual', 'member'), 
                     values = c('blue', 'red'))

# make subplot (p21), ride count vs month
p21 <- ggplot() + 
  geom_line(data = stat_user_month_casual, 
            mapping = aes(x = x_data_month, y = ride_count), 
            color = 'blue') +
  geom_line(data = stat_user_month_member, 
            mapping = aes(x = x_data_month, y = ride_count), 
            color = 'red')

# make subplot (p22), ride count vs day of week
p22 <- ggplot() + 
  geom_line(data = stat_user_day_of_week_casual, 
            mapping = aes(x = x_data_day_of_week, y = ride_count), 
            color = 'blue') + 
  geom_line(data = stat_user_day_of_week_member, 
            mapping = aes(x = x_data_day_of_week, y = ride_count), 
            color = 'red') 

# make subplot (p23), ride count vs hour of day
p23 <- ggplot() + 
  geom_line(data = stat_user_hour_of_day_casual, 
            mapping = aes(x = x_data_hour_of_day, y = ride_count), 
            color = 'blue') +
  geom_line(data = stat_user_hour_of_day_member, 
            mapping = aes(x = x_data_hour_of_day, y = ride_count), 
            color = 'red') 

# update axes labels and limits

# create string for x-axis tick labels for each subplot
month_str <- c('May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr')
day_of_week_str <- c('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
hour_of_day_str <- c('00', '02', '04', '06', '08', '10', '12', '14', '16', '18', '20', '22')

# get max mean ride length and ride count
max_mean_ride_length <- max(c(stat_user_month$mean_ride_length, 
                              stat_user_day_of_week$mean_ride_length, 
                              stat_user_hour_of_day$mean_ride_length))

max_ride_count <- max(c(stat_user_month$ride_count, 
                        stat_user_day_of_week$ride_count, 
                        stat_user_hour_of_day$ride_count))

# get max y-tick for mean ride length and ride count, round to the
# nearest 10
max_y_tick_mean_ride_length <- ceiling(max_mean_ride_length/60/10)*10
max_y_tick_ride_count <- ceiling(max_ride_count/100000)*100000

# for every subplot, set names, tick positions, tick labels,
# limits of y- and x-axes,  aspect ratio, panel color, 
# and spacing between them
# for p13, set properties of legend

p11 <-  p11 + 
  scale_y_continuous(name = 'Mean ride length [min]',
                     limits = c(10, max_y_tick_mean_ride_length)) +
  scale_x_continuous(name = NULL, 
                     breaks = x_data_month,
                     labels = NULL) +
  theme(aspect.ratio = 1/2.5, 
        panel.background = element_rect(fill = 'white', color = 'black'), 
        plot.margin = unit(c(0, 0, 0, 0), 'pt'))

p12 <-  p12 + 
  scale_y_continuous(name = NULL,
                     labels = NULL,
                     limits = c(10, max_y_tick_mean_ride_length)) +
  scale_x_continuous(name = NULL, 
                     labels = NULL,
                     breaks = x_data_day_of_week) + 
  theme(aspect.ratio = 1/2.5, 
        panel.background = element_rect(fill = 'white', color = 'black'), 
        plot.margin = unit(c(0, 0, 0, 0), 'pt'))

p13 <-  p13 + 
  scale_y_continuous(name = NULL,
                     labels = NULL,
                     limits = c(10, max_y_tick_mean_ride_length)) +
  scale_x_continuous(name = NULL, 
                     labels = NULL,
                     breaks = x_hour_of_day_tick) + 
  theme(aspect.ratio = 1/2.5, 
        panel.background = element_rect(fill = 'white', color = 'black'), 
        legend.background = element_rect(color = 'black'),
        legend.key = element_rect(fill = 'white'),
        legend.position = c(0.86, 0.75),
        legend.spacing.y = unit(-5, 'pt'),
        plot.margin = unit(c(0, 0, 0, 0), 'pt'))

# assemble string of y-ticks for subplots of ride count vs time (p21-p23)
# each y-tick (ride count) is set as increments of 100K
ride_count_y_tick <- seq(from = 0, to = max_y_tick_ride_count, by = 100000)
ride_count_y_tick_str <- list('0')
for (i in 2:length(ride_count_y_tick)){
  ride_count_y_tick_str <- append(ride_count_y_tick_str, 
                                  sprintf('%dK', ride_count_y_tick[i]/1000))
}

p21 <- p21 + 
  scale_y_continuous(name = 'Ride count', 
                     breaks = ride_count_y_tick, 
                     labels = ride_count_y_tick_str, 
                     limits = c(0, max_y_tick_ride_count)) +
  scale_x_continuous(name = 'Months', 
                     breaks = x_data_month, labels = month_str) +
  theme(aspect.ratio = 1/2.5, 
        panel.background = element_rect(fill = 'white', color = 'black'), 
        plot.margin = unit(c(0, 0, 0, 0), 'pt'))

p22 <- p22 + 
  scale_y_continuous(name = NULL,
                     labels = NULL,
                     limits = c(0, max_y_tick_ride_count)) +
  scale_x_continuous(name = 'Day of week', 
                     breaks = x_data_day_of_week, 
                     labels = day_of_week_str) +
  theme(aspect.ratio = 1/2.5, 
        panel.background = element_rect(fill = 'white', color = 'black'), 
        plot.margin = unit(c(0, 0, 0, 0), 'pt'))

p23 <- p23 + 
  scale_y_continuous(name = NULL,
                     labels = NULL,
                     limits = c(0, max_y_tick_ride_count)) +
  scale_x_continuous(name = 'Hour of day [HH]', 
                     breaks = x_hour_of_day_tick, 
                     labels = hour_of_day_str) +
  theme(aspect.ratio = 1/2.5, 
        panel.background = element_rect(fill = 'white', color = 'black'),
        plot.margin = unit(c(0, 0, 0, 0), 'pt'))

# show subplots in one page using plot_grid() from cowplot package
p_output <- plot_grid(p11, p12, p13, p21, p22, p23, 
                      nrow = 2, ncol = 3, align = 'vh')

#--------------------------------------
# make horizontal bar chart

# note:
# static_casual(OR member)_station_filtered_sorted contains ride count 
# percentage (sorted in descending order) of
# casual (OR member) riders for every station with a ride count >= 
# mean ride counts of both casual and member riders.

# obtain the first 20 entries from sorted df
stat_casual_station_req <- head(stat_casual_station_filtered_sorted, 20)   # top 20 stations among casual riders
stat_member_station_req <- head(stat_member_station_filtered_sorted, 20)   # top 20 stations among member riders

# from each of the sorted df, obtain df for making stacked bar plot by
# vertically concatenating relevant columns such that groups of 'member' and 'casual'
# with their respective ride count perc't are formed,
# specifically, concatenate the following columns
# start_station_name, 
# membership type,
# ride count percentage w.r.t. each rider type
df_req_casual <- data.frame(station_name = c(stat_casual_station_req$'start_station_name', 
                                      stat_casual_station_req$'start_station_name'),
                     member_casual = c(stat_casual_station_req$member_casual_casual, 
                                       stat_casual_station_req$member_casual_member), 
                     ride_count_perct = c(stat_casual_station_req$'ride_count_perct_casual', 
                                          stat_casual_station_req$'ride_count_perct_member'))

df_req_member <- data.frame(station_name = c(stat_member_station_req$'start_station_name', 
                                             stat_member_station_req$'start_station_name'),
                            member_casual = c(stat_member_station_req$member_casual_casual, 
                                              stat_member_station_req$member_casual_member), 
                            ride_count_perct = c(stat_member_station_req$'ride_count_perct_casual', 
                                                 stat_member_station_req$'ride_count_perct_member'))

# convert start station name to factor variable with levels (order) assigned 
# for each df_req_casual(OR member)
x_data_station_name_casual <- factor(df_req_casual$station_name, 
                              levels = stat_casual_station_req$'start_station_name')

x_data_station_name_member <- factor(df_req_member$station_name, 
                                     levels = stat_member_station_req$'start_station_name')

# specify y-tick str
ride_count_perct_y_tick_str = c('0', '20', '40', '60', '80', '100')

# make stacked bar plot for top 20 stations for casual riders, name it p2_casual
p2_casual <- ggplot() +
  geom_col(data = df_req_casual, 
           mapping = aes(x = x_data_station_name_casual, 
                         y = ride_count_perct, 
                         fill = member_casual), 
           position = position_fill(reverse = TRUE))

# make stacked bar plot for top 20 stations for member riders, name it p2_member
p2_member <- ggplot() +
  geom_col(data = df_req_member, 
           mapping = aes(x = x_data_station_name_member, 
                         y = ride_count_perct, 
                         fill = member_casual), 
           position = position_fill(reverse = TRUE))

# specify the following for p2_casual and p2_member, 
# flip x- and y-coordinates (bars pointing horizontally),
# reverse direction of x-axis, remove x-axis title,
# specify y-axis' title, breaks, and limits,
# specify color of bars,
# set aspect ratio, panel background, plot margin, legend details
p2_casual <- p2_casual + coord_flip() + 
  scale_x_discrete(name = NULL, 
                   limits = rev)  + 
  scale_y_continuous(name = 'Ride count percentage (%)',
                     breaks = seq(0, 1, 0.2),
                     labels = ride_count_perct_y_tick_str,
                     limits =  c(0, 1)) +
  scale_fill_manual(values = c('blue', 'red')) +
  theme(aspect.ratio = 2.5, 
        panel.background = element_rect(fill = 'white', color = 'black'),
        plot.margin = unit(c(0, -10, 0, 0), 'pt'),
        legend.title = element_blank(), 
        legend.position = 'top', 
        legend.key = element_rect(color = 'transparent', 
                                  fill = 'white'),
        legend.key.size = unit(5, 'pt'),
        legend.spacing.y = unit(-5, 'pt'))

p2_member <- p2_member + coord_flip() + 
  scale_x_discrete(name = NULL, 
                   limits = rev)  + 
  scale_y_continuous(name = 'Ride count percentage (%)',
                     breaks = seq(0, 1, 0.2),
                     labels = ride_count_perct_y_tick_str,
                     limits =  c(0, 1)) +
  scale_fill_manual(values = c('blue', 'red')) +
  theme(aspect.ratio = 2.5, 
        panel.background = element_rect(fill = 'white', color = 'black'),
        plot.margin = unit(c(0, 0, 0, -10), 'pt'),
        legend.title = element_blank(), 
        legend.position = 'top', 
        legend.key = element_rect(color = 'transparent', 
                                  fill = 'white'),
        legend.key.size = unit(5, 'pt'),
        legend.spacing.y = unit(-5, 'pt'))

# show subplots in one page using plot_grid() from cowplot package,
# name combined subplots as p2_output
p2_output <- plot_grid(p2_casual, p2_member, 
                       ncol = 2, align = 'h')

#---------------------------------------------------------
# specify output directory
fig_output_dir <- '/cloud/project/bike_share/plots_r'

# save each figure to path, specify background color and dimensions

# saving time series plot
ggsave(file.path(fig_output_dir, 'stat_time_series.png'), 
       plot = p_output, 
       bg = 'white',
       width = 35,
       height = 11,
       unit = 'cm')

ggsave(file.path(fig_output_dir, 'stat_time_series.eps'), 
       plot = p_output, 
       bg = 'white',
       width = 35,
       height = 11,
       unit = 'cm')

# saving stacked horizontal bar plot
ggsave(file.path(fig_output_dir, 'stat_perct_barh.png'), 
       plot = p2_output, 
       bg = 'white',
       width = 20,
       height = 11,
       unit = 'cm')

ggsave(file.path(fig_output_dir, 'stat_perct_barh.eps'), 
       plot = p2_output, 
       bg = 'white',
       width = 20,
       height = 11,
       unit = 'cm')
