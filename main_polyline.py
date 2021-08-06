from haversine import haversine
import os
import folium
from folium import plugins
import pynmea2
import webbrowser
import fileinput


coordinates = []


def get_location():
    return os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


def list_coordinates(lat, lon):
    list = []
    list.append(lat)
    list.append(lon)
    return coordinates.append(list)


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
    with open(os.path.join(get_location(), "gps_track.nmea"), encoding='utf-8') as file:
        for line in file.readlines():
            if line.startswith('$GPGGA'):
                msg = pynmea2.parse(line)
                lat = msg.latitude
                lon = msg.longitude
                distance += calculate_distance(lat, lon, prev_lat, prev_lon)
                list_coordinates(lat, lon)
                prev_lat = lat
                prev_lon = lon

    return round(distance, 2)


def create_map():
    m = folium.Map(height=600)
    folium.plugins.AntPath(
        locations=coordinates, reverse="True", dash_array=[20, 30]
    ).add_to(m)
    m.fit_bounds(m.get_bounds())
    return m.save('index.html')


def open_result():
    result_text = "<div style=\"font-size: 40px; text-align: center\">Distance covered: " + str(main_calc()) + "km</div>"
    create_map()
    url = os.path.join(get_location(), "index.html")
    for line in fileinput.FileInput(url, inplace=1):
        if "</div>" in line:
            line = line.replace(line, line+result_text)
        print(line)
    return webbrowser.open(url, new=2)

open_result()