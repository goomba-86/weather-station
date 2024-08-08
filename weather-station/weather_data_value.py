class WeatherDataValue:
    """Class to encapsulate weather data for a single time instance"""

    def __init__(self, datetime, temperature, weather_symbol):
        self.datetime = datetime
        self.temperature = temperature
        self.weather_symbol = weather_symbol

    def get_temperature(self):
        """Get the temperature value"""
        return self.temperature

    def get_datetime(self):
        """Get the temperature value"""
        return self.datetime

    def get_weather_symbol(self):
        """Get the weather symbol value as integer"""
        return self.weather_symbol
