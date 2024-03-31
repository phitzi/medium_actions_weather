import pandas as pd
import requests, json, pprint
from sendemail import send_email
from datetime import datetime
from jinja2 import Template
import os

weather_api_key = os.environ["WEATHER_API_KEY"]
location = 'London'
csv_file = "temperature_log.csv"

# Get the weather forcast
url= f'http://api.weatherapi.com/v1/forecast.json?key={weather_api_key}&q={location}&days=4&aqi=no&alerts=no'
response = requests.get(url)
data = json.loads(response.text)

# Create a new entry for the csv in a dataframe
new_entry = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
    'last_updated': data['current']['last_updated'],
    'location': f'{data['location']['name']}/{data['location']['country']}',
    'condition': data['current']['condition']['text'],
    'temperature': data['current']['temp_c'],
    'feels_like': data['current']['feelslike_c'],
    'humidity': data['current']['humidity'],
    'wind_speed': data['current']['wind_kph']
}
new_entry_df = pd.DataFrame([new_entry])

# Append the new entry to the csv and save it
# Use try except in case the file does not exist (first time)
try:
    df = pd.read_csv(csv_file)
    df = pd.concat([df, new_entry_df])
except FileNotFoundError:
    df = new_entry_df.copy()
df.to_csv(csv_file, index=False)

#read html template and render the template
with open('template_forecast.html', 'r') as file:
    html_template = file.read()
template = Template(html_template)
html_output = template.render(data=data)

#send the email
send_email("Temprature Forecast Daily Email", html_output)
