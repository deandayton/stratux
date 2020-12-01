#!/usr/bin/python2.7
# Copyright (c) 2016, Swift Navigation, All Rights Reserved.
# Released under MIT License.
#
# Find documentation of parameters here:
# http://aprs.gids.nl/nmea/#gga
#
# time_t is a `time_struct` (https://docs.python.org/2/library/time.html)
# alt_m, geoidal_sep_m are in meters

# output from Avare
# $GPBOD,083.0,T,090.0,M,gDST,gSRC*44
# $GPRMC,162632,A,4013.611,N,08317.078,W,000.0,000.0,301120,007.1,W*71
# $GPGGA,162632,4013.611,N,08317.078,W,1,11,0.0,259.3,M,0.0,M,,*6D
# $GPRMB,A,0.24,L,gSRC,gDST,4014.730,N,08307.710,W,007.2,081.1,000.0,V*21

import time
from datetime import datetime



def gen_gga(t, alt_m):
  
  str = 'GPGGA,%s,4013.611,N,08317.078,W,1,11,1.6,%s,M,0.0,M,,' % (t, alt_m)
  cksum = 0
  for c in str:
    cksum = cksum ^ ord(c)
  cksum = cksum & 0xFF
  
  return '$%s*%0.2X' % (str, cksum)

def gen_rmc(t, trk, gs, mv, mvEw):
  
  str = 'GPRMC,%s,A,4013.611,N,08317.078,W,%s,%s,301120,%s,%s' % (t, gs, trk, mv, mvEw)
  cksum = 0
  for c in str:
    cksum = cksum ^ ord(c)
  cksum = cksum & 0xFF
  
  return '$%s*%0.2X' % (str, cksum)

def gen_rmb(xtrk, xtrkLR, dest, bearing, dist):
  
  str = 'GPRMB,A,%s,%s,gSRC,%s,4014.730,N,08307.710,W,%s,%s,000.0,V' % (xtrk, xtrkLR, dest, dist, bearing)
  cksum = 0
  for c in str:
    cksum = cksum ^ ord(c)
  cksum = cksum & 0xFF
  
  return '$%s*%0.2X' % (str, cksum)


# from http://www.gpsinformation.org/dale/nmea.htm
# $GPGGA,183730,3907.356,N,12102.482,W,1,05,1.6,646.4,M,-24.1,M,,*75

alt = '2000.0'
tcog = '180.0'
sog = '200.0'
mv = '007.1'
mvEW = 'W'
wpt = 'test'
xtrk = '2.1'
xtrkLR = 'L'
range2wpt = '040.0'
tbearing2wpt = '270.0'

for x in range(60):
	now = datetime.now().time() # time object
	#now = datetime.datetime.now()  
	hhmmssss = '%02d%02d%02d.%02d' % (now.hour, now.minute, now.second, now.microsecond/10000)


	gga =  gen_gga(hhmmssss, alt)

	rmc = gen_rmc(hhmmssss, tcog, sog, mv,mvEW)

	rmb = gen_rmb(xtrk, xtrkLR, wpt, range2wpt, tbearing2wpt)

	print gga
	print rmc
	print rmb

	time.sleep(1)
