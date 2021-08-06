from haversine import haversine
import os
import pynmea2


def calculate_distance(lat, lon, prev_lat, prev_lon):
    if prev_lat != None and prev_lon != None:
        s1 = (prev_lat, prev_lon)
        s2 = (lat, lon)
        return haversine(s1, s2)
    else:
        return 0


def main_calc():
    distance = 0
    prev_lat = None
    prev_lon = None
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(location, "gps_track.nmea"), encoding='utf-8') as file:
        for line in file.readlines():
            if line.startswith('$GPGGA'):
                msg = pynmea2.parse(line)
                lat = msg.latitude
                lon = msg.longitude
                distance += calculate_distance(lat, lon, prev_lat, prev_lon)
                prev_lat = lat
                prev_lon = lon
    return distance

print(round(main_calc(), 2), 'km')
