
from pathlib import Path
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Weather API URLs (free, no API key required)
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODES = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Heavy Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    80: "Rain Showers",
    81: "Moderate Rain Showers",
    82: "Heavy Rain Showers",
    95: "Thunderstorm",
    96: "Thunderstorm With Hail",
    99: "Heavy Thunderstorm With Hail"
}

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SkyCast Weather App</title>
<style>
* { box-sizing: border-box; }
body {
    margin: 0;
    padding: 25px;
    font-family: Arial, sans-serif;
    color: #17233d;
    background: linear-gradient(135deg, #e6edff, #e5f9ff);
}
.container {
    max-width: 850px;
    margin: 30px auto;
}
header, .card, .forecast, .welcome, .error {
    background: white;
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 20px;
    box-shadow: 0 8px 25px #243b6420;
}
header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
header h2 { margin: 0; color: #5268ed; }
header span { color: #318567; font-size: 12px; }
.hero { text-align: center; padding: 25px 0; }
.hero h1 { font-size: 42px; margin-bottom: 10px; }
.hero h1 span { color: #5268ed; }
.hero p { color: #69758d; }
form {
    display: flex;
    gap: 10px;
    max-width: 600px;
    margin: 25px auto 10px;
}
input {
    flex: 1;
    min-width: 0;
    padding: 15px;
    border: 1px solid #dce2f0;
    border-radius: 10px;
    font-size: 16px;
}
button {
    padding: 15px 20px;
    border: none;
    border-radius: 10px;
    color: white;
    background: #5268ed;
    cursor: pointer;
    font-weight: bold;
}
button:hover { background: #394fce; }
.muted { color: #748098; font-size: 13px; }
.weather-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 15px;
    background: #edf2ff;
    padding: 22px;
    border-radius: 14px;
}
.temperature { font-size: 58px; font-weight: bold; }
.symbol { font-size: 65px; }
.metrics, .forecast-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-top: 18px;
}
.metric, .forecast-item {
    padding: 17px;
    background: #f6f8fc;
    border-radius: 12px;
}
.metric p, .forecast-item p {
    margin: 0 0 8px;
    color: #748098;
    font-size: 13px;
}
.metric strong, .forecast-item strong { font-size: 19px; }
.error { color: #a52d36; background: #fff2f2; }
footer { text-align: center; color: #748098; padding: 20px; font-size: 12px; }
@media (max-width: 500px) {
    body { padding: 12px; }
    .container { margin: 8px auto; }
    header, .card, .forecast, .welcome { padding: 17px; }
    .hero h1 { font-size: 32px; }
    form { flex-direction: column; }
    .weather-top { padding: 15px; }
    .temperature { font-size: 43px; }
    .symbol { font-size: 45px; }
    .metrics, .forecast-grid { grid-template-columns: 1fr 1fr; }
}
</style>
</head>
<body>
<div class="container">

<header>
    <h2>☁ SkyCast</h2>
    <span>● LIVE WEATHER</span>
</header>

<section class="hero">
    <h1>Weather, at a <span>glance.</span></h1>
    <p>Check current weather and today's forecast for any city.</p>

    <form method="POST">
        <input name="city" placeholder="Enter city, e.g. Bengaluru"
               value="{{ city_input }}" required>
        <button type="submit">Get Weather →</button>
    </form>
    <p class="muted">Try Bengaluru, Hyderabad, Tirupati, London or Tokyo.</p>
</section>

{% if error %}
<div class="error">
    <strong>Unable to get weather</strong>
    <p>{{ error }}</p>
</div>
{% endif %}

{% if weather %}
<section class="card">
    <p class="muted">CURRENT CONDITIONS</p>
    <h2>{{ weather.city }}{% if weather.region %}, {{ weather.region }}{% endif %}</h2>
    <p class="muted">{{ weather.country }} · {{ weather.time }}</p>

    <div class="weather-top">
        <div>
            <p>{{ weather.condition }}</p>
            <div class="temperature">{{ weather.temp }}°C</div>
            <p class="muted">Feels like {{ weather.feels }}°C</p>
        </div>
        <div class="symbol">{{ weather.symbol }}</div>
    </div>

    <div class="metrics">
        <div class="metric">
            <p>💧 Humidity</p>
            <strong>{{ weather.humidity }}%</strong>
        </div>
        <div class="metric">
            <p>🌬 Wind Speed</p>
            <strong>{{ weather.wind }} km/h</strong>
        </div>
        <div class="metric">
            <p>☁ Cloud Cover</p>
            <strong>{{ weather.cloud }}%</strong>
        </div>
        <div class="metric">
            <p>🌧 Precipitation</p>
            <strong>{{ weather.rain }} mm</strong>
        </div>
    </div>
</section>

<section class="forecast">
    <h2>Today's Forecast</h2>
    <div class="forecast-grid">
        <div class="forecast-item">
            <p>🌡 Highest Temperature</p>
            <strong>{{ weather.high }}°C</strong>
        </div>
        <div class="forecast-item">
            <p>❄ Lowest Temperature</p>
            <strong>{{ weather.low }}°C</strong>
        </div>
        <div class="forecast-item">
            <p>☔ Chance of Rain</p>
            <strong>{{ weather.rain_chance }}%</strong>
        </div>
        <div class="forecast-item">
            <p>🌤 Sunrise</p>
            <strong>{{ weather.sunrise }}</strong>
        </div>
        <div class="forecast-item">
            <p>🌇 Sunset</p>
            <strong>{{ weather.sunset }}</strong>
        </div>
        <div class="forecast-item">
            <p>🌥 Forecast</p>
            <strong>{{ weather.forecast_condition }}</strong>
        </div>
    </div>
</section>
{% else %}
<section class="welcome">
    <h2>Your city's weather, made simple.</h2>
    <p>Enter a city name above to view live weather conditions.</p>
</section>
{% endif %}

<footer>Built with Python + Flask | Weather data by Open-Meteo</footer>
</div>
</body>
</html>
"""


def get_weather(city_name):
    # Find the city's latitude and longitude
    response = requests.get(
        GEOCODING_URL,
        params={
            "name": city_name,
            "count": 1,
            "language": "en",
            "format": "json"
        },
        timeout=15
    )
    response.raise_for_status()

    places = response.json().get("results", [])
    if not places:
        return None

    place = places[0]

    # Fetch current conditions and today's forecast
    response = requests.get(
        WEATHER_URL,
        params={
            "latitude": place["latitude"],
            "longitude": place["longitude"],
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,is_day,precipitation,"
                "weather_code,cloud_cover,wind_speed_10m"
            ),
            "daily": (
                "weather_code,temperature_2m_max,"
                "temperature_2m_min,precipitation_probability_max,"
                "sunrise,sunset"
            ),
            "timezone": place.get("timezone", "auto"),
            "forecast_days": 1
        },
        timeout=15
    )
    response.raise_for_status()
    data = response.json()

    current = data["current"]
    daily = data["daily"]

    code = current.get("weather_code")
    daily_code = daily["weather_code"][0]

    symbols = {
        "Clear Sky": "☀️",
        "Mainly Clear": "🌤️",
        "Partly Cloudy": "⛅",
        "Overcast": "☁️",
        "Fog": "🌫️",
        "Rime Fog": "🌫️",
        "Light Drizzle": "🌦️",
        "Moderate Drizzle": "🌧️",
        "Heavy Drizzle": "🌧️",
        "Slight Rain": "🌦️",
        "Moderate Rain": "🌧️",
        "Heavy Rain": "🌧️",
        "Slight Snow": "❄️",
        "Moderate Snow": "❄️",
        "Heavy Snow": "🌨️",
        "Rain Showers": "🌦️",
        "Moderate Rain Showers": "🌧️",
        "Heavy Rain Showers": "🌧️",
        "Thunderstorm": "⛈️",
        "Thunderstorm With Hail": "⛈️",
        "Heavy Thunderstorm With Hail": "⛈️"
    }

    condition = WEATHER_CODES.get(code, "Unknown Conditions")

    return {
        "city": place.get("name", city_name),
        "region": place.get("admin1", ""),
        "country": place.get("country", ""),
        "time": current.get("time", "N/A"),
        "condition": condition,
        "symbol": symbols.get(condition, "🌤️"),
        "temp": current.get("temperature_2m", "N/A"),
        "feels": current.get("apparent_temperature", "N/A"),
        "humidity": current.get("relative_humidity_2m", "N/A"),
        "wind": current.get("wind_speed_10m", "N/A"),
        "cloud": current.get("cloud_cover", "N/A"),
        "rain": current.get("precipitation", "N/A"),
        "high": daily["temperature_2m_max"][0],
        "low": daily["temperature_2m_min"][0],
        "rain_chance": daily["precipitation_probability_max"][0],
        "sunrise": daily["sunrise"][0].split("T")[-1],
        "sunset": daily["sunset"][0].split("T")[-1],
        "forecast_condition": WEATHER_CODES.get(
            daily_code, "Unknown Conditions"
        )
    }


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None
    city_input = ""

    if request.method == "POST":
        city_input = request.form.get("city", "").strip()

        if not city_input:
            error = "Please enter a city name."
        else:
            try:
                weather = get_weather(city_input)

                if weather is None:
                    error = (
                        f"City '{city_input}' was not found. "
                        "Please check the spelling."
                    )

            except requests.exceptions.Timeout:
                error = "The weather server took too long. Try again."
            except requests.exceptions.ConnectionError:
                error = "Connection failed. Check your internet connection."
            except requests.exceptions.RequestException:
                error = "Weather service unavailable. Please try again."
            except (KeyError, IndexError, TypeError, ValueError):
                error = "Unable to process the weather data. Try again."

    return render_template_string(
        HTML,
        weather=weather,
        error=error,
        city_input=city_input
    )


if __name__ == "__main__":
    print("Starting SkyCast Weather App...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True)
