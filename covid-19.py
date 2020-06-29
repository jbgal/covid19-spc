## Created by Justine Galbraith, 2020-06-27

import matplotlib.pyplot as plt
from matplotlib.dates import (YEARLY, DateFormatter, rrulewrapper, RRuleLocator, drange)
import numpy as np
import datetime
import csv
import statistics
import urllib.request

state = "Pennsylvania"
#state = input("Enter your state:")
county = input("Enter your county: ")

## Important dates for Allegheny County
DateRed = datetime.datetime.strptime("2020-03-21", "%Y-%m-%d").date() 
DateCDCMask = datetime.datetime.strptime("2020-04-02","%Y-%m-%d").date()
DatePennMask = datetime.datetime.strptime("2020-04-19","%Y-%m-%d").date()
#DateYellow = datetime.datetime.strptime("2020-06-05","%Y-%m-%d").date()
#DateGreen = datetime.datetime.strptime("2020-06-26","%Y-%m-%d").date()
#Yellow phase depends on county
if county in ["Bradford", "Cameron", "Centre", "Clarion", "Clearfield", "Clinton", "Crawford", "Elk", "Erie", "Forest", "Jefferson", "Lawrence", "Lycoming", "McKean", "Mercer", "Montour", "Northumberland", "Potter", "Snyder", "Sullivan", "Tioga", "Union", "Venango", "Warren"]:
    DateYellow = datetime.datetime.strptime("2020-05-08","%Y-%m-%d").date()
elif county in ["Allegheny", "Armstrong", "Bedford", "Blair", "Butler", "Cambria", "Fayette", "Fulton", "Greene", "Indiana", "Somerset", "Washington", "Westmoreland"]:
    DateYellow = datetime.datetime.strptime("2020-05-15","%Y-%m-%d").date()
elif county in ["Adams", "Beaver", "Carbon", "Columbia", "Cumberland", "Juniata", "Mifflin", "Perry", "Susquehanna", "Wayne", "Wyoming", "York"]:
    DateYellow = datetime.datetime.strptime("2020-05-22","%Y-%m-%d").date()
elif county in ["Dauphin", "Franklin", "Huntingdon", "Lebanon", "Luzerne", "Monroe", "Pike", "Schuylkill"]:
    DateYellow = datetime.datetime.strptime("2020-05-29","%Y-%m-%d").date()
elif county in ["Berks", "Bucks", "Chester", "Delaware", "Lackawanna", "Lancaster", "Lehigh", "Montgomery", "Northampton", "Philadelphia"]:
    DateYellow = datetime.datetime.strptime("2020-06-05","%Y-%m-%d").date()
#green phase depends on county
if county in ["Bradford", "Cameron", "Centre", "Clarion", "Clearfield", "Crawford", "Elk", "Forest", "Jefferson", "Lawrence", "McKean", "Montour", "Potter", "Snyder", "Sullivan", "Tioga", "Venango", "Warren"]:
    DateGreen = datetime.datetime.strptime("2020-05-29","%Y-%m-%d").date()
elif county in ["Allegheny", "Armstrong", "Bedford", "Blair", "Butler", "Cambria", "Clinton", "Fayette", "Fulton", "Greene", "Indiana", "Lycoming", "Mercer", "Somerset", "Washington", "Westmoreland"]:
    DateGreen = datetime.datetime.strptime("2020-06-05","%Y-%m-%d").date()
elif county in ["Adams", "Beaver", "Carbon", "Columbia", "Cumberland", "Juniata", "Mifflin", "Northumberland", "Union", "Wayne", "Wyoming", "York"]:
    DateGreen = datetime.datetime.strptime("2020-06-12","%Y-%m-%d").date()
elif county in ["Dauphin", "Franklin", "Huntingdon", "Luzerne", "Monroe", "Perry", "Pike", "Schuylkill"]:
    DateGreen = datetime.datetime.strptime("2020-06-19","%Y-%m-%d").date()
elif county in ["Berks", "Bucks", "Chester", "Delaware", "Erie", "Lackawanna", "Lancaster", "Lehigh", "Montgomery", "Northampton", "Philadelphia", "Susquehanna"]:
    DateGreen = datetime.datetime.strptime("2020-06-26","%Y-%m-%d").date()
else:
    DateGreen = datetime.datetime.now()

xs = []
ysum = []

## Pull data from table (NYT Covid Dataset from github) and plot
# covid-NYT.txt header: date,county,state,fips,cases,deaths 
link = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
req = urllib.request.Request(link)
response = urllib.request.urlopen(req)
the_page = response.read().decode()
the_page2 = the_page.split('\n')
output = []
for row in the_page2:
    output.append(row.split(','))
for row in output:
    if row[2] == state:
        if row[1] == county:
            xs.append(datetime.datetime.strptime(row[0],"%Y-%m-%d").date())
            ysum.append(int(row[4]))

xmin = min(xs)
xmax = max(xs)

## Convert the y values from cumulative cases to daily cases
ys = []
ys.append(ysum[0])
for i in range(len(ysum)):
    if i > 0:
        ys.append(ysum[i]-ysum[i-1])



## Control data: 14 days after shutdown, and then leading up to the masks being required -- 16 days
DateControlStart0 = DateRed + datetime.timedelta(days=14) #datetime.datetime.strptime("2020-04-04","%Y-%m-%d").date()
DateControlEnd0 = DatePennMask #datetime.datetime.strptime("2020-04-19","%Y-%m-%d").date()
## Control data: 14 days after masks are required, and then leading up to the yellow phase -- 13 days
DateControlStart = DatePennMask +datetime.timedelta(days=14) #datetime.datetime.strptime("2020-05-03","%Y-%m-%d").date()
DateControlEnd = DateYellow #datetime.datetime.strptime("2020-05-15","%Y-%m-%d").date()



xc0 = []
yc0 = []

for i in range(len(xs)):
    if DateControlStart0 <= xs[i] <= DateControlEnd0:
        xc0.append(xs[i])
        yc0.append(ys[i])

yavg0 = statistics.mean(yc0)
ystdev0 = statistics.stdev(yc0)
yp30 = yavg0+3*ystdev0
yp20 = yavg0+2*ystdev0
yp10 = yavg0+1*ystdev0 
ym10 = yavg0-1*ystdev0 
ym20 = yavg0-2*ystdev0 
ym30 = yavg0-3*ystdev0 

xc = []
yc = []

for i in range(len(xs)):
    if DateControlStart <= xs[i] <= DateControlEnd:
        xc.append(xs[i])
        yc.append(ys[i])

yavg = statistics.mean(yc)
ystdev = statistics.stdev(yc)
yp3 = yavg+3*ystdev
yp2 = yavg+2*ystdev 
yp1 = yavg+1*ystdev 
ym1 = yavg-1*ystdev 
ym2 = yavg-2*ystdev 
ym3 = yavg-3*ystdev 




## Calculating the statistically significant "out-of-control" data points

## OOC1: Above/below 3 sigma
## Note: This matters what the avg/stdev are. You need separate ones for each zone. 
OOC1x = [] 
OOC1y = []
OOC1x0 = [] 
OOC1y0 = []
for i in range(len(xs)):
    if ys[i] >= yp3:
        if xs[i] >= DateControlStart: 
            OOC1x.append(xs[i])
            OOC1y.append(ys[i])
    elif ys[i] <= ym3:
        if xs[i] >= DateControlStart: 
            OOC1x.append(xs[i])
            OOC1y.append(ys[i])
    if ys[i] >= yp30:
        if xs[i] >= DateControlStart0: 
            OOC1x0.append(xs[i])
            OOC1y0.append(ys[i])
    elif ys[i] <= ym30:
        if xs[i] >= DateControlStart0: 
            OOC1x0.append(xs[i])
            OOC1y0.append(ys[i])

#Make a list that says whether the point (i+1) is increasing ("P"), decreasing ("M"), or the same ("Z") as the point i
OOCPMZ = []
for i in range(len(ys)-1):
    if ys[i+1] > ys[i]:
        OOCPMZ.append("P")
    elif ys[i+1] < ys[i]:
        OOCPMZ.append("M")
    else:
        OOCPMZ.append("Z")

## OOC2: Seven consecutive points increasing or decreasing
## Note: This doesn't matter what the avg/stdev are. It'll be the same for all zones. 
OOC2x = []
OOC2y = []
OOC2x0 = []
OOC2y0 = []
jj = 6
for i in range(len(ys)-jj):
    OOC2h = []
    for j in range(jj):
        OOC2h.append(OOCPMZ[i+j])
    if(all(k == "M" for k in OOC2h)) == True:
        for j in range(jj+1):
            if xs[i] >= DateControlStart: 
                OOC2x.append(xs[i+j])
                OOC2y.append(ys[i+j])
            if xs[i] >= DateControlStart0: 
                OOC2x0.append(xs[i+j])
                OOC2y0.append(ys[i+j])
    elif(all(k == "P" for k in OOC2h)):
        for j in range(jj+1):
            if xs[i] >= DateControlStart: 
                OOC2x.append(xs[i+j])
                OOC2y.append(ys[i+j])
            if xs[i] >= DateControlStart0: 
                OOC2x0.append(xs[i+j])
                OOC2y0.append(ys[i+j])



## OOC3: Eight consecutive points on one side of the average
## Note: This will depend on the average
OOC3x = []
OOC3y = []
OOC3h = []
OOC3x0 = []
OOC3y0 = []
OOC3h0 = []
for i in range(len(ys)):
    if ys[i] > yavg:
        OOC3h.append("P")
    elif ys[i] < yavg:
        OOC3h.append("M")
    else:
        OOC3h.append("Z")
    if ys[i] > yavg0:
        OOC3h0.append("P")
    elif ys[i] < yavg0:
        OOC3h0.append("M")
    else:
        OOC3h0.append("Z")
jj = 8
for i in range(len(ys)-jj+1):
    OOC3h2 = []
    OOC3h20 = []
    for j in range(jj):
        OOC3h2.append(OOC3h[i+j])
        OOC3h20.append(OOC3h0[i+j])
    if(all(k == "M" for k in OOC3h2)) == True:
        for j in range(jj):
            if xs[i] >= DateControlStart: 
                OOC3x.append(xs[i+j])
                OOC3y.append(ys[i+j])
    elif(all(k == "P" for k in OOC3h2)):
        for j in range(jj):
            if xs[i] >= DateControlStart: 
                OOC3x.append(xs[i+j])
                OOC3y.append(ys[i+j])
    if(all(k == "M" for k in OOC3h20)) == True:
        for j in range(jj):
            if xs[i] >= DateControlStart0: 
                OOC3x0.append(xs[i+j])
                OOC3y0.append(ys[i+j])
    elif(all(k == "P" for k in OOC3h20)):
        for j in range(jj):
            if xs[i] >= DateControlStart0: 
                OOC3x0.append(xs[i+j])
                OOC3y0.append(ys[i+j])



## OOC4: 14 consecuting poitns in a up/down pattern
## Note: This will not depend on the avg/stdev
OOC4x = []
OOC4y = []
OOC4x0 = []
OOC4y0 = []
jj = 13
for i in range(len(ys)-jj):
    OOC4h = ""
    for j in range(jj):
        OOC4h += OOCPMZ[i+j]
    if OOC4h == "PMPMPMPMPMPMP":
        for j in range(jj+1):
            if xs[i] >= DateControlStart: 
                OOC4x.append(xs[i+j])
                OOC4y.append(ys[i+j])
            if xs[i] >= DateControlStart0: 
                OOC4x0.append(xs[i+j])
                OOC4y0.append(ys[i+j])
    elif OOC4h == "MPMPMPMPMPMPM":
        for j in range(jj+1):
            if xs[i] >= DateControlStart: 
                OOC4x.append(xs[i+j])
                OOC4y.append(ys[i+j])
            if xs[i] >= DateControlStart0: 
                OOC4x0.append(xs[i+j])
                OOC4y0.append(ys[i+j])


##Zone List
##Note that this will depend on the 
OOCZones = []
OOCZones0 = []
for i in range(len(ys)):
    if ys[i] >= yp2:
        OOCZones.append("Ap")
    elif ys[i] >= yp1:
        OOCZones.append("Bp")
    elif ys[i] >= ym1:
        OOCZones.append("C")
    elif ys[i] >= ym2:
        OOCZones.append("Bm")
    else:
        OOCZones.append("Am")
    if ys[i] >= yp20:
        OOCZones0.append("Ap")
    elif ys[i] >= yp10:
        OOCZones0.append("Bp")
    elif ys[i] >= ym10:
        OOCZones0.append("C")
    elif ys[i] >= ym20:
        OOCZones0.append("Bm")
    else:
        OOCZones0.append("Am")
#print(OOCZones)


##OOC 5: two out of three in Zone A (3sigma)
OOC5x = []
OOC5y = []
OOC5x0 = []
OOC5y0 = []
jj = 2 
for i in range(len(ys)-jj):
    OOC5p = 0
    OOC5m = 0
    OOC5p0 = 0
    OOC5m0 = 0
    for j in range(jj+1):
        if OOCZones[i+j] == "Ap":
            OOC5p = OOC5p + 1
        elif OOCZones[i+j] == "Am":
            OOC5m = OOC5m + 1
        if OOCZones0[i+j] == "Ap":
            OOC5p0 = OOC5p0 + 1
        elif OOCZones0[i+j] == "Am":
            OOC5m0 = OOC5m0 + 1
    if OOC5p >= 2:
        for j in range(jj+1):
            if xs[i] >= DateControlStart: 
                OOC5x.append(xs[i+j])
                OOC5y.append(ys[i+j])
    elif OOC5m >= 2:
        for j in range(jj+1):
            if xs[i] >= DateControlStart: 
                OOC5x.append(xs[i+j])
                OOC5y.append(ys[i+j])
    if OOC5p0>= 2:
        for j in range(jj+1):
            if xs[i] >= DateControlStart0: 
                OOC5x0.append(xs[i+j])
                OOC5y0.append(ys[i+j])
    elif OOC5m0 >= 2:
        for j in range(jj+1):
            if xs[i] >= DateControlStart0: 
                OOC5x0.append(xs[i+j])
                OOC5y0.append(ys[i+j])


##OOC 6: four out of five in Zone B or beyond (2sigma)
## Note: This will depend on the avg/stdev
OOC6x = []
OOC6y = []
OOC6x0 = []
OOC6y0 = []
jj = 4
for i in range(len(ys)-jj):
    OOC6p = 0
    OOC6m = 0
    OOC6p0 = 0
    OOC6m0 = 0
    for j in range(jj+1):
        if OOCZones[i+j] == "Ap":
            OOC6p = OOC6p + 1
        elif OOCZones[i+j] == "Bp":
            OOC6p = OOC6p + 1
        elif OOCZones[i+j] == "Am":
            OOC6m = OOC6m + 1
        elif OOCZones[i+j] == "Bm":
            OOC6m = OOC6m + 1
        if OOCZones0[i+j] == "Ap":
            OOC6p0 = OOC6p0 + 1
        elif OOCZones0[i+j] == "Bp":
            OOC6p0 = OOC6p0 + 1
        elif OOCZones0[i+j] == "Am":
            OOC6m0 = OOC6m0 + 1
        elif OOCZones0[i+j] == "Bm":
            OOC6m0 = OOC6m0 + 1
    if OOC6p >= 4:
        for j in range(jj+1):
            if xs[i] >= DateControlStart: 
                OOC6x.append(xs[i+j])
                OOC6y.append(ys[i+j])
    elif OOC6m >= 4:
        for j in range(jj+1):
            if xs[i] >= DateControlStart: 
                OOC6x.append(xs[i+j])
                OOC6y.append(ys[i+j])
    if OOC6p0 >= 4:
        for j in range(jj+1):
            if xs[i] >= DateControlStart0: 
                OOC6x0.append(xs[i+j])
                OOC6y0.append(ys[i+j])
    elif OOC6m0 >= 4:
        for j in range(jj+1):
            if xs[i] >= DateControlStart0: 
                OOC6x0.append(xs[i+j])
                OOC6y0.append(ys[i+j])



##OOC 7: 15 consecutive points in Zone C (1sigma)
OOC7x = []
OOC7y = []
OOC7x0 = []
OOC7y0 = []
jj = 14
for i in range(len(ys)-jj):
    OOC7h = 0
    OOC7h0 = 0
    for j in range(jj+1):
        if OOCZones[i+j] == "C":
            OOC7h = OOC7h + 1
    for j in range(jj+1):
        if OOCZones0[i+j] == "C":
            OOC7h0 = OOC7h0 + 1
    if OOC7h >= 15:
        for j in range(jj+1):
            if xs[i] >= DateControlStart: 
                OOC7x.append(xs[i+j])
                OOC7y.append(ys[i+j])
    if OOC7h0 >= 15:
        for j in range(jj+1):
            if xs[i] >= DateControlStart0: 
                OOC7x0.append(xs[i+j])
                OOC7y0.append(ys[i+j])



#
#
### Plot #1 - Just the raw data
#fig = plt.figure()
#ax = plt.subplot(111)
#plt.plot(xs, ys, 'bo-', label='Daily Confirmed Cases') 
#plt.title('Raw data: # cases drawn from NYT Covid Tracker on GitHub')
##shrink axis by 20%
#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.8])
#plt.legend(bbox_to_anchor=(1.05, 1))#ncol=2)
#plt.xlabel('Date')
##plt.xticks(rotation=30)
#plt.ylabel('# of Confirmed COVID Cases Daily in '+str(county) +' County')
#mng = plt.get_current_fig_manager()
#mng.full_screen_toggle()
#plt.show()
#
#
#
### Plot #2 - Raw data plus important dates
#fig = plt.figure()
#ax = plt.subplot(111)
#plt.plot(xs, ys, 'bo-', label='Daily Confirmed Cases') 
#plt.axvline(DateRed, color='r', label='Pennsylvania Shutdown')
#plt.axvline(DateCDCMask, color='c', label='CDC Recommends Masks')
#plt.axvline(DatePennMask, color='m', label='State Requires Masks')
#plt.axvline(DateYellow, color='y', label = 'Yellow Phase')
#plt.axvline(DateGreen, color='g', label = 'Green Phase')
#plt.title('Raw data: # cases drawn from NYT Covid Tracker on GitHub \n Vertical Lines: Important dates in Pennsylvania')
##shrink axis by 20%
#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.8])
#plt.legend(bbox_to_anchor=(1.05, 1))#ncol=2)
#plt.xlabel('Date')
##plt.xticks(rotation=30)
#plt.ylabel('# of Confirmed COVID Cases Daily in '+str(county) +' County')
#mng = plt.get_current_fig_manager()
#mng.full_screen_toggle()
#plt.show()
#
#
#
### Plot #3 - Raw data plus important dates plus control data identified
#fig = plt.figure()
#ax = plt.subplot(111)
#plt.plot(xs, ys, 'bo-', label='Daily Confirmed Cases') 
#plt.axvline(DateRed, color='r', label='Pennsylvania Shutdown')
#plt.axvline(DateCDCMask, color='c', label='CDC Recommends Masks')
#plt.axvline(DatePennMask, color='m', label='State Requires Masks')
#plt.axvline(DateYellow, color='y', label = 'Yellow Phase')
#plt.axvline(DateGreen, color='g', label = 'Green Phase')
#plt.plot(xc0 , yc0, 'yo', label='Control Data (Red Pre-Mask)')
#plt.title('Raw data: # cases drawn from NYT Covid Tracker on GitHub \n Vertical lines: Important dates in Pennsylvania \n Control data: from 14 days after Pennsylvania Shutdown to the date that the State Requires Masks')
##shrink axis by 20%
#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.8])
#plt.legend(bbox_to_anchor=(1.05, 1))#ncol=2)
#plt.xlabel('Date')
##plt.xticks(rotation=30)
#plt.ylabel('# of Confirmed COVID Cases Daily in '+str(county) +' County')
#mng = plt.get_current_fig_manager()
#mng.full_screen_toggle()
#plt.show()
#
#
#
### Plot #4 - Raw data plus important dates plus control data identified plus statistical lines
#fig = plt.figure()
#ax = plt.subplot(111)
#plt.plot(xs, ys, 'bo-', label='Daily Confirmed Cases') 
#plt.axvline(DateRed, color='r', label='Pennsylvania Shutdown')
#plt.axvline(DateCDCMask, color='c', label='CDC Recommends Masks')
#plt.axvline(DatePennMask, color='m', label='State Requires Masks')
#plt.axvline(DateYellow, color='y', label = 'Yellow Phase')
#plt.axvline(DateGreen, color='g', label = 'Green Phase')
#plt.plot(xc0 , yc0, 'yo', label='Control Data (Red Pre-Mask)')
#plt.plot((xmin, xmax), (yp30,yp30), color='lightgray', linestyle=':')
#plt.text(xmin, yp30, '+3$\sigma$')
#plt.text(xmin, (yp30+yp20)/2, 'Zone A')
#plt.plot((xmin, xmax), (yp20,yp20), color='silver', linestyle='-.')
#plt.text(xmin, yp20, '+2$\sigma$')
#plt.text(xmin, (yp20+yp10)/2, 'Zone B')
#plt.plot((xmin, xmax), (yp10, yp10), color='darkgray', linestyle='--')
#plt.text(xmin, yp10, '+1$\sigma$')
#plt.text(xmin, (yp10+yavg0)/2, 'Zone C')
#plt.plot((xmin, xmax), (yavg0,yavg0), color='gray', linestyle = '-')
#plt.text(xmin, yavg0, 'avg')
#plt.text(xmin, (ym10+yavg0)/2, 'Zone C')
#plt.plot((xmin, xmax), (ym10,ym10), color='darkgray', linestyle='--')
#plt.text(xmin, ym10, '-1$\sigma$')
#plt.text(xmin, (ym10+ym20)/2, 'Zone B')
#plt.plot((xmin,xmax), (ym20,ym20), color='silver', linestyle='-.')
#plt.text(xmin, ym20, '-2$\sigma$')
#plt.text(xmin, (ym20+ym30)/2, 'Zone A')
#plt.plot((xmin,xmax), (ym30, ym30), color='lightgray', linestyle=':')
#plt.text(xmin, ym30, '-3$\sigma$')
#plt.title('Raw data: # cases drawn from NYT Covid Tracker on GitHub \n Vertical lines: Important dates in Pennsylvania \n Control data: from 14 days after Pennsylvania Shutdown to the date that the State Requires Masks \n Hortizontal lines: Statistical Zones')
##shrink axis by 20%
#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.8])
#plt.legend(bbox_to_anchor=(1.05, 1))#ncol=2)
#plt.xlabel('Date')
##plt.xticks(rotation=30)
#plt.ylabel('# of Confirmed COVID Cases Daily in '+str(county) +' County')
#mng = plt.get_current_fig_manager()
#mng.full_screen_toggle()
#plt.show()
#
#
#
### Plot #5 - Raw data plus important dates plus control data identified plus statistical lines plus OOC 
#fig = plt.figure()
#ax = plt.subplot(111)
#plt.plot(xs, ys, 'bo-', label='Daily Confirmed Cases') 
#plt.axvline(DateRed, color='r', label='Pennsylvania Shutdown')
#plt.axvline(DateCDCMask, color='c', label='CDC Recommends Masks')
#plt.axvline(DatePennMask, color='m', label='State Requires Masks')
#plt.axvline(DateYellow, color='y', label = 'Yellow Phase')
#plt.axvline(DateGreen, color='g', label = 'Green Phase')
#plt.plot(xc0 , yc0, 'yo', label='Control Data (Red Pre-Mask)')
#plt.plot((xmin, xmax), (yp30,yp30), color='lightgray', linestyle=':')
#plt.text(xmin, yp30, '+3$\sigma$')
#plt.text(xmin, (yp30+yp20)/2, 'Zone A')
#plt.plot((xmin, xmax), (yp20,yp20), color='silver', linestyle='-.')
#plt.text(xmin, yp20, '+2$\sigma$')
#plt.text(xmin, (yp20+yp10)/2, 'Zone B')
#plt.plot((xmin, xmax), (yp10, yp10), color='darkgray', linestyle='--')
#plt.text(xmin, yp10, '+1$\sigma$')
#plt.text(xmin, (yp10+yavg0)/2, 'Zone C')
#plt.plot((xmin, xmax), (yavg0,yavg0), color='gray', linestyle = '-')
#plt.text(xmin, yavg0, 'avg')
#plt.text(xmin, (ym10+yavg0)/2, 'Zone C')
#plt.plot((xmin, xmax), (ym10,ym10), color='darkgray', linestyle='--')
#plt.text(xmin, ym10, '-1$\sigma$')
#plt.text(xmin, (ym10+ym20)/2, 'Zone B')
#plt.plot((xmin,xmax), (ym20,ym20), color='silver', linestyle='-.')
#plt.text(xmin, ym20, '-2$\sigma$')
#plt.text(xmin, (ym20+ym30)/2, 'Zone A')
#plt.plot((xmin,xmax), (ym30, ym30), color='lightgray', linestyle=':')
#plt.text(xmin, ym30, '-3$\sigma$')
#plt.plot(OOC1x0 , OOC1y0, 'rv', label='OOC1: Above/Below 3$\sigma$')
#plt.plot(OOC2x0 , OOC2y0, 'r^', label='OOC2: 7 points inc/dec')
#plt.plot(OOC3x0 , OOC3y0, 'r<', label='OOC3: 8 points on one side of avg')
#plt.plot(OOC4x0 , OOC4y0, 'r>', label='OOC4: 14 points in an up/down pattern')
#plt.plot(OOC5x0 , OOC5y0, 'rs', label='OOC5 2/3 points in Zone A')
#plt.plot(OOC6x0 , OOC6y0, 'rp', label='OOC6: 4/5 points in Zone A/B')
#plt.plot(OOC7x0 , OOC7y0, 'rD', label='OOC7: 15 points in Zone C')
#plt.title('Raw data: # cases drawn from NYT Covid Tracker on GitHub \n Vertical lines: Important dates in Pennsylvania \n Control data: from 14 days after Pennsylvania Shutdown to the date that the State Requires Masks \n Hortizontal lines: Statistical Zones \n  Red markers: Out-of-control conditions for a Statistical Process')
##shrink axis by 20%
#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.8])
#plt.legend(bbox_to_anchor=(1.05, 1))#ncol=2)
#plt.xlabel('Date')
##plt.xticks(rotation=30)
#plt.ylabel('# of Confirmed COVID Cases Daily in '+str(county) +' County')
#mng = plt.get_current_fig_manager()
#mng.full_screen_toggle()
#plt.show()
#
#
### Plot #6 - Raw data plus important dates plus control data identified plus statistical lines plus new control data
#fig = plt.figure()
#ax = plt.subplot(111)
#plt.plot(xs, ys, 'bo-', label='Daily Confirmed Cases') 
#plt.axvline(DateRed, color='r', label='Pennsylvania Shutdown')
#plt.axvline(DateCDCMask, color='c', label='CDC Recommends Masks')
#plt.axvline(DatePennMask, color='m', label='State Requires Masks')
#plt.axvline(DateYellow, color='y', label = 'Yellow Phase')
#plt.axvline(DateGreen, color='g', label = 'Green Phase')
#plt.plot(xc0 , yc0, 'yo', label='Control Data (Red Pre-Mask)')
#plt.plot((xmin, xmax), (yp30,yp30), color='lightgray', linestyle=':')
#plt.text(xmin, yp30, '+3$\sigma$')
#plt.text(xmin, (yp30+yp20)/2, 'Zone A')
#plt.plot((xmin, xmax), (yp20,yp20), color='silver', linestyle='-.')
#plt.text(xmin, yp20, '+2$\sigma$')
#plt.text(xmin, (yp20+yp10)/2, 'Zone B')
#plt.plot((xmin, xmax), (yp10, yp10), color='darkgray', linestyle='--')
#plt.text(xmin, yp10, '+1$\sigma$')
#plt.text(xmin, (yp10+yavg0)/2, 'Zone C')
#plt.plot((xmin, xmax), (yavg0,yavg0), color='gray', linestyle = '-')
#plt.text(xmin, yavg0, 'avg')
#plt.text(xmin, (ym10+yavg0)/2, 'Zone C')
#plt.plot((xmin, xmax), (ym10,ym10), color='darkgray', linestyle='--')
#plt.text(xmin, ym10, '-1$\sigma$')
#plt.text(xmin, (ym10+ym20)/2, 'Zone B')
#plt.plot((xmin,xmax), (ym20,ym20), color='silver', linestyle='-.')
#plt.text(xmin, ym20, '-2$\sigma$')
#plt.text(xmin, (ym20+ym30)/2, 'Zone A')
#plt.plot((xmin,xmax), (ym30, ym30), color='lightgray', linestyle=':')
#plt.text(xmin, ym30, '-3$\sigma$')
#plt.plot(xc, yc, 'mo', label='Control Data (Red Post-Mask)')
#plt.title('Raw data: # cases drawn from NYT Covid Tracker on GitHub \n Vertical lines: Important dates in Pennsylvania \n Control data: from 14 days after Pennsylvania Shutdown to the date that the State Requires Masks \n Hortizontal lines: Statistical Zones \n New control data: from 14 days after State Requires Masks to date of Yellow Phase')
##shrink axis by 20%
#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.8])
#plt.legend(bbox_to_anchor=(1.05, 1))#ncol=2)
#plt.xlabel('Date')
##plt.xticks(rotation=30)
#plt.ylabel('# of Confirmed COVID Cases Daily in '+str(county) +' County')
#mng = plt.get_current_fig_manager()
#mng.full_screen_toggle()
#plt.show()
#
#
#
### Plot #7 - Raw data plus important dates plus control data identified plus statistical lines plus new control data plus new statistical lines
#fig = plt.figure()
#ax = plt.subplot(111)
#plt.plot(xs, ys, 'bo-', label='Daily Confirmed Cases') 
#plt.axvline(DateRed, color='r', label='Pennsylvania Shutdown')
#plt.axvline(DateCDCMask, color='c', label='CDC Recommends Masks')
#plt.axvline(DatePennMask, color='m', label='State Requires Masks')
#plt.axvline(DateYellow, color='y', label = 'Yellow Phase')
#plt.axvline(DateGreen, color='g', label = 'Green Phase')
#plt.plot(xc0 , yc0, 'yo', label='Control Data (Red Pre-Mask)')
#plt.plot((xmin, DateControlStart), (yp30,yp30), color='lightgray', linestyle=':')
#plt.text(xmin, yp30, '+3$\sigma$')
#plt.text(xmin, (yp30+yp20)/2, 'Zone A')
#plt.plot((xmin, DateControlStart), (yp20,yp20), color='silver', linestyle='-.')
#plt.text(xmin, yp20, '+2$\sigma$')
#plt.text(xmin, (yp20+yp10)/2, 'Zone B')
#plt.plot((xmin, DateControlStart), (yp10, yp10), color='darkgray', linestyle='--')
#plt.text(xmin, yp10, '+1$\sigma$')
#plt.text(xmin, (yp10+yavg0)/2, 'Zone C')
#plt.plot((xmin, DateControlStart), (yavg0,yavg0), color='gray', linestyle = '-')
#plt.text(xmin, yavg0, 'avg')
#plt.text(xmin, (ym10+yavg0)/2, 'Zone C')
#plt.plot((xmin, DateControlStart), (ym10,ym10), color='darkgray', linestyle='--')
#plt.text(xmin, ym10, '-1$\sigma$')
#plt.text(xmin, (ym10+ym20)/2, 'Zone B')
#plt.plot((xmin, DateControlStart), (ym20,ym20), color='silver', linestyle='-.')
#plt.text(xmin, ym20, '-2$\sigma$')
#plt.text(xmin, (ym20+ym30)/2, 'Zone A')
#plt.plot((xmin, DateControlStart), (ym30, ym30), color='lightgray', linestyle=':')
#plt.text(xmin, ym30, '-3$\sigma$')
#plt.plot(xc, yc, 'mo', label='Control Data (Red Post-Mask)')
#plt.plot((DateControlStart, xmax), (yp3,yp3), color='lightgray', linestyle=':')
##plt.text(DateControlStart, yp3, '+3$\sigma$')
#plt.plot((DateControlStart, xmax), (yp2,yp2), color='silver', linestyle='-.')
##plt.text(DateControlStart, yp2, '+2$\sigma$')
#plt.plot((DateControlStart, xmax), (yp1, yp1), color='darkgray', linestyle='--')
##plt.text(DateControlStart, yp1, '+1$\sigma$')
#plt.plot((DateControlStart, xmax), (yavg,yavg), color='gray', linestyle = '-')
##plt.text(DateControlStart, yavg, 'avg')
#plt.plot((DateControlStart, xmax), (ym1,ym1), color='darkgray', linestyle='--')
##plt.text(DateControlStart, ym1, '-1$\sigma$')
#plt.plot((DateControlStart, xmax), (ym2,ym2), color='silver', linestyle='-.')
##plt.text(DateControlStart, ym2, '-2$\sigma$')
#plt.plot((DateControlStart, xmax), (ym3, ym3), color='lightgray', linestyle=':')
##plt.text(DateControlStart, ym3, '-3$\sigma$')
#plt.title('Raw data: # cases drawn from NYT Covid Tracker on GitHub \n Vertical lines: Important dates in Pennsylvania \n Control data: from 14 days after Pennsylvania Shutdown to the date that the State Requires Masks \n Hortizontal lines: Statistical Zones \n New control data: from 14 days after State Requires Masks to date of Yellow Phase')
##shrink axis by 20%
#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.8])
#plt.legend(bbox_to_anchor=(1.05, 1))#ncol=2)
#plt.xlabel('Date')
##plt.xticks(rotation=30)
#plt.ylabel('# of Confirmed COVID Cases Daily in '+str(county) +' County')
#mng = plt.get_current_fig_manager()
#mng.full_screen_toggle()
#plt.show()
#


## Plot #8 - Raw data plus important dates plus control data identified plus statistical lines plus new control data plus new statistical lines plus OOC
fig = plt.figure()
ax = plt.subplot(111)
plt.plot(xs, ys, 'bo-', label='Daily Confirmed Cases') 
plt.axvline(DateRed, color='r', label='Pennsylvania Shutdown')
plt.axvline(DateCDCMask, color='c', label='CDC Recommends Masks')
plt.axvline(DatePennMask, color='m', label='State Requires Masks')
plt.axvline(DateYellow, color='y', label = 'Yellow Phase')
plt.axvline(DateGreen, color='g', label = 'Green Phase')
plt.plot(xc0 , yc0, 'yo', label='Control Data (Red Pre-Mask)')
plt.plot((xmin, DateControlStart), (yp30,yp30), color='lightgray', linestyle=':')
plt.text(xmin, yp30, '+3$\sigma$')
plt.text(xmin, (yp30+yp20)/2, 'Zone A')
plt.plot((xmin, DateControlStart), (yp20,yp20), color='silver', linestyle='-.')
plt.text(xmin, yp20, '+2$\sigma$')
plt.text(xmin, (yp20+yp10)/2, 'Zone B')
plt.plot((xmin, DateControlStart), (yp10, yp10), color='darkgray', linestyle='--')
plt.text(xmin, yp10, '+1$\sigma$')
plt.text(xmin, (yp10+yavg0)/2, 'Zone C')
plt.plot((xmin, DateControlStart), (yavg0,yavg0), color='gray', linestyle = '-')
plt.text(xmin, yavg0, 'avg')
plt.text(xmin, (ym10+yavg0)/2, 'Zone C')
plt.plot((xmin, DateControlStart), (ym10,ym10), color='darkgray', linestyle='--')
plt.text(xmin, ym10, '-1$\sigma$')
plt.text(xmin, (ym10+ym20)/2, 'Zone B')
plt.plot((xmin, DateControlStart), (ym20,ym20), color='silver', linestyle='-.')
plt.text(xmin, ym20, '-2$\sigma$')
plt.text(xmin, (ym20+ym30)/2, 'Zone A')
plt.plot((xmin, DateControlStart), (ym30, ym30), color='lightgray', linestyle=':')
plt.text(xmin, ym30, '-3$\sigma$')
plt.plot(xc, yc, 'mo', label='Control Data (Red Post-Mask)')
plt.plot((DateControlStart, xmax), (yp3,yp3), color='lightgray', linestyle=':')
#plt.text(DateControlStart, yp3, '+3$\sigma$')
plt.plot((DateControlStart, xmax), (yp2,yp2), color='silver', linestyle='-.')
#plt.text(DateControlStart, yp2, '+2$\sigma$')
plt.plot((DateControlStart, xmax), (yp1, yp1), color='darkgray', linestyle='--')
#plt.text(DateControlStart, yp1, '+1$\sigma$')
plt.plot((DateControlStart, xmax), (yavg,yavg), color='gray', linestyle = '-')
#plt.text(DateControlStart, yavg, 'avg')
plt.plot((DateControlStart, xmax), (ym1,ym1), color='darkgray', linestyle='--')
#plt.text(DateControlStart, ym1, '-1$\sigma$')
plt.plot((DateControlStart, xmax), (ym2,ym2), color='silver', linestyle='-.')
#plt.text(DateControlStart, ym2, '-2$\sigma$')
plt.plot((DateControlStart, xmax), (ym3, ym3), color='lightgray', linestyle=':')
#plt.text(DateControlStart, ym3, '-3$\sigma$')
plt.plot(OOC1x , OOC1y, 'rv', label='OOC1: Above/Below 3$\sigma$')
plt.plot(OOC2x , OOC2y, 'r^', label='OOC2: 7 points inc/dec')
plt.plot(OOC3x , OOC3y, 'r<', label='OOC3: 8 points on one side of avg')
plt.plot(OOC4x , OOC4y, 'r>', label='OOC4: 14 points in an up/down pattern')
plt.plot(OOC5x , OOC5y, 'rs', label='OOC5 2/3 points in Zone A')
plt.plot(OOC6x , OOC6y, 'rp', label='OOC6: 4/5 points in Zone A/B')
plt.plot(OOC7x , OOC7y, 'rD', label='OOC7: 15 points in Zone C')
plt.title('Raw data: # cases drawn from NYT Covid Tracker on GitHub \n Vertical lines: Important dates in Pennsylvania \n Control data: from 14 days after Pennsylvania Shutdown to the date that the State Requires Masks \n Hortizontal lines: Statistical Zones \n New control data: from 14 days after State Requires Masks to date of Yellow Phase \n Red points: New out-of-control conditions for a Statistical Process')
#shrink axis by 20%
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height * 0.8])
plt.legend(bbox_to_anchor=(1.05, 1))#ncol=2)
plt.xlabel('Date')
#plt.xticks(rotation=30)
plt.ylabel('# of Confirmed COVID Cases Daily in '+str(county) +' County')
mng = plt.get_current_fig_manager()
mng.full_screen_toggle()
plt.show()






