# app/main.py

import streamlit as st
from utils.ai_services import (
    get_collaboration_recommendation, 
    generate_full_concept, 
    translate_text, 
    generate_outreach_message,
    generate_audio # <-- Import our new function
)

# --- Page Configuration ---
st.set_page_config(
    page_title="Setu Sangam AI Director",
    page_icon="✨",
    layout="wide"
)

# --- Artisan Profile Sidebar ---
with st.sidebar:
    st.title("🎨 Artisan Profile")
    artisan_name = st.text_input("What is your name?", "Artisan")
    languages = ["English", "Hindi", "Bengali", "Tamil", "Telugu", "Marathi", "Kannada"]
    chosen_language = st.selectbox("What is your preferred language?", languages)
    st.divider()
    st.markdown("Built for the Google Gen AI Hackathon.")

# --- App Title and Description ---
st.title(f"✨ Welcome, {artisan_name}!")
st.header("Setu Sangam: Your AI Co-Creator")
st.markdown("Select your craft. Our AI will recommend a synergistic partner and generate a full collaboration proposal to help you innovate and connect.")
st.divider()

# --- Main App Flow ---
st.subheader("1. Tell Us About Your Craft")
artisan_crafts = ["Madhubani Painting", "Jaipur Blue Pottery", "Kutch Lippan Art", "Kalamkari Textile Art", "Bidriware Metal Inlay", "Pattachitra Scroll Painting"]
my_craft = st.selectbox("I am a...", artisan_crafts)

# Initialize session state variables
st.session_state.setdefault('recommendation', None)
st.session_state.setdefault('full_concept_en', None)
st.session_state.setdefault('full_concept_translated', None)
st.session_state.setdefault('outreach_message', None)

if st.button("🤝 Find My AI Co-Creator", use_container_width=True):
    with st.spinner("Analyzing your craft for the perfect partner..."):
        st.session_state.recommendation = get_collaboration_recommendation(my_craft)
        # Clear all previous results
        st.session_state.full_concept_en = None
        st.session_state.full_concept_translated = None
        st.session_state.outreach_message = None

if st.session_state.recommendation:
    st.success(f"**AI Recommendation:** A great partner for your craft is **{st.session_state.recommendation}**!")
    
    st.subheader("2. Generate the Collaboration Concept")
    if st.button("🚀 Generate Full Concept!", use_container_width=True):
        with st.spinner("Dreaming up a new masterpiece..."):
            english_concept = generate_full_concept(my_craft, st.session_state.recommendation)
            st.session_state.full_concept_en = english_concept
            
            if chosen_language != "English":
                with st.spinner(f"Translating to {chosen_language}..."):
                    st.session_state.full_concept_translated = translate_text(english_concept, chosen_language)
            else:
                st.session_state.full_concept_translated = None

if st.session_state.full_concept_en:
    st.divider()
    st.subheader("✅ Your AI-Generated Proposal")
    
    # Determine which text to display and use for audio
    text_to_show = st.session_state.full_concept_translated or st.session_state.full_concept_en
    language_for_audio = chosen_language if st.session_state.full_concept_translated else "English"

    st.markdown(text_to_show)
    
    # --- NEW: Text-to-Speech "Read Aloud" Feature ---
    if st.button(f"🔊 Read Aloud in {language_for_audio}", use_container_width=True):
        with st.spinner("Generating audio... please wait."):
            audio_bytes = generate_audio(text_to_show, language_for_audio)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.error("Sorry, I couldn't generate the audio at this time.")

    # --- Actionable Outreach Feature ---
    st.divider()
    st.subheader("3. Start the Conversation!")
    if st.button("✍️ Create Outreach Message", use_container_width=True):
        with st.spinner("Drafting a professional message..."):
            st.session_state.outreach_message = generate_outreach_message(st.session_state.full_concept_en)

if st.session_state.outreach_message:
    with st.expander("View and Copy Your Outreach Message", expanded=True):
        st.markdown(st.session_state.outreach_message)
        st.info("You can now copy this message to start a real-world collaboration!")