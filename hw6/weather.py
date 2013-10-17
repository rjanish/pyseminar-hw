
import numpy as np
import sqlalchemy as sql 

def max_entry_size(filename):
    '''Compute the maximum character length of an entry in a csv file'''
    file_max = 0
    with open(filename, 'r') as csv_file:
        for line in csv_file.readlines():
            line = line[:-1] # remove newline
            line_max = max([len(entry) for entry in line.split(",")])
            if line_max > file_max:
                file_max = line_max
    return  file_max

# load all airport and top 50 airport data 
# The use of '^' as comments is to be sure that no characters are 
# flagged as comments, as there are no ^s in the data files.
# The choice of 190 and 70 for string size limits were determined by 
# running the above function 'max_entry_size' on the two datafiles
all_airports = np.loadtxt("ICAO_airports.csv", delimiter=',',
                          skiprows=1, comments='^',
                          dtype=[("id", int),
                                 ("ident", 'S190'),
                                 ("type", 'S190'),
                                 ("name", 'S190'),
                                 ("latitude_deg", 'S190'),
                                 ("longitude_deg", 'S190'),
                                 ("elevation_ft", 'S190'),
                                 ("continent", 'S190'),
                                 ("iso_country", 'S190'),
                                 ("iso_region", 'S190'),
                                 ("municipality", 'S190'),
                                 ("scheduled_service", 'S190'),
                                 ("gps_code", 'S190'),
                                 ("iata_code", 'S190'),
                                 ("local_code", 'S190'),
                                 ("home_link", 'S190'),
                                 ("wikipedia_link", 'S190'),
                                 ("keywords", 'S190')]) 
top_airports = np.loadtxt("top_airports.csv", delimiter=',',
                          skiprows=1, comments='^',
                          dtype=[("City", 'S70'),
                                 ("FAA", 'S70'),
                                 ("IATA", 'S70'),
                                 ("ICAO", 'S70'),
                                 ("Airport", 'S70'),
                                 ("Role", 'S70'),
                                 ("Enplanements", int)])

