import streamlit as st
from google import genai
from google.genai import types
import wave
import base64

# =========================
# Function to save wave file
# =========================
def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

# =========================
# Streamlit App
# =========================
st.set_page_config(
    page_title="Gemini TTS Generator",
    page_icon="🎙️",
    layout="centered"
)

# Sidebar - API key
st.sidebar.header("🔑 Gemini API Key")
api_key = st.sidebar.text_input(
    "Enter your API Key",
    type="password",
    placeholder="sk-xxxxxxxxxxxxxxxx"
)

# Main title
st.title("🎙️ Gemini Text-to-Speech")
st.markdown(
    """
    Generate **high-quality speech** from text using **Google Gemini**.
    Just enter your API key, choose a style, and write your script.
    """
)

# Audio style
prompt = st.text_input(
    "🎭 Speaking Style",
    placeholder="Example: Calm and friendly tone"
)

# Audio script
text = st.text_area(
    "📝 Script to Speak",
    placeholder="Type your text here..."
)

# Generate button
if st.button("🎧 Generate Audio"):
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.")
    elif not prompt or not text:
        st.error("Please enter both a speaking style and script.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            with st.spinner("Generating audio... ⏳"):
                response = client.models.generate_content(
                    model="gemini-2.5-flash-preview-tts",
                    contents=f"{prompt}: {text}",
                    config=types.GenerateContentConfig(
                        response_modalities=["AUDIO"],
                        speech_config=types.SpeechConfig(
                            voice_config=types.VoiceConfig(
                                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                                    voice_name='Kore',
                                )
                            )
                        ),
                    )
                )
                data = response.candidates[0].content.parts[0].inline_data.data
                file_name = "output.wav"
                wave_file(file_name, data)

            # Read and encode file for download
            with open(file_name, "rb") as f:
                audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()

            st.success("✅ Audio generated successfully!")
            st.audio(audio_bytes, format="audio/wav")

            st.download_button(
                label="⬇️ Download Audio",
                data=audio_bytes,
                file_name="output.wav",
                mime="audio/wav"
            )

        except Exception as e:
            st.error(f"Error: {str(e)}")
