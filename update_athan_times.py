#!/usr/bin/env python

import datetime
from praytimes import PrayTimes
from crontab import CronTab

PATH_TO_PLAY_SCRIPT = '/home/pi/rpi_athan/play_athan.py'

LATITUDE   =  41.9668
LONGITUDE  = -71.1870
GMT_OFFSET = -5

def get_prayer_times():

  now = datetime.datetime.now()
  today = (now.year,now.month,now.day)

  PT = PrayTimes('ISNA')
  times = PT.getTimes(today, (LATITUDE, LONGITUDE), GMT_OFFSET , 1)

  # Only interested in prayer times but getTimes() returns other times too
  times.pop('sunrise')
  times.pop('imsak')
  times.pop('sunset')
  times.pop('midnight')

  return times


def add_athan_cron_job(cron, time):

  shell_command = 'python {} > /dev/null 2>&1'.format(PATH_TO_PLAY_SCRIPT)

	job = cron.new(command = shell_command)
	
	split_time = time.split(':')

	hour = split_time[0]
	mins = split_time[1]

	job.minute.on( int(mins) )
	job.hour.on(   int(hour) )

	print "Added job: {}".format(job)


def main():

  cron = CronTab(user = 'pi')

  print "Removing old jobs..."
  cron.remove_all(command = shell_command)
  
  prayer_times = get_prayer_times()

  for prayer in prayer_times:
    add_athan_cron_job(cron, prayer_times[prayer])

  cron.write()

main()



