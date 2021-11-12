# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 19:28:36 2021

@author: Nolan jimmo
"""

from Weather import Weather

user_input = str(input("What is the zip code of your current city?"))

w = Weather(user_input)
print(f"The weather in {w.get_city_zip()} is: Temp: {w.get_temp()} f  Description: {w.get_weather_description()}")