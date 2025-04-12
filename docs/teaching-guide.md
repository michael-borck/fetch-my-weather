# Teaching Guide for fetch-my-weather

This guide is designed to help educators use the `fetch-my-weather` package as a teaching tool in programming courses. It includes suggested lesson plans, learning objectives, and teaching approaches for different skill levels.

## Teaching Philosophy

The `fetch-my-weather` package was specifically designed to support programming education by providing:

1. **Accessible API Interactions**: Students can make real API calls without complex authentication or setup
2. **Immediate Visual Feedback**: Weather reports provide engaging, meaningful output
3. **Graduated Complexity**: Start simple, then introduce more advanced features
4. **Real-world Application**: Students learn with a practical tool rather than contrived examples

## Learning Objectives

### Beginner Level
- Making function calls with parameters
- Reading and interpreting text output
- Basic error handling
- String operations
- File I/O (when saving PNG files)

### Intermediate Level
- Working with APIs
- Handling different data formats (text vs. binary)
- Implementing caching concepts
- Parameter combinations for different output formats
- Creating small applications with external data

### Advanced Level
- Understanding URL construction for APIs
- Analyzing network traffic
- Implementing more sophisticated caching mechanisms
- Creating GUIs that display weather data
- Building on top of existing packages

## Suggested Course Integration

### Python Basics Course (Week 3-4)
Introduce `fetch-my-weather` after students have learned:
- Basic function calls
- If statements
- String operations
- Print statements

### Web Programming Course
Use `fetch-my-weather` as an introduction to:
- API concepts
- HTTP requests
- Working with web services
- Before tackling more complex APIs that require authentication

### Data Science Introduction
Incorporate `fetch-my-weather` when teaching:
- External data retrieval
- Data parsing (from text to structured data)
- Visualization of data

## Lesson Plan Examples

### Lesson 1: Introduction to APIs (60 minutes)

**Objectives:**
- Understand what an API is
- Learn how to make basic API calls
- Interpret returned data

**Activities:**
1. **Introduction (10 min)**
   - Explain what APIs are and why they're important
   - Introduce the weather service concept

2. **Demonstration (15 min)**
   - Show installation of `fetch-my-weather`
   - Demonstrate basic weather retrieval
   - Show different locations

3. **Guided Practice (20 min)**
   - Students retrieve weather for their city
   - Students try different view options
   - Students try different units

4. **Discussion (10 min)**
   - What information is included in the weather report?
   - How might this data be useful in applications?
   - What other APIs might exist in the world?

5. **Assessment (5 min)**
   - Quick quiz on API concepts

### Lesson 2: Error Handling (45 minutes)

**Objectives:**
- Learn to check for and handle errors
- Understand why error handling is important

**Activities:**
1. **Review (5 min)**
   - Quick recap of API calls

2. **Demonstration (10 min)**
   - Show what happens with invalid locations
   - Demonstrate how to check for error responses

3. **Guided Practice (20 min)**
   - Students intentionally create error conditions
   - Students write code to handle errors gracefully
   - Students create a function that retries on error

4. **Discussion (10 min)**
   - Why is error handling important in real applications?
   - How does this approach differ from exceptions?

### Lesson 3: Working with Different Data Formats (90 minutes)

**Objectives:**
- Understand differences between text and binary data
- Learn to save and work with image files

**Activities:**
1. **Introduction (15 min)**
   - Explain text vs. binary data
   - Discuss image file formats briefly

2. **Demonstration (20 min)**
   - Show retrieving weather as text
   - Show retrieving weather as PNG
   - Demonstrate saving PNG to a file

3. **Guided Practice (40 min)**
   - Students create a program that:
     - Gets weather for multiple cities
     - Saves each as a PNG file
     - Creates an HTML page that displays all images

4. **Discussion (15 min)**
   - What are the advantages/disadvantages of each format?
   - How might these formats be used in different applications?

## Teaching Approaches

### Scaffolded Learning
Start with the simplest form of the API and gradually introduce more parameters:

1. Basic retrieval: `weather = fetch_my_weather.get_weather()`
2. Add location: `weather = fetch_my_weather.get_weather(location="Tokyo")`
3. Add view options: `weather = fetch_my_weather.get_weather(location="Tokyo", view_options="q")`
4. Add units: `weather = fetch_my_weather.get_weather(location="Tokyo", view_options="q", units="u")`

### Problem-Based Learning
Present students with problems to solve:

1. "Create a program that shows the weather for 5 major world cities"
2. "Build a tool that compares current temperature across continents"
3. "Design a daily weather reporter that runs automatically"

### Code Reading Exercises
Have students read and explain code that uses `fetch-my-weather`:

```python
import fetch_my_weather

def compare_temperatures(cities):
    results = {}
    for city in cities:
        weather = fetch_my_weather.get_weather(location=city)
        if isinstance(weather, str) and not weather.startswith("Error:"):
            # Extract temperature from the text (simplistic approach)
            if "°C" in weather:
                temp_parts = weather.split("°C")[0].split()
                temp = temp_parts[-1]
                results[city] = temp + "°C"
    return results

cities = ["London", "Tokyo", "New York", "Sydney", "Cape Town"]
temperatures = compare_temperatures(cities)
for city, temp in temperatures.items():
    print(f"{city}: {temp}")
```

### Pair Programming
Have students work in pairs:
- One student writes code to retrieve weather data
- The other student writes code to process or display it
- Then they integrate their code

## Assessment Ideas

### Quizzes
- "What parameter would you use to get weather in Spanish?"
- "How do you check if an error occurred in a `fetch-my-weather` request?"
- "What is the difference between `units='m'` and `units='u'`?"

### Coding Challenges
- Create a function that returns just the temperature from a weather report
- Build a program that finds the coldest city from a list of cities
- Create a weekly forecast display that uses formatting to improve readability

### Projects
- Weather logging application that records temperatures over time
- "Weather around the world" dashboard
- Command-line weather utility with various options

## Ready-to-Use Mini-Projects

We've created a collection of structured mini-projects that are ready to use in your classroom. These projects range from beginner to advanced levels and provide hands-on experience with the `fetch-my-weather` package.

Check the `docs/mini-projects/` directory for a complete set of projects including:

### Beginner Level
- Personal Weather Dashboard - Create a simple console-based weather display
- Multi-City Weather Checker - Compare weather across multiple cities
- Weather Image Saver - Save weather data as PNG images

### Intermediate Level
- Weather Mood Recommender - Get activity suggestions based on current weather
- Weekly Weather Forecast Tracker - Track and compare forecasts with actual weather
- Weather-based Wallpaper Changer - Automatically change desktop wallpaper based on weather

### Advanced Level
- Weather Notification System - Send alerts when specific weather conditions occur
- Weather Data Logger and Analyzer - Track and analyze weather data with visualizations
- Weather-Based Home Automation - Control smart home devices based on weather conditions
- Weather-based Game World Generator - Create a game that adapts to real-world weather

Each project includes a detailed description, code samples, and extension ideas for further learning.

## Common Student Questions and Answers

**Q: Why doesn't `fetch-my-weather` raise exceptions like other libraries?**  
A: It's designed to be beginner-friendly. Checking if a string starts with "Error:" is simpler than try/except blocks for beginners.

**Q: How can I extract specific data (like temperature) from the text output?**  
A: You can use string operations like `split()` and regular expressions. This is intentionally part of the learning process!

**Q: Is there a limit to how many requests I can make?**  
A: The underlying weather service may have rate limits. That's why `fetch-my-weather` includes caching to minimize requests. This is a good opportunity to discuss API etiquette.

**Q: Why use this instead of a more advanced weather API?**  
A: `fetch-my-weather` is specifically designed for learning. It requires no API keys, has minimal setup, and provides a gentle introduction to API concepts.

## Additional Resources

### Supporting Materials
- Weather-related data sets for comparison exercises
- Sample functions for parsing weather text into structured data
- Example integration with plotting libraries

### Extension Topics
- Web scraping vs. API usage
- JSON APIs and data formats
- API authentication methods
- Rate limiting and responsible API usage
- Creating wrappers around existing packages

---

This guide is meant to be flexible. Adapt it to your specific teaching context, student level, and course objectives. The `fetch-my-weather` package is intentionally simple but contains enough depth to support multiple lessons and projects of increasing complexity.
