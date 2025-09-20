import streamlit as st
from utils.ai_services import (
    get_market_trends,
    get_collaboration_recommendation, 
    generate_full_concept, 
    translate_text, 
    generate_outreach_message,
    generate_audio
)

st.set_page_config(
    page_title="Setu Sangam",
    page_icon="🎨",
    layout="wide"
)

with st.sidebar:
    st.title("🎨 Artisan Profile")
    artisan_name = st.text_input("What is your name?", "Artisan")
    languages = ["English", "Hindi", "Bengali", "Tamil", "Telugu", "Marathi", "Kannada"]
    chosen_language = st.selectbox("What is your preferred language?", languages)
    st.divider()
    st.markdown("Built for the Google Gen AI Hackathon.")
    st.sidebar.image("app/assets/genai.png")

st.title(f"✨ Welcome, {artisan_name}!")
st.header("Setu Sangam: Your AI Strategy Co-Pilot")
st.markdown("From market trends to collaborative concepts, let's build a winning strategy for your craft.")
st.divider()


st.session_state.setdefault('market_trends_en', None)
st.session_state.setdefault('market_trends_translated', None)
st.session_state.setdefault('recommendation', None)
st.session_state.setdefault('full_concept_en', None)
st.session_state.setdefault('full_concept_translated', None)
st.session_state.setdefault('outreach_message', None)



with st.container(border=True):
    st.subheader("Step 1: Discover What's Selling")
    artisan_crafts = ["Madhubani Painting", "Jaipur Blue Pottery", "Kutch Lippan Art", "Kalamkari Textile Art", "Bidriware Metal Inlay", "Pattachitra Scroll Painting", "Channapatna Toys"]
    my_craft = st.selectbox("First, tell us about your craft:", artisan_crafts)

    if st.button("📈 Analyze Market Trends", use_container_width=True):
        with st.spinner("Researching current market trends..."):
            english_trends = get_market_trends(my_craft)
            st.session_state.market_trends_en = english_trends
            
            if chosen_language != "English":
                with st.spinner(f"Translating trends to {chosen_language}..."):
                    st.session_state.market_trends_translated = translate_text(english_trends, chosen_language)
            else:
                st.session_state.market_trends_translated = None
            
            st.session_state.recommendation = None
            st.session_state.full_concept_en = None
            st.session_state.full_concept_translated = None
            st.session_state.outreach_message = None

if st.session_state.market_trends_en:
    with st.container(border=True):
        st.subheader("AI Market Trend Report")
        if st.session_state.market_trends_translated:
            tab1, tab2 = st.tabs([chosen_language, "English (Original)"])
            with tab1:
                st.markdown(st.session_state.market_trends_translated)
                if st.button(f"🔊 Read Trends in {chosen_language}", key="read_trends_translated"):
                    audio_bytes = generate_audio(st.session_state.market_trends_translated, chosen_language)
                    if audio_bytes: st.audio(audio_bytes, format="audio/mp3")
            with tab2:
                st.markdown(st.session_state.market_trends_en)
                if st.button("🔊 Read Trends in English", key="read_trends_english"):
                    audio_bytes = generate_audio(st.session_state.market_trends_en, "English")
                    if audio_bytes: st.audio(audio_bytes, format="audio/mp3")
        else:
            st.markdown(st.session_state.market_trends_en)
            if st.button("🔊 Read Trends in English", key="read_trends_english_main"):
                audio_bytes = generate_audio(st.session_state.market_trends_en, "English")
                if audio_bytes: st.audio(audio_bytes, format="audio/mp3")
    
    with st.container(border=True):
        st.subheader("Step 2: Find Your AI Co-Creator")
        if st.button("🤝 Find a Collaborator Based on Trends", use_container_width=True):
            with st.spinner("Finding the perfect strategic partner..."):
                st.session_state.recommendation = get_collaboration_recommendation(my_craft, st.session_state.market_trends_en)
                st.session_state.full_concept_en = None
                st.session_state.full_concept_translated = None
                st.session_state.outreach_message = None

if st.session_state.recommendation:
    st.success(f"**AI Recommendation:** Based on current trends, a great partner for your craft is **{st.session_state.recommendation}**!")
    
    with st.container(border=True):
        st.subheader("Step 3: Generate the Collaboration Concept")
        if st.button("Generate Full Concept!", use_container_width=True):
            with st.spinner("Dreaming up a new masterpiece..."):
                english_concept = generate_full_concept(my_craft, st.session_state.recommendation)
                st.session_state.full_concept_en = english_concept
                if chosen_language != "English":
                    with st.spinner(f"Translating to {chosen_language}..."):
                        st.session_state.full_concept_translated = translate_text(english_concept, chosen_language)
                else:
                    st.session_state.full_concept_translated = None

if st.session_state.full_concept_en:
    with st.container(border=True):
        st.subheader("Your AI-Generated Proposal")
        if st.session_state.full_concept_translated:
            tab1, tab2 = st.tabs([chosen_language, "English (Original)"])
            with tab1:
                st.markdown(st.session_state.full_concept_translated)
                if st.button(f"🔊 Read Aloud in {chosen_language}", key="read_proposal_translated"):
                    audio_bytes = generate_audio(st.session_state.full_concept_translated, chosen_language)
                    if audio_bytes: st.audio(audio_bytes, format="audio/mp3")
            with tab2:
                st.markdown(st.session_state.full_concept_en)
                if st.button("🔊 Read Aloud in English", key="read_proposal_english"):
                    audio_bytes = generate_audio(st.session_state.full_concept_en, "English")
                    if audio_bytes: st.audio(audio_bytes, format="audio/mp3")
        else:
            st.markdown(st.session_state.full_concept_en)
            if st.button("🔊 Read Aloud in English", key="read_proposal_english_main"):
                audio_bytes = generate_audio(st.session_state.full_concept_en, "English")
                if audio_bytes: st.audio(audio_bytes, format="audio/mp3")
    
    with st.container(border=True):

        st.subheader("Step 4: Start the Conversation!")
        if st.button("✍️ Create Outreach Message", use_container_width=True):
            with st.spinner("Drafting a professional message..."):
                st.session_state.outreach_message = generate_outreach_message(st.session_state.full_concept_en)

if st.session_state.outreach_message:
    with st.expander("View Your Outreach Message", expanded=True):
        st.markdown(st.session_state.outreach_message)
        st.info("You can now manually copy this message to start a real-world collaboration!")
