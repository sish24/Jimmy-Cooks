import streamlit as st
import torch
import torch.serialization
import soundfile as sf
import os
import io
from pydub import AudioSegment
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import av
from TTS.api import TTS  # Coqui XTTS-v2

st.set_page_config(page_title="🎙️ Jimmy Cooks - Voice Cloning", page_icon="🎤", layout="centered")

# Set environment variable for Coqui
os.environ["COQUI_TOS_AGREED"] = "1"

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load Coqui XTTS-v2 model
st.write("Loading voice cloning model...")

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")

st.title("🎙️ Jimmy Cooks - Personalized Voice Cloning")
st.write("**Upload a voice sample, choose a mood, enter text, and generate speech.**")

# Step 1: Voice Input Selection
st.subheader("🎤 Provide Your Voice Sample")

audio_path = None
recorded_audio_path = "recorded_audio.wav"

def process_audio(frame):
    audio = frame.to_ndarray()
    with open(recorded_audio_path, "ab") as f:
        f.write(audio.tobytes())

# Streamlit WebRTC Audio Recorder
uploaded_file = st.file_uploader("Upload a WAV file (max 5MB)", type=["wav"])
if uploaded_file:
    audio_path = "user_voice_sample.wav"
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("✅ Voice sample uploaded successfully!")
    st.audio(audio_path, format="audio/wav")




# Step 2: Choose Mood
st.subheader("🎭 Select Mood")
mood = st.selectbox("Choose the mood of the cloned voice:", ["Neutral", "Happy", "Sad", "Angry", "Calm", "Excited"])

# Step 3: Adjust Speech Speed
st.subheader("⚡ Adjust Speech Speed")
speech_speed = st.slider("Select speed (0.5x = Slower, 2.0x = Faster, 1.0x = Normal)", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# Step 4: Text input for speech generation
st.subheader("✍️ Enter Text to Synthesize")
text = st.text_area("Type something...", "Hello, this is my cloned voice!")

# Mood settings for Coqui XTTS-v2
# Enhanced Mood Settings with Pitch & Energy
mood_settings = {
    "Neutral": {"speed": 1.0, "pitch": 1.0, "energy": 1.0},
    "Happy": {"speed": 1.1, "pitch": 1.2, "energy": 1.2},
    "Sad": {"speed": 0.9, "pitch": 0.8, "energy": 0.8},
    "Angry": {"speed": 1.2, "pitch": 1.1, "energy": 1.5},
    "Calm": {"speed": 0.95, "pitch": 0.9, "energy": 0.9},
    "Excited": {"speed": 1.3, "pitch": 1.3, "energy": 1.4}
}


# Generate Voice Button
if st.button("🎙️ Generate Voice"):
    if text and audio_path:
        st.info(f"Generating voice with **{mood}** emotion at speed {speech_speed}x...")

        output_wav = "generated_voice.wav"

                # Get selected mood settings
        mood_params = mood_settings[mood]

        # Generate speech with modified parameters
        tts.tts_to_file(
            text=text,
            speaker_wav=audio_path,
            language="en",
            speed=mood_params["speed"],  
            file_path=output_wav
        )

        # Modify pitch and energy using pydub
        audio = AudioSegment.from_wav(output_wav)
        audio = audio + (mood_params["energy"] * 5)  # Adjust volume (energy)
        if mood_params["pitch"] != 1.0:
            audio = audio.speedup(playback_speed=mood_params["pitch"])  # Change pitch

        # Export modified version
        output_wav = "generated_voice_modified.wav"
        audio.export(output_wav, format="wav")


        # Define `fixed_wav` before the try block
        fixed_wav = "generated_voice_fixed.wav"


        # Ensure the generated file is a valid WAV
        try:
            audio = AudioSegment.from_file(output_wav, format="wav")
            output_wav = "generated_voice_fixed.wav"
            audio.export(output_wav, format="wav")

            # Display in Streamlit UI
            st.success("✅ Voice generation complete! Listen to the cloned voice below:")
            st.audio(fixed_wav, format="audio/wav")

            # Provide a download button for the fixed WAV file
            with open(fixed_wav, "rb") as f_wav:
                st.download_button("⬇️ Download as WAV", f_wav, file_name="cloned_voice.wav", mime="audio/wav")


        except Exception as e:
            st.error(f"Error processing the generated audio: {e}")
            st.stop()

        # Adjust speed
        audio = AudioSegment.from_wav(output_wav)
        audio = audio.speedup(playback_speed=speech_speed)
        output_wav = "generated_voice_adjusted.wav"
        audio.export(output_wav, format="wav")

        # Convert to MP3 and OGG
        output_mp3 = "generated_voice.mp3"
        output_ogg = "generated_voice.ogg"
        audio.export(output_mp3, format="mp3")
        audio.export(output_ogg, format="ogg")

        # Display audio player
        st.audio(output_wav, format="audio/wav")

        # Provide multiple format download options
        with open(output_wav, "rb") as f_wav, open(output_mp3, "rb") as f_mp3, open(output_ogg, "rb") as f_ogg:
            st.download_button("⬇️ Download as WAV", f_wav, file_name="cloned_voice.wav", mime="audio/wav")
            st.download_button("⬇️ Download as MP3", f_mp3, file_name="cloned_voice.mp3", mime="audio/mpeg")
            st.download_button("⬇️ Download as OGG", f_ogg, file_name="cloned_voice.ogg", mime="audio/ogg")
    else:
        st.error("⚠️ Please enter text and provide a voice sample!")
