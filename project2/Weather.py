# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 18:42:22 2021

@author: Nolan Jimmo
"""

import json, requests, datetime

class Weather():
    """
    Constructor for weather
    
    Parameters
    ----------
    city where weather needs to be reported
    
    Returns
    -------
    None
    """
    def __init__(self, city_zip):
        self.key = None
        self.read_key()
        self.city_zip = city_zip
        self.temp, self.weather_description, self.wind_speed, self.humidity = self.fetch_weather()
    
    '''
    Getter for the current city
    
    Paramaters
    ---------
    None
    
    Returns
    -------
    current city
    '''
    def get_city_zip(self):
        return self.city_zip
    
    '''
    Setter for the current city
    
    Paramaters
    ---------
    Target city to change to
    
    Returns
    -------
    None
    '''
    def set_city_zip(self, city_zip):
        self.city_zip = city_zip
    
    '''
    Getter for the temperature
    
    Paramaters
    ---------
    None
    
    Returns
    -------
    current temperature
    '''
    def get_temp(self):
        self.update_weather()
        return self.temp
       
    '''
    Getter for the weather description
    
    Paramaters
    ---------
    None
    
    Returns
    -------
    current weather description
    '''
    def get_weather_description(self):
        self.update_weather()
        return self.weather_description
    
    '''
    Getter for the wind speed
    
    Paramaters
    ---------
    None
    
    Returns
    -------
    current wind speed
    '''
    def get_wind_speed(self):
        self.update_weather()
        return self.wind_speed
    
    '''
    Getter for the humidity
    
    Paramaters
    ---------
    None
    
    Returns
    -------
    current humidity
    '''
    def get_humidity(self):
        self.update_weather()
        return self.humidity
    
    '''
    Getter for the aggregated weather as a whole
    
    Paramaters
    ---------
    None
    
    Returns
    -------
    current temp and weather description in a string
    '''
    def get_weather(self):
        return f"{self.get_temp()}F {self.get_weather_description()}, Humidity: {self.get_humidity()} Wind Speed: {self.wind_speed}"
    
    '''
    Helper function to update the temperature and weather description vars
    
    Paramaters
    ---------
    None
    
    Returns
    -------
    None
    '''
    def update_weather(self):
        self.temp, self.weather_description, self.wind_speed, self.humidity = self.fetch_weather()

    '''
    Function to query the API and set the temp and weather_description vars
    appropriately
    
    Paramaters
    ---------
    None
    
    Returns
    -------
    current (int) temperature (fahrenheit), (string) weather description
    '''
    def fetch_weather(self):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = base_url + "appid=" + self.key + "&q=" + self.city_zip
        response = requests.get(complete_url)
        
        weather_data = response.json()
        if weather_data["cod"] == '404':
            print("Weather data could not be loaded from API... request was 404")
            return 0, 0
        else:
            return self.kelvin_to_fahrenheit(weather_data["main"]["temp"]), weather_data["weather"][0]["description"], weather_data["wind"]["speed"], weather_data["main"]["humidity"]
        
    '''
    Helper function to convert temperatures
    
    Paramaters
    ---------
    None
    
    Returns
    -------
    None
    '''
    def kelvin_to_fahrenheit(self, k):
        fah = str((((k-273.15)*9)/5)+32)
        return float(f"{fah:.2}")
    
    '''
    Helper function to read the API key in from txt file (for security)
    Function returns nothing, and set the key internally (for security)
    
    Paramaters
    ---------
    None
    
    Returns
    -------
    None
    '''
    def read_key(self):
        try:
            infile = open('api_k.txt', 'r')
            lines = infile.readlines()
            self.key = lines[0]
            infile.close()
        except:
            print("API key file could not be found")
