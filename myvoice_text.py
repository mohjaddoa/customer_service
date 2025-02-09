import whisper
import sounddevice as sd
import numpy as np
import webrtcvad
import wave
import os
from gtts import gTTS
from playsound import playsound
import streamlit as st

class myvoice_text:
    def __init__(self, samplerate=16000, channels=1):
        self.samplerate = samplerate
        self.channels = channels
        self.vad = webrtcvad.Vad()
        self.vad.set_mode(2)  # Mode 2: Balanced (higher = more aggressive, 0-3)
# recording voice 
    def record_until_silence(self, filename="temp_audio.wav", silence_duration=1.5):
        """
        Record audio from the microphone until the user finishes speaking.

        :param filename: Filename to save the recorded audio
        :param silence_duration: Duration of silence (in seconds) to stop recording
        """
        st.write("Please start speaking...")
        buffer_size = int(self.samplerate * 0.02)  # 20ms buffer
        silence_threshold = int(silence_duration / 0.02)  # Number of silent buffers
        audio_data = []
        silent_buffers = 0

        stream = sd.InputStream(samplerate=self.samplerate, channels=self.channels, dtype="int16")
        stream.start()

        try:
            while True:
                buffer = stream.read(buffer_size)[0]
                audio_data.append(buffer)

                # Detect voice activity
                is_speech = self.vad.is_speech(buffer.tobytes(), self.samplerate)
                if is_speech:
                    silent_buffers = 0  # Reset silence counter if speech is detected
                else:
                    silent_buffers += 1
                    if silent_buffers > silence_threshold:
                        break  # Stop recording if silence is detected for the threshold duration
        finally:
            stream.stop()
            stream.close()
            print("Recording complete. Saving audio...")

        # Save audio to a WAV file
        audio_np = np.concatenate(audio_data, axis=0)
        with wave.open(filename, "wb") as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)  # 16-bit audio
            wav_file.setframerate(self.samplerate)
            wav_file.writeframes(audio_np.tobytes())
# voice to text 
    def transcribe_audio(self, model_size="base", audio_filename="temp_audio.wav"):
        """
        Record and transcribe audio using Whisper.

        :param model_size: Whisper model size (e.g., "base", "small")
        :param audio_filename: The audio file to transcribe
        :return: Transcription text
        """
        self.record_until_silence(filename=audio_filename)

        # Load Whisper model
        model = whisper.load_model(model_size)

        print("Transcribing audio...")
        try:
            # Transcribe the audio using Whisper
            transcription = model.transcribe(audio_filename)
            print("Transcription: ", transcription["text"])
            return transcription["text"]
        except Exception as e:
            print("An error occurred during transcription:", str(e))
            return None

    def text_to_speech(self, text, output_audio="output.mp3"):
        """
        Convert text to speech using Google Text-to-Speech (gTTS).

        :param text: The text to convert to speech
        :param output_audio: The filename to save the speech audio
        """
        try:
            tts = gTTS(text=text, lang="en")
            tts.save(output_audio)
            print("Text converted to speech. Playing audio...")
            playsound(output_audio)
            os.remove(output_audio)  # Clean up the temporary audio file
        except Exception as e:
            print("An error occurred during text-to-speech conversion:", str(e))
