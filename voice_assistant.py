# from openai import OpenAI
import openai
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("API_KEY")

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except:
        print('Skipping  unknown error')

def generate_response(prompt):
    api_key = API_KEY
    openai.api_key = api_key
    response = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo", #model name
        messages= [{"role": "system", "content": "You are a helpful assistant that generates text aggressive manner for the given prompt."}, 
                   {"role": "user", "content": prompt},
                   {"role": "assistant", "content": "generate the text relevant to topic"}], # establishing a conversational context
        temperature = 0.3, # randomness of the responses 
        max_tokens = 500,   # limit the content of responses 
        top_p = 0.3,       #used for making model make it more selective
        frequency_penalty = 0.6, #to avoid repetative responses 
        presence_penalty=0.8,   #provide more relevant details 
        stop = "python")
    return response["choices"][0]["message"]["content"]
    

def speak_text(text):
    # if st.button("Speak"):
    engine.say(text)
    engine.runAndWait()

def main():
        # Record audio
        st.title("🎙️ Chat with Chatterbot: Your Personal Voice Assistant 🤖")
        
        if st.button("Start Speaking"):
            filename = "input.wav"
         
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                source.pause_threshold = 1
                audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                with open(filename, "wb") as f:
                    f.write(audio.get_wav_data())

            # Transcribe audio to text
            text = transcribe_audio_to_text(filename)
            if text:
                st.header('You said', divider='rainbow')

                # Generate response using GPT-3
                response = generate_response(text)
                st.write(f"GPT-3 says: {response}")

                # Record audio with gtts for video
                tts = gTTS(text=response, lang='en', slow = True)
                tts.save("sample.mp3")

                speak_text(response)

                st.caption("Thank you")

if __name__ == "__main__":
    main()

