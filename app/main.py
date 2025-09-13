# app/main.py

import streamlit as st
from utils.ai_services import get_collaboration_recommendation, generate_full_concept, translate_text, generate_outreach_message

# --- Page Configuration ---
st.set_page_config(
    page_title="Setu Sangam AI Director",
    page_icon="🥻",
    layout="wide"
)

# --- Artisan Profile Sidebar ---
with st.sidebar:
    st.title("Artisan Profile")
    artisan_name = st.text_input("What is your name?", "Artisan")
    
    languages = ["English", "Hindi", "Bengali", "Tamil", "Telugu", "Marathi"]
    chosen_language = st.selectbox("What is your preferred language?", languages)
    
    st.divider()
    st.markdown("Built for the Google Gen AI Hackathon.")

# --- App Title and Description ---
st.title(f"Welcome, {artisan_name}!")
st.header("Setu Sangam: Your AI Co-Creator")
st.markdown("Select your craft. Our AI will recommend a synergistic partner and generate a full collaboration proposal to help you innovate and connect.")
st.divider()

# --- Main App Flow ---
st.subheader("1. Tell Us About Your Craft")
artisan_crafts = ["Madhubani Painting", "Jaipur Blue Pottery", "Kutch Lippan Art", "Kalamkari Textile Art", "Bidriware Metal Inlay", "Pattachitra Scroll Painting"]
my_craft = st.selectbox("I am a...", artisan_crafts)

# --- Session State Management ---
if 'recommendation' not in st.session_state:
    st.session_state.recommendation = None
if 'full_concept_en' not in st.session_state:
    st.session_state.full_concept_en = None
if 'full_concept_translated' not in st.session_state:
    st.session_state.full_concept_translated = None
if 'outreach_message' not in st.session_state:
    st.session_state.outreach_message = None

# --- Recommendation Button ---
if st.button("Find My AI Co-Creator", use_container_width=True):
    with st.spinner("Analyzing your craft for the perfect partner..."):
        st.session_state.recommendation = get_collaboration_recommendation(my_craft)
        # Clear all previous concepts
        st.session_state.full_concept_en = None
        st.session_state.full_concept_translated = None
        st.session_state.outreach_message = None

# --- Display Recommendation and Generate Full Concept ---
if st.session_state.recommendation:
    st.success(f"**AI Recommendation:** A great partner for your craft is **{st.session_state.recommendation}**!")
    
    st.subheader("2. Generate the Collaboration Concept")
    if st.button("Generate Full Concept!", use_container_width=True):
        with st.spinner("Dreaming up a new masterpiece..."):
            english_concept = generate_full_concept(my_craft, st.session_state.recommendation)
            st.session_state.full_concept_en = english_concept
            
            if chosen_language != "English":
                with st.spinner(f"Translating to {chosen_language}..."):
                    translated_concept = translate_text(english_concept, chosen_language)
                    st.session_state.full_concept_translated = translated_concept
            else:
                st.session_state.full_concept_translated = None

# --- Display the Full Concept ---
if st.session_state.full_concept_en:
    st.divider()
    st.subheader("Your AI-Generated Proposal")
    
    # Display in tabs if translation exists
    if st.session_state.full_concept_translated:
        tab1, tab2 = st.tabs([chosen_language, "English (Original)"])
        with tab1:
            st.markdown(st.session_state.full_concept_translated)
        with tab2:
            st.markdown(st.session_state.full_concept_en)
    else:
        st.markdown(st.session_state.full_concept_en)

    # --- NEW: The Actionable Outreach Feature ---
    st.divider()
    st.subheader("3. Start the Conversation!")
    st.markdown("Your proposal is ready. Now, let's turn this idea into reality. Generate a personalized message to send to a potential collaborator.")

    if st.button("Create Outreach Message", use_container_width=True):
        with st.spinner("Drafting a professional message..."):
            # Use the English concept for the most creative message
            message = generate_outreach_message(st.session_state.full_concept_en)
            st.session_state.outreach_message = message

if 'outreach_message' in st.session_state and st.session_state.outreach_message:
    with st.expander("View and Copy Your Outreach Message", expanded=True):
        st.markdown(st.session_state.outreach_message)
        st.info("You can now copy this message and send it via WhatsApp or email to a fellow artisan!")
