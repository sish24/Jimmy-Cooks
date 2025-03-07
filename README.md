
# What is Jimmy Cooks's Voice Cloning?

It is a voice cloning app that lets you generate speech in your own voice (or someone else’s) just by uploading a short audio sample. It gives you control over the mood, speed, and style of the speech, making it sound natural and expressive.

We built this project to explore the power of AI-driven voice synthesis while keeping it simple and accessible. With just a few clicks, you can hear your voice say anything you type.

# What Can You Do With It?

1. Upload a short WAV file of your voice.
2. Choose a mood—neutral, happy, sad, angry, calm, or excited.
3. Adjust the speech speed to make it sound faster or slower.
4. Enter the text you want the cloned voice to say.
5. Generate the speech and listen or download it in WAV, MP3, or OGG format.

# The Core Tech We Used

The app relies on machine learning, audio processing, and web technologies to create a seamless experience. Here’s a breakdown of the key components:

1. Streamlit – Powers the web interface, handling file uploads, buttons, and user interactions.
2. PyTorch – Runs the AI model and checks if a GPU (CUDA) is available for faster processing.
3. Coqui XTTS-v2 – The deep learning model that clones the voice and generates speech.
4. Pydub – Adjusts pitch, speed, and energy to fine-tune the final audio output.
5. Streamlit WebRTC – Allows users to record audio directly if they don’t have a pre-recorded file.
6. Understanding the Code & Model

The heart of this project is Coqui XTTS-v2, a multilingual text-to-speech (TTS) model capable of cloning voices from short samples. Here’s how the app uses it:

Loading the Model

The app first checks if a GPU is available using torch.cuda.is_available().
It then loads the Coqui XTTS-v2 model with:


tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cpu")
This model is designed to synthesize speech that closely matches the uploaded voice.
Processing the Uploaded Voice

The user uploads a WAV file, which is saved locally.

The app extracts key voice characteristics, like tone, pitch, and speaking style, to use them in the final synthesis.
Generating Speech with the Cloned Voice

The user enters text, selects a mood, and adjusts the speech speed.
Each mood has predefined settings for speed, pitch, and energy:

mood_settings = {
    "Neutral": {"speed": 1.0, "pitch": 1.0, "energy": 1.0},
    "Happy": {"speed": 1.1, "pitch": 1.2, "energy": 1.2},
    "Sad": {"speed": 0.9, "pitch": 0.8, "energy": 0.8},
    "Angry": {"speed": 1.2, "pitch": 1.1, "energy": 1.5},
    "Calm": {"speed": 0.95, "pitch": 0.9, "energy": 0.9},
    "Excited": {"speed": 1.3, "pitch": 1.3, "energy": 1.4}
}

These settings modify the final speech output, making it sound more expressive.
Generating the Final Audio

The TTS model converts the input text into speech using the cloned voice:

tts.tts_to_file(
    text=text,
    speaker_wav=audio_path,
    language="en",
    speed=mood_params["speed"],  
    file_path=output_wav
)

Once the initial speech is generated, Pydub is used to apply further modifications, such as pitch and energy adjustments.
Post-Processing & Download Options

The generated voice is converted into multiple formats (WAV, MP3, OGG) for easy playback and sharing. 

Streamlit provides audio players and download buttons so users can listen and save their cloned voice. 

# How to Get Started

1. Upload or record a short voice sample.
2. Select a mood and adjust the speech speed if needed.
3. Enter your text—what do you want your cloned voice to say?
4. Click Generate and let the AI do its thing.
5. Listen to the result and download your cloned voice in different formats.
6. That’s it! This project was built to make voice cloning fun, accessible, and easy to experiment with. Whether you’re curious about AI-generated voices or just want to hear yourself say something in a different tone, Jimmy Cook's Voice Clone is here to bring your words to life.
