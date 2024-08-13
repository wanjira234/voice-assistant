import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import re

listener = aa.Recognizer()
machine = pyttsx3.init()


def talk(text):
    machine.say(text)
    machine.runAndWait()


def input_instruction():
    instruction = ""  # Initialize the instruction variable
    try:
        with aa.Microphone() as origin:
            print("Listening...")
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            print(f"Recognized Instruction: {instruction}")
            if "jarvis" in instruction:
                instruction = instruction.replace("jarvis", "").strip()
                print(f"Processed Instruction: {instruction}")

    except aa.UnknownValueError:
        print("Sorry, I did not understand the audio.")
        talk("Sorry, I did not understand the audio.")
    except aa.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        talk("Could not connect to the speech recognition service.")
    except Exception as e:
        print(f"Error: {e}")
        talk("Something went wrong.")
    return instruction


def process_instruction(instruction):
    if "play" in instruction:
        song = instruction.replace("play", "").strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)
    elif re.search(r'\btime\b', instruction):
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'The current time is {time}')
    elif re.search(r'\bdate\b', instruction):
        date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        talk(f"Today's date is {date}")
    elif re.search(r'\bhow are you\b', instruction):
        talk("I'm an AI, so I don't have feelings, but thank you for asking!")
    elif re.search(r'\byour name\b', instruction):
        talk("I am Jarvis, your virtual assistant. How can I assist you today?")
    elif "who is" in instruction or "what is" in instruction:
        query = instruction.replace("who is", "").replace("what is", "").strip()
        info = wikipedia.summary(query, sentences=2)
        print(info)
        talk(info)
    elif "thank you" in instruction:
        talk("You're welcome! I'm here to help.")
    elif "stop" in instruction:
        talk("Goodbye! Have a great day!")
        return False  # Signal to stop the loop
    else:
        talk("I'm not sure how to help with that. Could you please rephrase?")
    return True  # Continue the loop


def play_jarvis():
    keep_listening = True
    while keep_listening:
        instruction = input_instruction()
        if instruction:
            keep_listening = process_instruction(instruction)
        else:
            talk("I didn't catch that. Please say it again.")


play_jarvis()
