# Weather Image Saver

**Description:** Create a program that saves the current weather as a PNG image.

**Skills practiced:**
- Working with binary data
- File I/O
- Error handling

**Sample code:**

```python
import fetch_my_weather
import os
from datetime import datetime

def save_weather_image(location, save_directory="weather_images"):
    # Create the directory if it doesn't exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    
    # Get current date and time for the filename
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{save_directory}/{location.replace(' ', '_')}_{current_time}.png"
    
    # Get the weather as PNG
    print(f"Getting weather for {location}...")
    weather_png = fetch_my_weather.get_weather(location=location, is_png=True)
    
    # Check if we got an error
    if not isinstance(weather_png, bytes):
        print(f"Error getting weather: {weather_png}")
        return False
    
    # Save the PNG to a file
    try:
        with open(filename, "wb") as f:
            f.write(weather_png)
        print(f"Saved weather image to {filename}")
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

# Save weather for New York
save_weather_image("New York")
```

**Extensions:**
- Add options for transparent or padded images
- Create a daily weather logger that saves an image every day