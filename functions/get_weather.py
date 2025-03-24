import requests

# Function to get weather information
def get_weather():
    # Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
    api_key = 'enter_your_api_key_here' 
    base_url = "http://api.openweathermap.org/data/2.5/"
    
    # location, should be more flexible later on
    location = 'boston'
    
    # Create the complete URL for current weather with units set to 'imperial'
    current_url = base_url + "weather?q=" + location + "&appid=" + api_key + "&units=imperial"
    
    # Create the complete URL for 5-day forecast with 3-hour intervals
    forecast_url = base_url + "forecast?q=" + location + "&appid=" + api_key + "&units=imperial"
    
    try:
        # Get current weather data
        response = requests.get(current_url)
        data = response.json()
        
        # Check if the response has an error
        if data.get("cod") != 200:
            return f"Error fetching current weather: {data.get('message', 'Unknown error')}"
        
        # Extract current weather data
        city = data.get("name", "Unknown city")
        country = data.get("sys", {}).get("country", "Unknown country")
        main = data.get("main", {})
        weather_description = data.get("weather", [{}])[0].get("description", "No description")
        temperature_fahrenheit = main.get("temp", "N/A")
        humidity = main.get("humidity", "N/A")
        pressure = main.get("pressure", "N/A")
        wind_speed = data.get("wind", {}).get("speed", "N/A")
        
        # Get 5-day forecast data
        forecast_response = requests.get(forecast_url)
        forecast_data = forecast_response.json()
        
        # Check if the response has an error
        if forecast_data.get("cod") != "200":
            return f"Error fetching forecast data: {forecast_data.get('message', 'Unknown error')}"
        
        # Extract 5-day forecast data
        forecast_report = "\n5-Day Forecast (3-hour intervals):\n"
        for entry in forecast_data.get("list", []):
            dt = entry.get("dt_txt", "No date")
            temp = entry.get("main", {}).get("temp", "N/A")
            description = entry.get("weather", [{}])[0].get("description", "No description")
            forecast_report += (f"- {dt}: Temp: {temp:.1f}°F, Condition: {description.capitalize()}\n")
        
        # Return a detailed weather report with the 5-day forecast
        weather_report = (f"Weather report for {city}, {country}:\n"
                          f"- Temperature: {temperature_fahrenheit:.1f}°F\n"
                          f"- Condition: {weather_description.capitalize()}\n"
                          f"- Humidity: {humidity}%\n"
                          f"- Pressure: {pressure} hPa\n"
                          f"- Wind Speed: {wind_speed} mph\n\n"
                          + forecast_report)
        
    except Exception as e:
        weather_report = f"An error occurred: {e}"
    
    return ("The user asked for the weather, here is the current weather report. Please give them a detailed report as if you are a weather reporter, please use units whenever possible.\n\n" + weather_report)

# Main function to run when script is executed
if __name__ == "__main__":
    print(get_weather())
