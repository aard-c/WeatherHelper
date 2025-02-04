import requests
import json

def get_weather(api_key, city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    
    # Debugging: Prints the raw API response for any confusion there is
    print("Raw API Response:", response.json())  

    return response.json()

def parse_weather_data(weather_data):
    if weather_data.get('cod') != 200:
        print(f"Error: {weather_data.get('message', 'City not found.')}")
        return None
    
    weather = {
        'city': weather_data['name'],
        'temperature': weather_data['main']['temp'],
        'description': weather_data['weather'][0]['description'],
        'humidity': weather_data['main']['humidity'],
        'pressure': weather_data['main']['pressure'],
        'wind_speed': weather_data['wind']['speed'],
    }
    return weather

def save_favorites(favorites, filename="favorites.json"):
    with open(filename, 'w') as file:
        json.dump(favorites, file)

def load_favorites(filename="favorites.json"):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def main():
    api_key = ''  # Make sure to insert your Open WeatherAPI key here
    while True:
        city = input("Enter city (or 'quit' to exit, 'fav' to show favorites): ").strip()
        
        if city.lower() == 'quit':
            break
        elif city.lower() == 'fav':
            favorites = load_favorites()
            print("Favorites:", favorites)
            continue
        
        weather_data = get_weather(api_key, city)
        weather = parse_weather_data(weather_data)
        
        if weather:
            print(f"\nWeather in {weather['city']}:")
            print(f"Temperature: {weather['temperature']}°C")
            print(f"Description: {weather['description']}")
            print(f"Humidity: {weather['humidity']}%")
            print(f"Pressure: {weather['pressure']} hPa")
            print(f"Wind Speed: {weather['wind_speed']} m/s\n")
            
            save = input("Save this location to favorites? (y/n): ").strip().lower()
            if save == 'y':
                favorites = load_favorites()
                if city not in favorites:
                    favorites.append(city)
                    save_favorites(favorites)
                    print(f"{city} added to favorites!")
                else:
                    print(f"{city} is already in favorites.")
        else:
            print("City not found. Please check the name and try again.")

if __name__ == "__main__":
    main()
