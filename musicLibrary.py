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

# Wikipedia Search Function
def wikipedia_search(query):
    try:
        # Search for the query on Wikipedia
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={query}&format=json"
        response = requests.get(search_url)

        if response.status_code != 200:
            return "Failed to retrieve search results from Wikipedia."

        data = response.json()

        if "query" in data and "search" in data["query"] and len(data["query"]["search"]) > 0:
            # Get the first result
            page_title = data["query"]["search"][0]["title"]
            page_id = data["query"]["search"][0]["pageid"]

            # Fetch the page content
            page_url = f"https://en.wikipedia.org/w/api.php?action=parse&pageid={page_id}&prop=text&format=json"
            page_response = requests.get(page_url)
            page_data = page_response.json()

            if "parse" in page_data and "text" in page_data["parse"]:
                # Get the text and strip HTML tags
                page_content = page_data["parse"]["text"]
                soup = BeautifulSoup(page_content, 'html.parser')
                summary = soup.get_text()
                
                # Shorten the summary to a specific length (optional)
                summary = summary[:500]  # Limit summary to 500 characters
                return f"According to Wikipedia: {page_title}. {summary}..."
            else:
                return f"Could not fetch details for {page_title}."

        else:
            return "No results found on Wikipedia. Please refine your query."

    except Exception as e:
        return f"Error fetching search results from Wikipedia: {str(e)}"

# Play music from YouTube function
def play_music_on_youtube(song_name):
    try:
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
        song_name = c.lower().replace("play music", "").strip()
        if song_name:
            play_music_on_youtube(song_name)
        else:
            speak("Please specify a song name.")
    else:
        # Use Wikipedia search for any other commands
        output = wikipedia_search(c)
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
