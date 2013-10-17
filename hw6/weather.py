
import csv

import numpy as np
import sqlalchemy as sql 


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

# make databases
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
engine.execute(all_airports_table.insert(), all_airports).rowcount
engine.execute(top_airports_table.insert(), list(top_airports)).rowcount

# join database, get table of full data on the top 50 airports
joined = top_airports_table.join(all_airports_table, 
                    top_airports_table.c.icao == all_airports_table.c.icao)
query = sql.select([top_airports_table.c.city, all_airports_table])
query = query.select_from(joined)
new_table = engine.execute(query)