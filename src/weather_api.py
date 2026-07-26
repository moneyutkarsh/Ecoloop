import requests
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)

# Cache the 24-hour temperatures so we don't spam the API
_WEATHER_CACHE: Optional[List[float]] = None

def fetch_dynamic_weather(api_key: str = "TJJ8QVE8WLFSH7ESVVC2TQYHL") -> List[float]:
    """
    Fetches the 24-hour temperature forecast for Chicago today using the Visual Crossing Weather API.
    Returns a list of 24 float temperatures. Uses an in-memory cache after the first call.
    """
    global _WEATHER_CACHE
    if _WEATHER_CACHE is not None and len(_WEATHER_CACHE) == 24:
        return _WEATHER_CACHE

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/Chicago/today?unitGroup=metric&include=hours&key={api_key}&contentType=json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        hours_data = data.get("days", [])[0].get("hours", [])
        temps = []
        for i in range(24):
            if i < len(hours_data):
                temps.append(float(hours_data[i].get("temp", 22.0)))
            else:
                temps.append(22.0)
                
        _WEATHER_CACHE = temps
        logger.info(f"Successfully fetched dynamic weather from API: {_WEATHER_CACHE}")
        return temps
    except Exception as e:
        logger.error(f"Failed to fetch dynamic weather: {e}")
        # Fallback to the synthetic Chicago summer curve
        fallback = [21.5, 20.8, 20.2, 19.8, 19.5, 20.5, 22.0, 24.0, 26.2, 28.5, 30.2, 31.8, 32.5, 33.0, 32.8, 32.0, 30.5, 28.8, 26.8, 25.2, 24.0, 23.0, 22.2, 21.6]
        return fallback
