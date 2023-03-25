import os
import requests
from datetime import datetime, timedelta

def get_calgary_weather():
    # Set up the API request
    api_key = 'YOUR API KEY'
    api_url = f'https://api.openweathermap.org/data/2.5/forecast?q=calgary,CA&appid={api_key}&units=metric'

    # Make the API request and parse the response
    response = requests.get(api_url)
    if response.status_code != 200:
        return "API request failed."
    data = response.json()

    today = datetime.today()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    message = "**Here's the weather forecast for Calgary for the next 7 days:**\n"

    max_temp = float('-inf')
    max_temp_day = None

    for i in range(7):
        date = today + timedelta(days=i)
        day = days[date.weekday()]
        forecast = next((f for f in data['list'] if datetime.fromtimestamp(f['dt']).date() == date.date()), None)
        if forecast:
            temp = round(forecast['main']['temp'])
            desc = forecast['weather'][0]['description'].title()
            message += f"{day}: {temp}°C, {desc}\n"
            if temp > max_temp:
                max_temp = temp
                max_temp_day = day

    message += f"\nThe warmest day will be **{max_temp_day}**, with a high of **{max_temp}°C**, I recommend going out then"

    return message