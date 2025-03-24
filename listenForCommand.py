from gtts import gTTS
import os
import speech_recognition as sr
from responseFinder import responseFinder
from tts import speak

# Initialize the speech recognition engine
recognizer = sr.Recognizer()

# Function to append speech to a transcript file
def append_to_transcript(transcript):
    if not os.path.exists("text_files"):
        os.makedirs("text_files")
    with open("text_files/transcript.txt", "a") as file:
        file.write(transcript + "\n")

# Function to save the command to a text file
def save_command_to_file(command):
    if not os.path.exists("text_files"):
        os.makedirs("text_files")
    with open("text_files/latest_command.txt", "w") as file:
        file.write(command)

# Function to listen for a command that includes the wake word
def listen_for_command(wake_word="deon"):
    with sr.Microphone() as source:
        print("Listening for command...")
        while True:
            try:
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio).lower()
                print(f"Detected speech: {command}")

                # Always update the transcript file
                append_to_transcript(command)

                # Check if the wake word is in the command
                if wake_word in command:
                    print(f"Wake word '{wake_word}' detected!")
                    # Save the command to a text file
                    save_command_to_file(command)

                    # Remove wake word from command before processing
                    full_command = command.replace(wake_word, "").strip()

                    return full_command

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")