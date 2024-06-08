import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import requests
import subprocess

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except Exception as e:
        print(e)
        return ""
    return command


def get_weather():
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = "YOUR_CITY_NAME"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        temperature = main["temp"]
        pressure = main["pressure"]
        humidity = main["humidity"]
        weather_description = weather["description"]
        weather_report = (f"Temperature: {temperature - 273.15:.2f}°C\n"
                          f"Pressure: {pressure} hPa\n"
                          f"Humidity: {humidity}%\n"
                          f"Description: {weather_description}")
        talk(weather_report)
        print(weather_report)
    else:
        talk("City not found.")
        print("City not found.")


def open_application(app_name):
    app_paths = {
        "safari": "/System/Applications/Safari.app",
        "notes": "/System/Applications/Notes.app",
        "calendar": "/System/Applications/Calendar.app",
        # Add more applications and their paths as needed
    }
    if app_name in app_paths:
        subprocess.Popen(["open", app_paths[app_name]])
        talk(f"Opening {app_name}")
    else:
        talk(f"Application {app_name} not found")


def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'weather' in command:
        get_weather()
    elif 'open' in command:
        app_name = command.replace('open', '').strip()
        open_application(app_name)
    else:
        talk('Please say the command again.')


while True:
    run_alexa()
