import requests
from geopy.geocoders import Nominatim

class Weather():
    def __init__(self,token):
        self.token = token

    def get_weather(self,latitude,longitude):
        '''
        arguments - latitude, longitude
        takes in arguments as inputs and constructs URL to make API call to OpenWeatherMap API
        returns a response JSON after fetching weather data for the specified latitude and longitude
        '''
        url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&units={}&lang={}&appid={}'.format(latitude, longitude, 'metric', 'es', self.token)
        response = requests.get(url)
        #print(response.json())
        return response.json()

        
    def fetch_weather(self,message): 
        '''
        called when the user provides location in response to the '/weather' command.
        uses the 'location_handler' function to get latitude & longitude of the provided location and 'get_weather' function to fetch the weather data
        extracts weather description from API response and sends to user as message.
        '''
        latitude, longitude = self.location_handler(message)
        weather = self.get_weather(latitude,longitude)
        data = weather['list']
        data_2 = data[3]
        info_weather = data_2['weather']
        info_main= data_2['main']
        temp= info_main['temp']
        temp_max= info_main['temp_max']
        temp_min= info_main['temp_min']
        feels_like=info_main['feels_like']
        data_3 = info_weather[0]
        description = data_3['description']
        icon = data_3['icon']
        weather_message = f'*Temperatura de hoy será:* {temp}°C\n *Sensación térmica:* {feels_like}°C\n *Temperatura máxima:* {temp_max}°C\n *Temperatura mínima:* {temp_min}°C\n *Descripción:* {description}\n'
        print(icon)
        return weather_message

    def location_handler(self,message):
        '''
        returns the latitude and longitude coordinated from user's message (location) using the Nominatim geocoder.
        if location is found - returns the rounded latitude and longitude
        else - returns Location not found
        '''
        location = message.text
        # Create a geocoder instance
        geolocator = Nominatim(user_agent="my_app")

        try:
            # Get the latitude and longitude
            location_data = geolocator.geocode(location)
            latitude = round(location_data.latitude,2)
            longitude = round(location_data.longitude,2)
            #self.logger.info("Latitude '%s' and Longitude '%s' found for location '%s'", latitude, longitude, location)
            return latitude, longitude
        except AttributeError:
            #self.logger.exception('Location not found', exc_info=True)
            print("error")
