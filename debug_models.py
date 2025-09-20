#legacy debugging script

import vertexai
import google.generativeai as genai

PROJECT_ID = "formal-net-471916-g9" 
LOCATION = "asia-south1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

print("Checking available models for 'generateContent'")

for model in genai.list_models():
  if 'generateContent' in model.supported_generation_methods:
    print(model.name)

print("Check complete")
