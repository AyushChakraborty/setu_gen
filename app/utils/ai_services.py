# app/utils/ai_services.py

import os
import google.generativeai as genai
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image
from .prompts import RECOMMENDER_PROMPT, CREATIVE_DIRECTOR_PROMPT, CRAFT_LIST, OUTREACH_MESSAGE_PROMPT
from dotenv import load_dotenv
load_dotenv()

# --- UNIFIED AUTHENTICATION SETUP ---
# This is the new section that fixes the error.
# It initializes the Vertex AI SDK, which automatically handles authentication
# for both the Vertex AI (Imagen) and Generative Language (Gemini) libraries.

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION")
vertexai.init(project=PROJECT_ID, location=LOCATION)
# --- END OF NEW SECTION ---


def get_collaboration_recommendation(my_craft):
    """
    Gets an AI-powered recommendation for a partner craft.
    """
    try:
        # We need to remove the user's own craft from the list of possibilities
        filtered_craft_list = CRAFT_LIST.replace(my_craft, "").strip(", ")
        
        prompt = RECOMMENDER_PROMPT.replace(CRAFT_LIST, filtered_craft_list) + my_craft
        
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        
        # Clean up the response to get just the craft name
        recommended_craft = response.text.strip()
        return recommended_craft
    except Exception as e:
        print(f"Error in recommendation: {e}")
        # Fallback in case of an error
        return "Jaipur Blue Pottery"


# In app/utils/ai_services.py

# ... (keep all the other code, just replace this one function) ...

def generate_full_concept(craft1, craft2):
    """
    Generates the full collaboration concept including text and an AI image.
    Handles image generation errors gracefully.
    """
    generated_text = "Error: Could not generate the text concept."
    img_bytes = None

    try:
        # --- Step 1: Generate the Text Concept using Gemini ---
        text_prompt = f"{CREATIVE_DIRECTOR_PROMPT}\nCraft 1: {craft1}\nCraft 2: {craft2}"
        text_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        text_response = text_model.generate_content(text_prompt)
        generated_text = text_response.text
    except Exception as e:
        print(f"Error in text generation: {e}")
        # Return the error in the text part if this fails
        return f"An error occurred during text generation: {e}", None

    # try:
    #     # --- Step 2: Generate the Image using Imagen ---
    #     image_prompt_line = [line for line in generated_text.split('\n') if line.startswith("A photorealistic product shot of")]
    #     if not image_prompt_line:
    #         image_prompt = f"A photorealistic product shot of a beautiful fusion between {craft1} and {craft2}."
    #     else:
    #         image_prompt = image_prompt_line[0]

    #     image_model = GenerativeModel("imagegeneration@005") 
    #     image_response = image_model.generate_content([image_prompt])
    #     img_bytes = image_response.candidates[0].content.to_bytes()
    # except Exception as e:
    #     print(f"Error in image generation: {e}")
    #     # If image generation fails, we'll return the text but no image.
    #     # This is our graceful fallback.
    #     img_bytes = None
            
    return generated_text #, img_bytes


def translate_text(text_to_translate, target_language):
    """
    Uses Gemini to translate a block of text to a target language.
    """
    try:
        #better to use gemini again for the translation rather than google translates api say, 
        #as the translation then would be more literal than creative, which we need
        #it does end up using more tokens but thats ok in this context
        prompt = f"Please translate the following English text to {target_language}. Provide only the translated text, without any additional comments or introductions:\n\n---\n\n{text_to_translate}"
        
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        
        return response.text.strip()
    except Exception as e:
        print(f"Error during translation: {e}")
        return "Translation failed."

def generate_outreach_message(concept_text):
    """
    Uses Gemini to generate a professional outreach message based on a concept.
    """
    try:
        prompt = f"{OUTREACH_MESSAGE_PROMPT}\n\n---\n\n{concept_text}"
        
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        
        return response.text.strip()
    except Exception as e:
        print(f"Error during outreach message generation: {e}")
        return "Failed to generate outreach message."
