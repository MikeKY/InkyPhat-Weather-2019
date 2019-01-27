#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inkyphat
from time import sleep, strftime
from PIL import Image, ImageFont
from requests import get
from bs4 import BeautifulSoup

inkyUpdateFreq    =  3     # Minutes Fast that Clock Runs.
weatherUpdateFreq = 30     # Minutes between Weather Updates
checkClockFreq    = 60     # SECONDS between System Clock Checks

dow = strftime('%a')    # String Variables (Date)
date = strftime('%d')
#month = strftime('%m')
dateString = ("{0:3} {1:2}".format(dow, date))
hour = strftime('%H')   # String Variables (Time)
minute = strftime('%M')
#intHour   = int(hour)   # INTEGER Variables (Time)
intMinute = int(minute)

justUpdatedWeather    = False


obsPeriod     = "Time?"
obsTemp     = "?? F"
obsTalk     = "Weather Summary ???"
obsIcon     = "obsIcon?"
obsHumid    = "Humid?"
obsWind     = "obsWind?"
obsPress    = "inHg?"
obsVis      = "Vis?"
obsIndex    = "Index?"
obsUpdated  = "obsUpdated?"
nowTemp     = "NowTemp?"

def UPDATE_WEATHER():
    print('##### UPDATE_WEATHER Called  #####', strftime('%H:%M'), '\n')
    result = get("https://forecast-v3.weather.gov/point/33.7794,-117.9706?view=plain")

#    if 1 == 1:   ### Troubleshooting quick-swaps left in-place
    if(result.status_code == 200):
        content = result.content
        #content = open("/home/michael/WEATHER/NWS-190119.html")
        soup = BeautifulSoup(content, features="html.parser")
        forecastList = soup.findAll('div', attrs={'class':'tombstone-container'})
        period0 = forecastList[0]

        currentWeather = soup.find(id = 'current_conditions-summary')
        nowTemp = currentWeather.find('h1')
        nowTemp = str(nowTemp)
        nowTemp = nowTemp.replace('<h1 class="myforecast-current-lrg">', 'Now: ')
        nowTemp = nowTemp.replace('</h1>', '')

        obsIcon = soup.find_all('h4')  ### Current Forecast Icon
        obsIcon = obsIcon[2]    # Variable obsIcon is a LIST
        obsIcon = str(obsIcon)  # obsIcon changed from List to STRING.  Bad form.
        obsIcon = obsIcon.replace('<h4 class="myforecast-current">', '')
        obsIcon = obsIcon.replace('and ', '')
        obsIcon = obsIcon.replace('</h4>', '').strip()

        obsTable  = soup.find(id = 'current_conditions-observations')
        tableData = obsTable.find_all('td')

        metaTable = []

        try:
            for x in range(0, 14):
                metaData = tableData[x].text.strip()
                shortMetaTable = False
        except IndexError:
                shortMetaTable = True

        if shortMetaTable == True:
            for x in range(0, 12):
                metaData = tableData[x].text.strip()
                metaData = metaData.replace('/n', '')
                metaTable.append(metaData)

            obsIndex   = '--'
            obsUpdated = metaTable[11]
            obsUpdated    = obsUpdated[:19].strip()
            discardDate, discardComma, obsUpdated = obsUpdated.partition(',')
            obsUpdated = obsUpdated.replace(' ', '').strip()[:5]
        else:
            for x in range(0, 14):
                metaData = tableData[x].text.strip()
                metaData = metaData.replace('/n', '')
                metaTable.append(metaData)

            obsIndex   = metaTable[11]
            obsIndex   = obsIndex[:5].strip()
            obsUpdated = metaTable[13]
            obsUpdated = obsUpdated[:19].strip()
            discardDate, discardComma, obsUpdated = obsUpdated.partition(',')
            obsUpdated = obsUpdated.replace(' ', '').strip()[:5]

        obsHumid   = metaTable[1].strip()
        obsHumid   = 'RH ' + obsHumid
        obsWind    = metaTable[3]
        obsWind    = obsWind.replace('at ', '')
        obsWind    = obsWind.replace('mph', '')
        obsWind    = obsWind[:10].strip()
        obsPress   = metaTable[5]
        obsPress   = obsPress.replace('inHg', '')
        obsPress   = obsPress[:10].strip()
        obsPress   = obsPress + '"'
        obsDew     = metaTable[7]
        obsDew     = obsDew[:10].strip()
        obsVis     = metaTable[9]
        obsVis     = obsVis[:10].strip()

        nowArray = []

        for p in period0:
            paragraph = str(p.string)
            paragraph = paragraph.strip()
            nowArray.append(paragraph)

        obsPeriod      = nowArray[1]
        forecastIcon = nowArray[3]
        obsTemp      = nowArray[5]

        if ((obsPeriod[0] == 'T') or (obsPeriod[0] == 'O')):   # Normal Period Descriptors
            obsPeriod = obsPeriod[:14]                         # e.g. Today, This Afternoon, Overnight
        else:
            obsPeriod = 'Weird Report'   # Unusual Weather (or Fed Holiday)
            #obsTemp = '! ! ! !'

        try:
            obsTalk = nowArray[7]
        except IndexError:                 # Broken when NWS overlays Multiple Hazard Advisories
            obsTalk = "Weird Weather -- Check News"
    else:
        obsPeriod     = "Time ?"
        obsTemp     = "?? F"
        obsTalk     = "Weather Summary ???"
        obsIcon     = "obsIcon?"
        obsHumid    = "Humid?"
        obsWind     = "obsWind?"
        obsPress    = "inHg?"
        obsVis      = "Vis?"
        obsIndex    = "Index?"
        obsUpdated  = "obsUpdated?"
        nowTemp = "NowTemp?"

    weatherList = [obsPeriod, obsTemp, obsTalk, obsIcon, obsHumid,
                   obsWind, obsPress, obsVis, obsIndex, obsUpdated, nowTemp]

    print('##### UPDATE_WEATHER Returned*****', strftime('%H:%M'), '\n')

    return(weatherList)

def FAST_TIME (hour, minute, inkyUpdateFreq):
    print('###  FAST_TIME  ###               ', strftime('%H:%M'))
    intHour = int(hour)
    intMinute = int(minute)
    intFastMinute = 0
    intFastHour   = 0
    padZero  = '0'
    fastHour = 'Empty Error'

    intMinutePlusAdjust = intMinute + inkyUpdateFreq

    if intMinutePlusAdjust < 60:
        if intHour != 23:
            intFastHour = intHour
            intFastMinute = intMinutePlusAdjust
        else:
            intFastHour = intHour
            intFastMinute = intMinutePlusAdjust
    elif intMinutePlusAdjust == 60:
        if intHour != 23:
            intFastHour = intHour + 1
            intFastMinute = 0
        else:
            intFastHour = 0
            intFastMinute = 0
    elif intMinutePlusAdjust == 61:
        if intHour != 23:
            intFastHour = intHour + 1
            intFastMinute = 1
        else:
            intFastHour = 0
            intFastMinute = 1
    elif intMinutePlusAdjust == 62:
        if intHour != 23:
            intFastHour = intHour + 1
            intFastMinute = 2
        else:
            intFastHour = 0
            intFastMinute = 2
    elif intMinutePlusAdjust == 63:
        if intHour != 23:
            intFastHour = intHour + 1
            intFastMinute = 3
        else:
            intFastHour = 0
            intFastMinute = 3
    elif intMinutePlusAdjust == 64:
        if intHour != 23:
            intFastHour = intHour + 1
            intFastMinute = 4
        else:
            intFastHour = 0
            intFastMinute = 4

    if intFastHour < 10:
        fastHour = padZero + str(intFastHour)
    else:
        fastHour = str(intFastHour)

    if intFastMinute < 10:
        fastMinute = padZero + str(intFastMinute)
    else:
        fastMinute = str(intFastMinute)

    fastTime = fastHour + ':' + fastMinute

    return(fastTime)

def INKY_DISPLAY (inkyVars):
    print('###  INKY_DISPLAY  ###            ', strftime('%H:%M'),'\n')

    obsHumidPress = obsHumid + '  ' + obsPress

    inkyphat.set_colour('black')
    # inkyphat.set_border(inkyphat.BLACK)

    fontExSmall = ImageFont.truetype(inkyphat.fonts.FredokaOne, 14)
    fontSmall = ImageFont.truetype(inkyphat.fonts.FredokaOne, 18)
    fontMedSmall = ImageFont.truetype(inkyphat.fonts.FredokaOne, 20)
    fontMedium = ImageFont.truetype(inkyphat.fonts.FredokaOne, 29)
    fontMedLarge = ImageFont.truetype(inkyphat.fonts.FredokaOne, 30)
    fontLarge = ImageFont.truetype(inkyphat.fonts.FredokaOne, 38)

    inkyphat.rectangle([(0, 0), (212, 104)], fill=inkyphat.WHITE, outline=None)
    inkyphat.line((106, 1, 106, 85), 1, 1)  # Vertical Mid-line
    inkyphat.line((1, 85, 211, 85), 1, 1)   # Horizontal Line

    ### LEFT side of Display
    wFastTime, hFastTime = fontLarge.getsize(fastTimeString)
    wDate, hDate = fontMedium.getsize(dateString)
    wObsIcon, hObsIcon = fontExSmall.getsize(obsIcon)
    wNowTemp, hNowTemp = fontSmall.getsize(nowTemp)

    xFastTime = (inkyphat.WIDTH / 4) - (wFastTime / 2)
    xDate = (inkyphat.WIDTH / 4) - (wDate / 2)
    xObsIcon = (inkyphat.WIDTH / 4) - (wObsIcon / 2)
    xNowTemp = (inkyphat.WIDTH / 4) - (wNowTemp / 2)

    inkyphat.text((xFastTime, 0), fastTimeString, inkyphat.BLACK, font=fontLarge)
    inkyphat.text((xDate, 35), dateString, inkyphat.BLACK, font=fontMedium)
    inkyphat.text((xNowTemp, 63), nowTemp, inkyphat.BLACK, font=fontSmall)

    ### RIGHT side of Display
    wObsPeriod, hObsPeriod = fontExSmall.getsize(obsPeriod)
    wObsTemp, hObsTemp = fontMedium.getsize(obsTemp)
    wObsWind, hObsWind = fontMedSmall.getsize(obsWind)
    wObsHumidPress, hObsHumidPress = fontExSmall.getsize(obsHumidPress)
    wObsTalk, hObsTalk = fontExSmall.getsize(obsTalk)

    xObsPeriod = (inkyphat.WIDTH * 0.75) - (wObsPeriod / 2)
    xObsTemp = (inkyphat.WIDTH * 0.75) - (wObsTemp / 2)
    xObsWind = (inkyphat.WIDTH * 0.75) - (wObsWind / 2)
    xObsHumidPress = (inkyphat.WIDTH * 0.75) - (wObsHumidPress / 2)
    xObsTalk = (inkyphat.WIDTH / 2) - (wObsTalk / 2)

    inkyphat.text((xObsPeriod, 0), obsPeriod, inkyphat.BLACK, fontExSmall)
    inkyphat.text((xObsTemp, 16), obsTemp, inkyphat.BLACK, font=fontMedium)
    inkyphat.text((xObsWind, 43), obsWind, inkyphat.BLACK, font=fontMedSmall)
    inkyphat.text((xObsHumidPress, 65), obsHumidPress, inkyphat.BLACK, font=fontExSmall)
    inkyphat.text((xObsTalk, 86), obsTalk, inkyphat.BLACK, font=fontExSmall)

    #inkyphat.set_partial_mode(0, 104, 0, 70)
#    inkyphat.text((202,89), 'o', inkyphat.BLACK, font=fontExSmall)
    inkyphat.show()

def PRINT_DEBUG (printVars):
    print('### PRINT_DEBUG ###               ', strftime('%H:%M'))
    obsHumidPress = obsHumid + '  ' + obsPress
    ### LEFT side of Display
    print('LEFT: ', fastTimeString, dateString, nowTemp, '   ', str(justUpdatedWeather))
    ### RIGHT side of Display
    print('RIGHT: ', obsPeriod, obsTemp, obsWind, obsHumidPress)
    ### BOTTOM row of Display
    print('BOTTOM: ', obsTalk, '\n')
    ### NOT INCLUDED
    print('NOT Shown: ', 'obsVis: ', obsVis, 'Heat Index', obsIndex,
          'obsUpdated: ', obsUpdated, 'obsIcon', obsIcon, '\n\n')

#####.............................. Main ..............................#####

weatherList = UPDATE_WEATHER()
(obsPeriod, obsTemp, obsTalk, obsIcon, obsHumid, obsWind,
 obsPress, obsVis, obsIndex, obsUpdated, nowTemp) = weatherList

fastTimeString = FAST_TIME(hour, minute, inkyUpdateFreq)

printVars = [fastTimeString, dateString, nowTemp, justUpdatedWeather,
             obsPeriod, obsTemp, obsWind, obsHumid, obsPress, obsTalk,
             obsVis, obsIndex, obsUpdated, obsIcon]

inkyVars = [fastTimeString, dateString, obsIcon, nowTemp, justUpdatedWeather,
            obsPeriod, obsTemp, obsWind, obsHumid, obsPress, obsTalk]

#if 1 == 1:
while True:
    minute = strftime('%M')
    intMinute = int(minute)

    if intMinute % inkyUpdateFreq == 0:
        dow = strftime('%a')    # String Variables (Date)
        date = strftime('%d')
        dateString = ("{0:3} {1:2}".format(dow, date))
        hour = strftime('%H')
        fastTimeString = FAST_TIME(hour, minute, inkyUpdateFreq)
        INKY_DISPLAY (inkyVars)
        PRINT_DEBUG (printVars)

    if intMinute % weatherUpdateFreq == 0:
        weatherList = UPDATE_WEATHER()
        (obsPeriod, obsTemp, obsTalk, obsIcon, obsHumid, obsWind,
         obsPress, obsVis, obsIndex, obsUpdated, nowTemp) = weatherList
        justUpdatedWeather = True
    else:
        justUpdatedWeather = False

    sleep(checkClockFreq)
