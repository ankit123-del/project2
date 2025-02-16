import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
import os
from bs4 import BeautifulSoup

recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Speak function using pyttsx3
def speak(text):
    engine.say(text)
    engine.runAndWait()

# DuckDuckGo Search Function (Improved)
def duckduckgo_search(query):
    try:
        url = f"https://duckduckgo.com/html/?q={query}"
        # Change the User-Agent to mimic Google Chrome
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
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

# Fetch Latest News Headlines from NewsAPI
def fetch_news():
    try:
        # Replace 'YOUR_API_KEY' with your actual NewsAPI key
        api_key = "09c781c4f7f549ab90f3bc7c62b56c2d"
        url = f"https://newsapi.org/v2/everything?q=tesla&from=2024-09-05&sortBy=publishedAt&apiKey=09c781c4f7f549ab90f3bc7c62b56c2d={api_key}"

        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            return ["Failed to fetch news from NewsAPI."]

        # Parse the JSON response
        news_data = response.json()

        # Check if we have articles in the response
        if "articles" not in news_data or not news_data["articles"]:
            return ["No headlines found."]

        # Prepare the list of news headlines
        news_list = [article["title"] for article in news_data["articles"][:5]]
        
        return news_list

    except Exception as e:
        return [f"Error fetching news: {str(e)}"]

# Process voice commands
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "news" in c.lower():
        news_list = fetch_news()
        if news_list:
            for news in news_list:
                speak(news)
        else:
            speak("Sorry, I couldn't fetch the latest news.")
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
