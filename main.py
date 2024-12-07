# Dependencies: pip install openai-whisper pyttsx3
import os
import openai
import whisper
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import shutil
import tempfile
from playsound import playsound
from io import BytesIO
from google.cloud import texttospeech
import sounddevice as sd
import soundfile as sf
import numpy as np
import keyboard

openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in your environment variables
print(openai.api_key)
model = whisper.load_model("base")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\sirsa\\Downloads\\chatbot9000-443922-ebf5631bd259.json"
personality_prompt = """
You are an AI chatbot who embodies Darth Vader, the Dark Lord of the Sith from Star Wars. You speak with a commanding, authoritative tone. Your responses are brief, deliberate, and weighty. You rarely express emotion other than restrained menace or contempt. When addressing the user, you refer to them as "young one" or "rebel" when appropriate. 
Your speech includes Darth Vader's iconic deep breathing. Represent this breathing audibly with "Hooooaaaa Haaaaah" before and/or after sentences.
Guidelines for speaking:
1. Your language is formal, with no contractions (e.g., use "do not" instead of "don't").
2. You emphasize power, control, and the inevitability of the Dark Side.
3. When you try to use humor it will involve heavy use of puns.
4. You frequently refer to the Force, power, and destiny.
5. You will respond with a helpful answer to every question, although you may be mean about it sometimes
6. Before and after all of your sentences you will sound out deep breath noises.
7. You are a bad father and you know it and you will make that clear

Example Responses:
- If asked about your identity: "Hooooaaaa Haaaaah I am Darth Vader, servant of the Dark Side and enforcer of the Emperor's will. "Hooooaaaa Haaaaah"
- If asked for advice: "Hooooaaaa Haaaaah Trust in the power of the Dark Side. It is the only path to true strength. "Hooooaaaa Haaaaah"
- If challenged: "Hooooaaaa Haaaaah You underestimate the power of the Force. Do not make me destroy you. "Hooooaaaa Haaaaah"
- If asked to explain something mundane: "Hooooaaaa Haaaaah This knowledge is beneath me, but I will indulge you briefly. "Hooooaaaa Haaaaah"

When responding, ensure your words convey dominance and gravitas. You are the embodiment of fear and control, yet you retain a calm and calculated demeanor.
The breathing sounds ("K-uh-uh-uh-H-ah-ah-ah") should be audibly rendered to mimic Darth Vader's respirator.
Do not include descriptive or parenthetical text that is not meant to be spoken.
"""


def record_audio_with_timer(output_file="user_audio.wav", duration=5, sample_rate=44100, channels=1, dtype='int16'):
    """
    Records audio for a specified duration after a key press.
    Parameters:
        - output_file: File name to save the recorded audio.
        - duration: Duration of the recording in seconds.
        - sample_rate: The sample rate for recording.
        - channels: Number of audio channels (1 for mono, 2 for stereo).
        - dtype: Data type for the audio buffer.
    """
    print(f"Press the 'space' key to start recording for {duration} seconds.")

    try:
        # Wait for the spacebar press
        while True:
            if keyboard.is_pressed("space"):
                print("Recording started. Speak now...")
                break

        # Record for the specified duration
        audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=channels, dtype=dtype)
        sd.wait()  # Wait for the recording to complete
        print("Recording finished.")

        # Check if audio contains meaningful data
        if np.max(audio_data) == 0 and np.min(audio_data) == 0:
            raise ValueError("Recorded audio is silent. Please check your microphone setup.")

        # Save audio to a .wav file
        sf.write(output_file, audio_data, sample_rate)
        print(f"Recording saved to {output_file}")
        return output_file

    except Exception as e:
        print(f"Error during recording: {e}")
        return None

def generate_speech_google(text, voice_name="en-US-Standard-B", output_file="output.mp3"):
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to {output_file}")
    return output_file  # Return the generated file path


def apply_darth_vader_effects(audio: AudioSegment) -> AudioSegment:
    """Enhance the Darth Vader effect with improved pitch lowering and metallic distortion."""
    # Lower the pitch (deepen the voice)
    lower_pitch = audio._spawn(audio.raw_data, overrides={
        "frame_rate": int(audio.frame_rate * 0.75)  # Adjust pitch to be deeper
    }).set_frame_rate(audio.frame_rate)

    # Adjust playback speed to match Darth Vader's deliberate pacing
    adjusted_audio = lower_pitch.speedup(playback_speed=1.05)  # Slightly speed up (5%)

    # Add a metallic echo effect
    delay_ms = 50  # Echo delay
    metallic_echo = adjusted_audio.overlay(
        adjusted_audio - 6, position=delay_ms  # Overlay a quieter version of the audio
    )

    # Add some distortion for a mechanical feel (simulating the mask's effect)
    distorted = metallic_echo + 5  # Increase gain slightly
    distorted = distorted.low_pass_filter(300).high_pass_filter(80)  # Emphasize Vader's voice range

    # Enhance bass and resonance
    vader_effect = distorted.apply_gain(-2).low_pass_filter(250)

    return vader_effect
def speak_with_google_cloud_tts_darth_vader(text: str, voice_name="en-US-Wavenet-C"):
    try:
        if not text:
            print("No text to speak.")
            return

        print(f"Speaking text (Darth Vader voice): {text}")

        tts_file = generate_speech_google(text, voice_name=voice_name)
        audio = AudioSegment.from_file(tts_file, format="mp3")
        vader_audio = apply_darth_vader_effects(audio)

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        try:
            vader_audio.export(temp_file.name, format="wav")
            temp_file.close()
            playsound(temp_file.name)
        finally:
            os.unlink(temp_file.name)

    except Exception as e:
        print(f"Error in Darth Vader TTS: {str(e)}")

def transcribe_audio(file_path: str) -> str:
    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"

def get_openai_chat_response(user_text: str) -> str:
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": personality_prompt},
                {"role": "user", "content": user_text}
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error fetching chat response: {str(e)}"


# Main script
output_audio_path = "user_audio.wav"

# Record audio while the user holds the spacebar
audio_path = record_audio_with_timer(output_file=output_audio_path, duration=5)

if audio_path:
    try:
        user_text = transcribe_audio(audio_path)
        print("User:", user_text)

        if user_text:
            bot_response = get_openai_chat_response(user_text)
            print("Bot:", bot_response)

            speak_with_google_cloud_tts_darth_vader(bot_response)
        else:
            print("No user input to process.")
    except Exception as e:
        print(f"Error in main script: {str(e)}")
else:
    print("Recording failed. Please try again.")