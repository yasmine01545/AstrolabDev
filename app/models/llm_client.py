#AI model integration

import openai
from app.prompts.prompt_template import system_prompt
from dotenv import load_dotenv
from groq import Groq
from app.utils.data_cleaning import clean_response
#charger les variables d'environement
load_dotenv()
import google.generativeai as genai
from app.utils.config import GOOGLE_API_KEY,OPENAI_API_KEY,GROQ_API_KEY

gemini_model=None
groq_client = None

#gemini model setup and API key config
if GOOGLE_API_KEY:
  genai.configure(api_key=GOOGLE_API_KEY)
 
# model set Up
  generation_config = {
  "temperature": 0.9,
  "max_output_tokens": 2048,# 1500 word
  "response_mime_type": "text/plain",
  }
#Init te model with the system prompt
  gemini_model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",#gemini-1.5-flash"
  generation_config=generation_config,
  system_instruction=[system_prompt],
)


if OPENAI_API_KEY:
  openai.api_key=OPENAI_API_KEY

  

if GROQ_API_KEY:
    try:
        groq_client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        print(" Failed to initialize Groq client:", e)
print(groq_client )

def generate_with_fallback(prompt: str) -> str:
        # Check if any API keys are available
    if not any([groq_client, gemini_model, OPENAI_API_KEY]):
        raise Exception("No valid LLM API keys found.")
    # Try llama 
    if groq_client:
        try:
            print("Using LLaMA 3 (Groq)...")
            response = groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=1024,
                top_p=1,
                stream=False
            )
            return clean_response(response.choices[0].message.content)
        except Exception as e:
            print(" Groq/LLaMA 3 failed, falling back to Gemini...", e)
            raise Exception(f"Groq/LLaMA 3 error: {str(e)}")


    #try gemini
    if gemini_model:
        try:
            print(" Using Gemini model...")
            response = gemini_model.generate_content([prompt])
            return clean_response(response.text)
        except Exception as e:
            print("[ Gemini error fallback to OpenAI]", e)
            raise Exception(f"Gemini error: {str(e)}")

    # Try OpenAI
    if OPENAI_API_KEY:
        try:
            print(" Using OpenAI GPT model...")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return clean_response(response.choices[0].message["content"])
        except Exception as e:
            print("[ OpenAI error]", e)
            raise Exception(f"OpenAI error: {str(e)}")

    raise Exception("all providers failed. Verify Your API")