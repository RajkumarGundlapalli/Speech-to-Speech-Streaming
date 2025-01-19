import streamlit as st
import os
import ffmpeg
import speech_recognition as sr
from gtts import gTTS
from langdetect import detect
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Custom CSS for colorful UI
st.markdown(
    """
    <style>
    body {
        background-color: #fffae6;
        font-family: 'Arial', sans-serif;
    }
    .main-title {
        text-align: center;
        color: red;
        font-size: 36px;
        font-weight: bold;
    }
    .sub-title {
        color: #444444;
        font-size: 18px;
        text-align: center;
        margin-bottom: 20px;
    }
    .upload-box {
        border: 2px solid #2e77d0;
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
    }
    .stTextInput>div>div>input {
        border: 2px solid #2e77d0 !important;
        border-radius: 5px !important;
        background-color: #ffffff !important;
    }
    .stButton>button {
        background-color: #28a745;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #218838;
    }
    .video-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin-top: 20px;
    }
    .video-box {
        background-color: #f0f8ff;
        border: 2px solid #d0d0d0;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Helper functions
def extract_audio(input_video_path, output_audio_path):
    """Extract audio from a video file and save it as a WAV file."""
    ffmpeg.input(input_video_path).output(
        output_audio_path, acodec="pcm_s16le", ac=1, ar="16000"
    ).run()

def transcribe_audio(audio_path):
    """Transcribe audio using SpeechRecognition."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)

def translate_text(input_text, target_language):
    """Translate text using Google Generative AI."""
    summary_prompt = """
    You are a translator where you will be given input text:
    {input}
    You need to translate that input text into the desired language, i.e., {convertLanguage}.
    """
    prompt_template = PromptTemplate(
        input_variables=["input", "convertLanguage"], template=summary_prompt
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        api_key=GOOGLE_API_KEY
    )
    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke({"input": input_text, "convertLanguage": target_language})

def text_to_speech(text, output_audio_path):
    """Convert text to speech and save it as an MP3 file."""
    detected_language = detect(text)
    tts = gTTS(text=text, lang=detected_language)
    tts.save(output_audio_path)

def synchronize_audio_with_video(video_path, audio_path, output_path):
    """Synchronize the translated audio with the video."""
    video_clip = VideoFileClip(video_path)
    translated_audio = AudioSegment.from_file(audio_path)
    translated_duration = len(translated_audio) / 1000
    original_duration = video_clip.duration
    speed_factor = translated_duration / original_duration
    adjusted_audio = translated_audio._spawn(
        translated_audio.raw_data,
        overrides={"frame_rate": int(translated_audio.frame_rate * speed_factor)}
    ).set_frame_rate(translated_audio.frame_rate)
    adjusted_audio_path = "adjusted_audio.mp3"
    adjusted_audio.export(adjusted_audio_path, format="mp3")
    adjusted_audio_clip = AudioFileClip(adjusted_audio_path)
    final_video = video_clip.set_audio(adjusted_audio_clip)
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", audio=True)

# Streamlit Application
st.markdown("<h1 class='main-title'>Video to Multilingual Audio Synchronizer</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Upload a video, translate its audio, and download the final version.</p>", unsafe_allow_html=True)

# File upload
st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload MP4 Video", type=["mp4"])
st.markdown("</div>", unsafe_allow_html=True)
target_language = st.text_input("Enter Target Language (e.g., Hindi, French)")

if st.button("Process Video"):
    if uploaded_file and target_language:
        with st.spinner("Processing your video. Please wait..."):
            # Save uploaded video
            input_video_path = "uploaded_video.mp4"
            with open(input_video_path, "wb") as f:
                f.write(uploaded_file.read())

            # Step 1: Extract audio from video
            audio_path = "extracted_audio.wav"
            extract_audio(input_video_path, audio_path)

            # Step 2: Transcribe audio to text
            try:
                transcribed_text = transcribe_audio(audio_path)
            except Exception as e:
                st.error(f"Error during transcription: {e}")
                st.stop()

            # Step 3: Translate text to target language
            try:
                translated_text = translate_text(transcribed_text, target_language)
            except Exception as e:
                st.error(f"Error during translation: {e}")
                st.stop()

            # Step 4: Convert translated text to audio
            translated_audio_path = "translated_audio.mp3"
            try:
                text_to_speech(translated_text, translated_audio_path)
            except Exception as e:
                st.error(f"Error during text-to-speech: {e}")
                st.stop()

            # Step 5: Synchronize translated audio with video
            output_video_path = "final_video.mp4"
            try:
                synchronize_audio_with_video(input_video_path, translated_audio_path, output_video_path)
            except Exception as e:
                st.error(f"Error during synchronization: {e}")
                st.stop()

        st.success("Processing complete!")

        # Display videos side by side
        st.markdown("<div class='video-container'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='video-box'>", unsafe_allow_html=True)
            st.video(input_video_path)
            st.write("**Original Video**")
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='video-box'>", unsafe_allow_html=True)
            st.video(output_video_path)
            st.write("**Translated Video**")
            st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Provide download link
        with open(output_video_path, "rb") as f:
            st.download_button("Download Translated Video", f, file_name="translated_video.mp4")

    else:
        st.error("Please upload a video and specify a target language.")
