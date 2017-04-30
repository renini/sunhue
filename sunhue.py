#!/usr/bin/python
#
# Rene Arends / Turn Philips Hue Lights on/off sunset/sunrise
#
# pip install ephem
# pip install datetime
# pip install phue
#
import ephem
#from datetime import date, time, datetime
import datetime
#from datetime import datetime, timedelta
#from time import localtime, strftime
import logging
from phue import Bridge

# create logger with 'sunwait'
logger = logging.getLogger('sunwait')
#fh = logging.FileHandler('sunwait.log')
fh = logging.FileHandler('/tmp/sunhue.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.INFO)
logger.info("Initialise")

# home configuration
home=ephem.Observer()
home.pressure = 1010 # millibar
home.temp = 25 # deg. Celcius
home.horizon = 0
home.lat='51.900'
home.lon='4.553'
home.elevation = 3 # meters
#now = datetime.datetime.now() #get current time
#home.date = now
home.date = ephem.date(datetime.datetime.utcnow())
#fix the timezone stuff
#print (now)
#print (datetime.datetime.utcnow())

sun = ephem.Sun()

sun.compute(home)
sunrise, sunset = (home.next_rising(sun),
                   home.next_setting(sun))

#logger.info('Previous runrise will be: %s' % ephem.localtime(home.previous_rising(sun)))
#logger.info('Previous sunset will be: %s' % ephem.localtime(home.previous_setting(sun)))
#logger.info('Next runrise will be: %s' % ephem.localtime(home.next_rising(sun)))
#logger.info('Next sunset will be: %s' % ephem.localtime(home.next_setting(sun)))

logger.info('Next runrise will be: %s' % ephem.localtime(sunrise))
logger.info('Next sunset will be: %s' % ephem.localtime(sunset))

# init philips hue
b = Bridge('192.168.1.10')
lights_list = b.get_light_objects('list')

# check if its day or night
# if it is daytime, we will see a sunset sooner than a sunrise.
if sunset < sunrise:
 logger.info('Its day, make sure that the lights are off')
 for light in lights_list:
   if light.on == True:
     logger.info('Light %s is on, turning off' % light.name)
     light.on = False
else:
 logger.info('Its night, make sure that the lights are on')
 for light in lights_list:
   if light.on == False:
     logger.info('Light %s is off, turning on' % light.name)
     light.on = True
