# Weather-based Wallpaper Changer

**Description:** Create a program that changes your desktop wallpaper based on the current weather.

**Skills practiced:**
- System integration
- Image handling
- Conditional logic
- Scheduled tasks

**Sample code:**

```python
import simple_weather
import os
import platform
import ctypes
import subprocess
import tempfile
from datetime import datetime

def get_weather_condition():
    """Get the current weather condition"""
    weather = simple_weather.get_weather(view_options="0q")
    
    if isinstance(weather, str) and not weather.startswith("Error:"):
        # Simple weather condition detection (could be improved)
        weather_lower = weather.lower()
        
        if "rain" in weather_lower or "shower" in weather_lower:
            return "rainy"
        elif "snow" in weather_lower or "blizzard" in weather_lower:
            return "snowy"
        elif "cloud" in weather_lower or "overcast" in weather_lower:
            return "cloudy"
        elif "sunny" in weather_lower or "clear" in weather_lower:
            return "sunny"
        else:
            # Default to current weather image
            return "current"
    else:
        print(f"Error getting weather: {weather}")
        return None

def set_wallpaper(image_path):
    """Set the desktop wallpaper (platform specific)"""
    try:
        # Windows
        if platform.system() == "Windows":
            ctypes.windll.user32.SystemParametersInfoW(20, 0, image_path, 0)
            return True
        # macOS
        elif platform.system() == "Darwin":
            script = f'''
            tell application "Finder"
                set desktop picture to POSIX file "{image_path}"
            end tell
            '''
            subprocess.run(['osascript', '-e', script], check=True)
            return True
        # Linux (assuming GNOME)
        elif platform.system() == "Linux":
            subprocess.run(['gsettings', 'set', 'org.gnome.desktop.background', 
                           'picture-uri', f"file://{image_path}"], check=True)
            return True
        else:
            print(f"Unsupported platform: {platform.system()}")
            return False
    except Exception as e:
        print(f"Error setting wallpaper: {e}")
        return False

def change_wallpaper_based_on_weather():
    """Change wallpaper based on current weather"""
    # Get current weather condition
    condition = get_weather_condition()
    
    if condition == "current":
        # Use current weather image as wallpaper
        temp_file = os.path.join(tempfile.gettempdir(), f"weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        
        # Get current weather as PNG with padding for better wallpaper fit
        weather_png = simple_weather.get_weather(is_png=True, png_options="p")
        
        if isinstance(weather_png, bytes):
            with open(temp_file, "wb") as f:
                f.write(weather_png)
            
            # Set as wallpaper
            if set_wallpaper(temp_file):
                print(f"Set current weather as wallpaper: {temp_file}")
                return True
    else:
        # In a real application, you would have custom wallpapers for each condition
        # For this example, we'll use the weather image
        print(f"Weather condition: {condition}")
        
        # Get weather image
        temp_file = os.path.join(tempfile.gettempdir(), f"weather_{condition}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        
        # Get current weather as PNG
        weather_png = simple_weather.get_weather(is_png=True, png_options="p")
        
        if isinstance(weather_png, bytes):
            with open(temp_file, "wb") as f:
                f.write(weather_png)
            
            # Set as wallpaper
            if set_wallpaper(temp_file):
                print(f"Set {condition} weather as wallpaper: {temp_file}")
                return True
    
    return False

# Run the function
print("Changing wallpaper based on weather...")
success = change_wallpaper_based_on_weather()
if success:
    print("Wallpaper changed successfully!")
else:
    print("Failed to change wallpaper.")
```

**Note:** This script attempts to work on Windows, macOS, and Linux, but platform-specific behavior might require adjustments.

**Extensions:**
- Add custom wallpapers for different weather conditions
- Create a scheduler that updates the wallpaper every few hours
- Add transition effects between wallpapers