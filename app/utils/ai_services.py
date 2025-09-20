import os
from google.cloud import texttospeech
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from .prompts import RECOMMENDER_PROMPT, CREATIVE_DIRECTOR_PROMPT, CRAFT_LIST, OUTREACH_MESSAGE_PROMPT, TREND_ANALYSIS_PROMPT


PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION")
vertexai.init(project=PROJECT_ID, location=LOCATION)


def get_market_trends(my_craft):
    """Generates a market trend analysis for a given craft"""
    try:
        model = GenerativeModel("gemini-2.5-flash")
        prompt = f"{TREND_ANALYSIS_PROMPT}{my_craft}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating market trends: {e}")
        return "Could not retrieve market trends at this time."


def get_collaboration_recommendation(my_craft, trends_context):
    """Gets an AI-powered recommendation for a partner craft"""
    try:
        model = GenerativeModel("gemini-2.5-flash")
        filtered_craft_list = CRAFT_LIST.replace(my_craft, "").strip(", ")
        prompt = RECOMMENDER_PROMPT.replace("[MARKET_TRENDS]", trends_context)
        prompt = prompt.replace(CRAFT_LIST, filtered_craft_list)
        prompt += my_craft
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error in recommendation: {e}")
        return "Jaipur Blue Pottery"


def generate_full_concept(craft1, craft2):
    """Generates the full collaboration concept"""
    try:
        model = GenerativeModel("gemini-2.5-flash")
        text_prompt = f"{CREATIVE_DIRECTOR_PROMPT}\nCraft 1: {craft1}\nCraft 2: {craft2}"
        response = model.generate_content(text_prompt)
        return response.text
    except Exception as e:
        print(f"Error in text generation: {e}")
        return f"An error occurred during text generation: {e}"


def translate_text(text_to_translate, target_language):
    """Uses Gemini to translate a block of text"""
    try:
        model = GenerativeModel("gemini-2.5-flash")
        prompt = f"Please translate the following English text to {target_language}. Provide only the translated text...\n\n---\n\n{text_to_translate}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error during translation: {e}")
        return "Translation failed."


def generate_outreach_message(concept_text):
    """Uses Gemini to generate a professional outreach message"""
    try:
        model = GenerativeModel("gemini-2.5-flash")
        prompt = f"{OUTREACH_MESSAGE_PROMPT}\n\n---\n\n{concept_text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error during outreach message generation: {e}")
        return "Failed to generate outreach message."


def generate_audio(text_to_read, language="English"):
    """Generates audio from text"""
    try:
        client = texttospeech.TextToSpeechClient()
        clean_text = text_to_read.replace('**', '').replace('*', '').replace('---', '\n').replace('#', '')
        max_bytes = 4900
        truncated_bytes = clean_text.encode('utf-8')[:max_bytes]
        truncated_text = truncated_bytes.decode('utf-8', 'ignore')

        if len(clean_text) > len(truncated_text):
             last_space = truncated_text.rfind(' ')
             if last_space != -1:
                 truncated_text = truncated_text[:last_space] + "..."

        language_code_map = { "English": "en-IN", "Hindi": "hi-IN", "Bengali": "bn-IN", "Tamil": "ta-IN", "Telugu": "te-IN", "Marathi": "mr-IN", "Kannada": "kn-IN" }
        language_code = language_code_map.get(language, "en-IN")
        synthesis_input = texttospeech.SynthesisInput(text=truncated_text)
        voice = texttospeech.VoiceSelectionParams(language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.FEMALE, name=f"{language_code}-Standard-A")
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
        return response.audio_content
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
