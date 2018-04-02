#!/usr/bin/env python
import datetime
import os
import os.path
import requests
import time


temp_refresh_rate = 1000
temp_location = "barcelona"

def addon(which):
    if which in (1, 21, 31):
        return "st"
    elif which in (2, 22):
        return "nd"
    elif which in (3, 23):
        return "rd"
    else:
        return "th"
    
def center(string):
    padding = (terminal_width - len(string))//2
    return padding * " " + string + padding * " "

def fineprint(outlist):
    out = "|" + " " * 2
    padding = "|" + " " * 2
    
    for item in outlist:
        out += item
        out += 2* " " + "|" + 2 * " "
        padding += " " * len(item)
        padding += 2* " " + "|" + 2 * " "

    out = out[:-2]
    padding = padding[:-2]
    print("\n" * ((int(terminal_height)-9)//2))
    print(center(ul(out)))
    print(center(padding))
    print(center(out))
    print(center(padding))
    print(center(ul(out)))
    print("\n" * ((int(terminal_height)-7)//2))

def ul(string):
    return "+" +"-" * (len(string)-2) + "+"

def check_temperature():
    file_name = "/tmp/outside_temperature"
    if os.path.exists(file_name):
        modified = os.path.getmtime(file_name)
        if (time.time() - modified) < temp_refresh_rate:
            with open(file_name, 'r') as infile:
                temperature = infile.read()
            return temperature
    rr = requests.get("https://query.yahooapis.com/v1/public/yql?q=select item.condition.temp from weather.forecast where woeid in (select woeid from geo.places(1) where text%3D%22{0}%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys".format(temp_location))
    temp = rr.json()['query']['results']['channel']['item']['condition']['temp']
    temperature = str((int(temp)-32)*5//9)+ "°C"
    with open(file_name, 'w') as outfile:
        outfile.write(temperature)
    return temperature

check_temperature()

today = datetime.datetime.now()
terminal_width = os.get_terminal_size().columns
terminal_height = os.get_terminal_size().lines

today_date = str(today.strftime("%A, %-d" + addon(today.day) + " of %B"))
now_time = str(today.strftime("%-H:%M"))

fineprint([today_date, now_time, check_temperature()])
