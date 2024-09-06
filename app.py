import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a Youtube Video Summarizer. You will be taking the transcript text and summarizing the entire video and 
providing the important summary in points within 250 words. Please provide the summary of the text given here:
"""

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript = ""
        for entry in transcript_data:
            transcript += " " + entry["text"]
        
        return transcript

    except Exception as e:
        raise e

def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit app
st.title("Youtube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    try:
        video_id = youtube_link.split("v=")[1].split("&")[0]
        st.write(f"Video ID: {video_id}")  # Debugging: Check the extracted video ID
        thumbnail_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"
        st.image(thumbnail_url, use_column_width=True)
    except IndexError:
        st.error("Invalid YouTube link format. Make sure it includes 'v=' followed by the video ID.")

if st.button("Get Detailed Notes"):
    if youtube_link:
        try:
            transcript_text = extract_transcript_details(youtube_link)
            if transcript_text:
                summary = generate_gemini_content(transcript_text, prompt)
                st.markdown("## Detailed Notes:")
                st.write(summary)
        except Exception as e:
            st.error(f"An error occurred: {e}")


























