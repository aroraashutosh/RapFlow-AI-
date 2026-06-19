import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import base64

st.set_page_config(
    page_title="RapFlow AI 🎤",
    page_icon="🎤",
    layout="centered"
)

def get_base64(file):
    try:
        with open(file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

bg = get_base64("performance4.jpeg")

page_bg = f"""
<style>
.stApp {{
    background: 
        linear-gradient(rgba(0,0,0,0.75), rgba(0,0,0,0.75)),
        url("data:image/jpeg;base64,{bg}") no-repeat center center fixed;
    background-size: cover;
}}
</style>
"""

st.markdown(page_bg, unsafe_allow_html=True)

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("GEMINI_API_KEY not found in .env file")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.5-flash")

st.title("🎤 RapFlow AI")
st.caption("Powered by Gentleman")

bars = st.text_area(
    "Enter your rap bars:",
    height=180,
    placeholder="Raatein lambi, sapne bade..."
)

bpm = st.slider("BPM", 70, 180, 95)

mood = st.selectbox(
    "Mood",
    ["Motivational", "Love", "Sad", "Drill", "Flex", "Conscious"]
)

style = st.selectbox(
    "Style",
    ["Delhi Hip-Hop", "Punjabi", "Melodic", "Hardcore"]
)

if st.button("🔥 Generate Rap"):
    if not bars.strip():
        st.warning("Please enter some bars first.")
    else:
        prompt = f"""
You are a professional Indian hip-hop rapper.

Continue the user's rap.

Mood: {mood}
Style: {style}
BPM: {bpm}

Rules:
- Write exactly 8 bars
- Hinglish language
- Strong rhymes
- Modern Indian hip-hop vibe
- Meaningful lyrics
- Punchlines
- No explanation
- Only output lyrics

User lyrics:
{bars}
"""
        try:
            with st.spinner("Cooking bars... 🎵"):
                response = model.generate_content(prompt)

            st.subheader("🔥 Generated Verse")
            st.write(response.text)

        except Exception as e:
            st.error(f"Error: {e}")

st.markdown("---")
st.markdown("Built by Ashutosh Arora 🎤")
