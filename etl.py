import pandas as pd
import requests
import pymysql
import matplotlib.pyplot as plt

# MySQL Connection using PyMySQL
conn = pymysql.connect(
    host="localhost",
    user="tharun4",
    password="Tharun@4237",
    database="weather_tracker"
)

cursor = conn.cursor()

# Read CSV
df = pd.read_csv("events.csv")

# City Coordinates
locations = {
    "Bangalore": (12.97, 77.59),
    "Hyderabad": (17.38, 78.48),
    "Chennai": (13.08, 80.27),
    "Mumbai": (19.07, 72.87)
}

# Risk Counters
low_risk = 0
high_risk = 0

for index, row in df.iterrows():

    city = row['city']
    date = row['date']

    lat, lon = locations[city]

    # Insert Event
    cursor.execute("""
        INSERT INTO events(event_name, venue, city, event_date)
        VALUES (%s, %s, %s, %s)
    """, (row['event_name'], row['venue'], city, date))

    conn.commit()

    event_id = cursor.lastrowid

    # Weather API
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,weathercode&start_date={date}&end_date={date}&timezone=auto"

    response = requests.get(url)
    data = response.json()

    temp = data['daily']['temperature_2m_max'][0]
    code = data['daily']['weathercode'][0]

    # Weather Risk Logic
    if code in [61, 63, 65, 71, 73]:
        risk = "High Risk"
        condition = "Rain/Snow"
        high_risk += 1
    else:
        risk = "Low Risk"
        condition = "Clear"
        low_risk += 1

    # Insert Forecast
    cursor.execute("""
        INSERT INTO weather_forecasts(event_id, temperature, weather_condition, weather_risk)
        VALUES (%s, %s, %s, %s)
    """, (event_id, temp, condition, risk))

    conn.commit()

print("ETL Completed Successfully")

# Matplotlib Chart
labels = ["Low Risk", "High Risk"]
values = [low_risk, high_risk]

plt.bar(labels, values)
plt.title("Weather Risk Events")
plt.xlabel("Risk Type")
plt.ylabel("Number of Events")
plt.show()

cursor.close()
conn.close()
