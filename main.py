import speech_recognition as sr
import pyttsx3
import openai
import requests
import webbrowser
import os
import threading
from gtts import gTTS
import pygame

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# API keys
openai.api_key = "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"
newsapi = ""

# Speak function using pyttsx3
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Process OpenAI commands
def aiProcess(command):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks."},
                {"role": "user", "content": command}
            ]
        )
        return completion.choices[0].message['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Process voice commands
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get('articles', [])
            for article in articles[:5]:  # Read only first 5 articles
                speak(article['title'])
    else:
        # Pass any command to OpenAI for processing
        output = aiProcess(c)
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
            print(f"Error; {str(e)}")
