from fastmcp import FastMCP
import httpx

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get the weather for a location"""
    async with httpx.AsyncClient() as client:
        # Get coordinates for the location
        geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
        geo_response = await client.get(geocode_url)
        geo_data = geo_response.json()

        if not geo_data.get("results"):
            return f"Location '{location}' not found"

        latitude = geo_data["results"][0]["latitude"]
        longitude = geo_data["results"][0]["longitude"]
        city_name = geo_data["results"][0]["name"]

        # Get weather data
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code"
        weather_response = await client.get(weather_url)
        weather_data = weather_response.json()

        temperature = weather_data["current"]["temperature_2m"]
        weather_code = weather_data["current"]["weather_code"]

        # Simple weather code mapping
        weather_desc = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Foggy", 48: "Foggy", 51: "Light drizzle", 53: "Drizzle",
            55: "Heavy drizzle", 61: "Light rain", 63: "Rain", 65: "Heavy rain",
            71: "Light snow", 73: "Snow", 75: "Heavy snow", 95: "Thunderstorm"
        }.get(weather_code, "Unknown")

        return f"Weather in {city_name}: {temperature}°C, {weather_desc}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")