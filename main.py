import os
import openai
from dotenv import load_dotenv
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from datetime import datetime

load_dotenv()

api_key = os.getenv("API_KEY")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key
    print("API Key set to env variable")
else:
    print("API Key not found.")

personality = "You are roleplaying Jarvis, the AI of Tony Stark"
messages = [{"role":"system", "content": f"{personality}"}]
archive = Path(__file__).parent / "archived"

def archive_audio(file_path):
    time = str(datetime.now()).replace(" ", "").replace(":", "-")
    new_path = archive / f"{time}.mp3"
    Path(file_path).rename(new_path)


def generate_audio(text):
    speech_file_path = Path(__file__).parent / "speech.mp3"
    response = openai.audio.speech.create(model="tts-1",voice="onyx",input=text)
    response.stream_to_file(speech_file_path)
    audio_data,sample_rate = sf.read(speech_file_path)
    sd.play(audio_data,sample_rate)
    sd.wait()
    archive_audio(speech_file_path)

def generate_speech():
    response = openai.chat.completions.create(model="gpt-3.5-turbo",messages=messages)
    print(response)
    gpt_reply = response.choices[0].message.content
    print(gpt_reply)
    messages.append({"role": "assistant", "content": f"{gpt_reply}"})
    return gpt_reply

def start():
    while True:
        user_input = input("Enter prompt: ")
        if user_input == "exit": break
        messages.append({"role": "user", "content":f"{user_input}"})
        gpt_reply = generate_speech()
        generate_audio(gpt_reply)

if __name__ == "__main__":
    start()
    