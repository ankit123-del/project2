import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
import os
from bs4 import BeautifulSoup
from pytube import YouTube

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Speak function using pyttsx3
def speak(text):
    engine.say(text)
    engine.runAndWait()

# DuckDuckGo Search Function
def duckduckgo_search(query):
    try:
        url = f"https://duckduckgo.com/html/?q={query}"
        headers = {
            "User-Agent": "Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            return "Failed to retrieve search results."

        soup = BeautifulSoup(response.text, "html.parser")
        result = soup.find("a", class_="result__a")

        if result:
            return f"According to DuckDuckGo: {result.text.strip()}"
        else:
            return "No direct results found on DuckDuckGo. Please refine your query."

    except Exception as e:
        return f"Error fetching search results: {str(e)}"

# Play music from YouTube function

def play_music_on_youtube(song_name):
    try:
        # Search for the song on YouTube
        search_url = f"https://www.youtube.com/results?search_query={song_name.replace(' ', '+')}"
        webbrowser.open(search_url)  # Open search results in the web browser
        speak(f"Searching for {song_name} on YouTube.")
    except Exception as e:
        speak(f"Error occurred while searching for the song: {str(e)}")


# Shutdown function if something fails
def shutdown_pc():
    speak("The program encountered an error. Shutting down the PC.")
    os.system("shutdown /s /t 1")

# Process voice commands
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "play music" in c.lower():
        song_name = c.lower().replace("play music", "").strip()  # Extract song name from the command
        if song_name:
            play_music_on_youtube(song_name)  # Call the play music function
        else:
            speak("Please specify a song name.")
    elif "news" in c.lower():
        # In case of news fetching, you can add your fetch_news function here
        speak("Sorry, news fetching is not yet implemented.")
    else:
        # Pass any general command to DuckDuckGo Search for processing
        output = duckduckgo_search(c)
        if "Failed" in output or "Error" in output:
            speak("There was an issue with the search. Please try again later.")
        else:
            speak(output)

# Main voice recognition loop
if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        try:
            print("Listening for wake word...")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for background noise
                audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)  # Increased time
            word = recognizer.recognize_google(audio)
            print(f"Recognized: {word}")

            if "jarvis" in word.lower():
                speak("Yes, how can I help you?")
            else:
                print("Processing command...")
                processCommand(word)

        except sr.UnknownValueError:
            print("Could not understand the audio, please try again.")
        except sr.RequestError as e:
            print(f"Request error from Google Speech Recognition: {e}")
        except sr.WaitTimeoutError:
            print("Listening timed out, no speech detected.")
        except Exception as e:
            print(f"Error: {str(e)}")
            shutdown_pc()  # Shut down PC in case of an unhandled error
