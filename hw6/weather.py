
import csv
from datetime import date

import numpy as np
import sqlalchemy as sql 
import requests

def get_monthy_weather(icao, year, month):
    ''' 
    Download 1 month of daily min/max temps, mean humidity, 
    inches precipitation, and cloud cover level from wunderground.com 
    for a given airport code. Returned as list of dicts, one dict per day.
    '''
    url = ("http://www.wunderground.com/history/airport/{}/{}/{}/1/"
           "MonthlyHistory.html?format=1".format(icao, year, month))
    weather_data = []
    data_stream = requests.get(url).iter_lines()
    data_stream.next() # skip header
    data_stream.next() # skip header
    for line in data_stream:
        data = line.split(',')
        # verify weather data is of numeric type
        # ignore data field and wind direction, which has an annoying tag
        for data_pt, value in enumerate(data[1:-1]): 
            data_pt = data_pt + 1
            try:
                data[data_pt] = float(value)
            except ValueError: # for missing data or trace percip, use 0.0
                data[data_pt] = 0.0
        weather_data.append({"date": unicode(data[0], 'utf-8'),
                             "min_temp": float(data[3]),
                             "max_temp": float(data[1]),
                             "humidity": float(data[8]),
                             "precip": float(data[19]),
                             "cloud_cover": int(data[20])})
    return weather_data

def get_weather_since(icao, year):
    ''' 
    Download all daily min/max temps, mean humidity, inches precipitation,
    and cloud cover level from wunderground.com for a given airport code 
    since Jan 1st of the passed year.  Returned as a list of dicts, 
    with one dict per day.
    '''
    print "\ndownloading weather data from {} since {}:".format(icao, year)
    full_weather_data = []
    for y in range(year, 2014):
        for m in range(1, 13):
            if (y < 2013) or (m < 10):
                print '{}-{:02d}'.format(y, m)
                full_weather_data += get_monthy_weather(icao, y, m)
    return full_weather_data

#####################################################################

# read all airport data,
# save name, icao code, lat, and long 
all_airports = []
all_airports_file = csv.reader(open("ICAO_airports.csv", 'r'))
all_airports_file.next() # skip header
for row in all_airports_file:
    all_airports.append({"icao": unicode(row[1], 'utf-8'), # sql needs to be
                         "name": unicode(row[3], 'utf-8'), # given unicode
                         "lat": float(row[4]), 
                         "long": float(row[5])})
# read top airport data,
# save city and icao codes
top_airports = []
top_airports_file = csv.reader(open("top_airports.csv", 'r'))
top_airports_file.next() # skip header
for row in top_airports_file:
    top_airports.append({"city": unicode(row[0], 'utf-8'),
                         "icao": unicode(row[3], 'utf-8')})

# make airport databases
engine = sql.create_engine('sqlite:///:memory:')
metadata = sql.MetaData()
all_airports_table = sql.Table('all_airports', metadata,
                               sql.Column('icao', sql.String),
                               sql.Column('name', sql.String),
                               sql.Column('lat', sql.Float),
                               sql.Column('long', sql.Float))
top_airports_table = sql.Table('top_airports', metadata,
                               sql.Column('city', sql.String),
                               sql.Column('icao', sql.String))
all_airports_table.create(bind=engine)
top_airports_table.create(bind=engine)
engine.execute(all_airports_table.insert(), all_airports)
engine.execute(top_airports_table.insert(), list(top_airports))

# join airport database, get table of full data on the top 50 airports
joined = top_airports_table.join(all_airports_table, 
                    top_airports_table.c.icao == all_airports_table.c.icao)
query = sql.select([top_airports_table.c.city, all_airports_table])
query = query.select_from(joined)
new_table = engine.execute(query)

# make weather database
start_year = 2008
start_date = date(start_year, 1, 1)
weather_table = sql.Table('weather', metadata,
                          sql.Column('icao', sql.String),
                          sql.Column('date', sql.Integer),
                          sql.Column('min_temp', sql.Float),
                          sql.Column('max_temp', sql.Float),
                          sql.Column('humidity', sql.Float),
                          sql.Column('precip', sql.Float),
                          sql.Column('cloud_cover', sql.Integer))
weather_table.create(bind=engine)
full_weather_data = []
for airport in top_airports:
    airport_weather_data = get_weather_since(airport["icao"], start_year)
    for daily_data in airport_weather_data:
        year_month_day = map(int, daily_data['date'].split('-'))
        num_of_days = (date(*year_month_day) - start_date).days
        daily_data['date'] = num_of_days
        full_weather_data.append(daily_data)
engine.execute(weather_table.insert(), full_weather_data)
