import joblib
import numpy as np
import random
import json
from urllib.request import urlopen
import requests

def main():
    url = "https://ipinfo.io//json"
    response = urlopen(url)
    data = json.load(response )

    print(data["city"])
    insaan_ki_city = data["city"]



    def get_weather(city, count):

        url = f"https://wttr.in/{city}?format=%C+%t+%w+%h"

        # Send a GET request to the website
        response = requests.get(url)

        # If the request is successful, parse and display the weather data
        if count == 10:
            return

        if response.status_code == 200:
            weather_info = response.text
            weather_info_list = weather_info.split()

            sky = weather_info_list[0]
            temperature = weather_info_list[1]
            wind_speed = weather_info_list[2]
            precipitation = weather_info_list[3]
            print(f"Weather for {city}:\n{weather_info}")
            print("..............")
            print(weather_info_list)
            return sky, temperature, wind_speed, precipitation


        else:
            count = count +1
            return get_weather(city, count)


    sky, temperature, wind_speed, precipitation = get_weather(data["city"], 0)


    # Load saved models and encoders
    trend_model = joblib.load("trend_predictor.joblib")
    top_model = joblib.load("top_predictor.joblib")
    bottom_model = joblib.load("bottom_predictor.joblib")
    le_city = joblib.load("le_city.joblib")
    le_sky = joblib.load("le_sky.joblib")
    le_trend = joblib.load("le_trend.joblib")
    le_top = joblib.load("le_top.joblib")
    le_bottom = joblib.load("le_bottom.joblib")

    # List of valid cities, sky conditions, and trends from the dataset
    valid_cities = le_city.classes_
    valid_skies = le_sky.classes_
    valid_trends = le_trend.classes_

    # Function to recommend outfit
    def recommend_outfit(city, temperature, sky):
        try:
            # Encode city, if city is unknown, choose a random city from dataset
            try:
                city_enc = le_city.transform([city])[0]
            except:
                city_enc = random.choice(valid_cities)  # Randomly pick a city from the dataset
                city_enc = le_city.transform([city_enc])[0]  # Re-encode the randomly chosen city

            # Encode sky condition, if sky is unknown, choose a random sky condition
            try:
                sky_enc = le_sky.transform([sky])[0]
            except:
                sky_enc = random.choice(valid_skies)  # Randomly pick a sky condition from the dataset
                sky_enc = le_sky.transform([sky_enc])[0]  # Re-encode the randomly chosen sky condition

            # Predict the trend based on city, temperature, and sky
            try:
                trend_enc = trend_model.predict([[city_enc, temperature, sky_enc]])[0]
                trend = le_trend.inverse_transform([trend_enc])[0]
            except:
                # If trend prediction fails, choose a random trend
                trend_enc = random.choice(valid_trends)
                trend = le_trend.inverse_transform([trend_enc])[0]  # Decode the random trend

            # Encode the trend to pass it into the prediction models
            trend_enc = le_trend.transform([trend])[0]

            # Predict top and bottom based on the predicted trend
            try:
                top_enc = top_model.predict([[city_enc, temperature, sky_enc, trend_enc]])[0]
            except:
                top_enc = -1  # Default value if top prediction fails

            try:
                bottom_enc = bottom_model.predict([[city_enc, temperature, sky_enc, trend_enc]])[0]
            except:
                bottom_enc = -1  # Default value if bottom prediction fails

            # Decode the top and bottom, if available
            try:
                top = le_top.inverse_transform([top_enc])[0] if top_enc != -1 else "No top predicted"
            except:
                top = "No top predicted"

            try:
                bottom = le_bottom.inverse_transform([bottom_enc])[0] if bottom_enc != -1 else "No bottom predicted"
            except:
                bottom = "No bottom predicted"

            # Return the recommended outfit as a list
            return [top, bottom]

        except Exception as e:
            print(f"❌ Error: {e}")
            return ["Could not generate recommendation based on input"]

    # Example usage
    temperature_celsius = int((int(temperature[1:3]) - 32) / 1.8)
    outfit = recommend_outfit(insaan_ki_city, temperature_celsius, sky)

    print(f"Recommended Outfit: {outfit}")
    return outfit