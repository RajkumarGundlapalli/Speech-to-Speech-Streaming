## Speech to Speech Streaming 

This project is a **Streamlit-based application** that processes video files, extracts their audio, translates the audio into a specified language, and synchronizes the translated audio back with the video. It's designed for seamless user experience and multilingual support.

## Features

- **Video Processing**: Extracts audio from uploaded video files.
- **Speech Recognition**: Converts audio to text using Google Speech-to-Text.
- **Translation**: Translates text to a target language using Google Generative AI.
- **Text-to-Speech**: Generates audio from translated text.
- **Audio-Video Synchronization**: Synchronizes the translated audio with the original video.
- **User-Friendly Interface**: Built with custom CSS styling for an interactive and clean UI.

---

## Prerequisites

### Tools & Libraries
- Python 3.7 or higher
- [Streamlit](https://streamlit.io/) for the web interface
- `ffmpeg` for video and audio processing
- `SpeechRecognition` for transcription
- `gTTS` for text-to-speech
- `langdetect` for language detection
- `pydub` for audio manipulation
- `moviepy` for video editing
- `langchain-google-genai` for AI-powered translation
- `dotenv` for environment variable management

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/RajkumarGundlapalli/Speech-to-Speech-Streaming.git
 
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install **FFmpeg**:
   - Linux: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: [Download FFmpeg](https://ffmpeg.org/download.html)

4. Create a `.env` file in the root directory and add your Google API key:
   ```plaintext
   GOOGLE_API_KEY=your_google_api_key
   ```

---

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the local URL provided by Streamlit.

3. Upload an MP4 video file, enter the target language (e.g., `French` or `Hindi`), and click **Process Video**.

4. View and download the processed video with translated audio directly from the app.

---

## Custom CSS

This project includes custom CSS for styling the Streamlit interface:
- Enhanced upload box visuals.
- Styled input fields and buttons.
- Organized layout for video previews.

---

## Output
![Screenshot 2025-01-18 201459](https://github.com/user-attachments/assets/6b1284f8-445b-4636-9528-c623b0ebe63e)

---

## Limitations & Future Improvements

- **Current Limitations**:
  - Dependency on Google Generative AI for translation.
  - Processing speed depends on file size and language model performance.

- **Potential Improvements**:
  - Add support for multiple video formats.
  - Implement language detection for input audio.
  - Improve synchronization accuracy for longer videos.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

