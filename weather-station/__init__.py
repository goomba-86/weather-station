from lxml.etree import ElementTree
from lxml import etree
import requests
from weather_data_value import WeatherDataValue


def read_raw_weather_data():
    """Download raw weather data in WFS format"""
    request_string = (
        "https://opendata.fmi.fi/wfs?service=WFS&version=2.0.0&"
        "request=getFeature&"
        "storedquery_id=fmi::forecast::edited::weather::scandinavia::point::simple&"
        "place=espoo&"
    )
    weather_data = requests.get(request_string)
    return weather_data.content


def parse_raw_weather_data(raw_weather_data):
    root = etree.fromstring(raw_weather_data)

    wfs = "{http://www.opengis.net/wfs/2.0}"
    bswfs = "{http://xml.fmi.fi/schema/wfs/2.0}"
    times_and_temperatures = []
    times_and_weather_symbols = []
    for item in root.findall(f"./{wfs}member/{bswfs}BsWfsElement"):
        parameter_name = item.find(f"{bswfs}ParameterName")
        if parameter_name.text == "Temperature":
            temperature = item.find(f"{bswfs}ParameterValue")
            time = item.find(f"{bswfs}Time")
            times_and_temperatures.append((time.text, temperature.text))
        elif parameter_name.text == "WeatherSymbol3":
            weather_symbol_int = int(float(item.find(f"{bswfs}ParameterValue").text))
            time = item.find(f"{bswfs}Time")
            times_and_weather_symbols.append((time.text, weather_symbol_int))

    if len(times_and_temperatures) != len(times_and_weather_symbols):
        raise RuntimeError(
            "The number of temperatures and weather symbols does not match."
        )

    weather_data = []
    # Merge two arrays
    for count, time_temp in enumerate(times_and_temperatures):
        data_point = WeatherDataValue(
            time_temp[0],
            time_temp[1],
            times_and_weather_symbols[count][1],
        )
        weather_data.append(data_point)

    return weather_data


def weather_symbol_3_to_string(symbol):
    match int(float(symbol)):
        case 1:
            return "selkeää"
        case 2:
            return "puolipilvistä"
        case 21:
            return "heikkoja sadekuuroja"
        case 22:
            return "sadekuuroja"
        case 23:
            return "voimakkaita sadekuuroja"
        case 3:
            return "pilvistä"
        case 31:
            return "heikkoa vesisadetta"
        case 32:
            return "vesisadetta"
        case 33:
            return "voimakasta vesisadetta"
        case 41:
            return "heikkoja lumikuuroja"
        case 42:
            return "lumikuuroja"
        case 43:
            return "voimakkaita lumikuuroja"
        case 51:
            return "heikkoa lumisadetta"
        case 52:
            return "lumisadetta"
        case 53:
            return "voimakasta lumisadetta"
        case 61:
            return "ukkoskuuroja"
        case 62:
            return "voimakkaita ukkoskuuroja"
        case 63:
            return "ukkosta"
        case 64:
            return "voimakasta ukkosta"
        case 71:
            return "heikkoja räntäkuuroja"
        case 72:
            return "räntäkuuroja"
        case 73:
            return "voimakkaita räntäkuuroja"
        case 81:
            return "heikkoa räntäsadetta"
        case 82:
            return "räntäsadetta"
        case 83:
            return "voimakasta räntäsadetta"
        case 91:
            return "utua"
        case 92:
            return "sumua"


raw_data = read_raw_weather_data()
temp = parse_raw_weather_data(raw_data)

for t in temp:
    print(f"{t.get_datetime()} {t.get_temperature()} {t.get_weather_symbol()}")
