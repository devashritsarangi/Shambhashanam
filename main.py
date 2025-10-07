import speech_recognition as sr
import pyttsx3 
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def chat_with_chatbot(prompt):
    # This code is for v1 of the openai package: pypi.org/project/openai
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "user",
                "content": "Your name is Sambhashanam and under the hood you are OpenAI's GPT-3.5 Engine."   
            },
            {
                "role": "assistant",
                "content": "My name is Sambhashanam and under the hood I am OpenAI's GPT-3.5 Engine."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content.strip()

r = sr.Recognizer() 
def SpeakText(command, voice):
    engine = pyttsx3.init()
    newVoiceRate = 140
    engine.setProperty('rate',newVoiceRate)
    if voice == "male":
        engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0")
    elif voice == "female":
        engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0")
    engine.say(command) 
    engine.runAndWait()

# Loop infinitely for user to speak
def listen():   
    try:
        with sr.Microphone() as sourceMic:
            r.adjust_for_ambient_noise(sourceMic, duration=0.05)
            
            print("\nNow listening...")
            # Listening to User
            audio2 = r.listen(sourceMic)
            # Audio recognition using Google
            prompt = r.recognize_google(audio2)
            airesponse = chat_with_chatbot(prompt)
            updChatWindow(prompt=prompt, msg=airesponse)
            return airesponse
    except sr.RequestError as e:
        updChatWindow(msg=f"Couldn't request results; {e}")
        
    except sr.UnknownValueError:
        updChatWindow(msg=f"Sorry, I couldn't recognize what you just said. Please try again.")

def updChatWindow(msg, prompt=None):
    if prompt == None:
        prompt = " "
    with open('chat.txt', 'w') as f:
        f.write(f"You: {prompt} \nSambhashanam: {msg} \n")
    with open('aimsg.txt', 'w') as f:
        f.write(msg)

def speak(msg, voice):
    SpeakText(msg, voice)