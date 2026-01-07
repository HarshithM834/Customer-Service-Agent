# LLM Integrations for Sales Agent

import google.generativeai as genai
import requests
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(level = logging.INFO, format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    logger.warning("GEMINI_API_KEY not found in environment variables")

if gemini_api_key:
    genai.configure(api_key = gemini_api_key)
    logger.info("Gemini API key loaded successfully")
    gemini_model = genai.GenerativeModel('gemini-2.0-flash-lite')
else:
    gemini_model = None

perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")

def classify_sales_intent(customer_message: str) -> str: 
    if not gemini_model:
        return "other"
        
    try:
        response = gemini_model.generate_content(
            f"Classify this sales-related customer message as ONE of: new_customer, upgrade, device_inquiry, promotion, other."
            f"Focus on the primary sales intent only."
            f"Reply with ONLY the classification (one word). \n\n"
            f"Message: {customer_message}"
        )

        classification = response.text.strip().lower()
        valid_intents = ["new_customer", "upgrade", "device_inquiry", "promotion", "other"]
        if classification in valid_intents:
            logger.info(f"Classified as: {classification}")
            return classification

        else:
            logger.warning(f"Invalid classification: {classification}, defaulting to 'other'")
            return "other"
        
    except Exception as e:
        logger.error(f"Intent Classification Failed: {e}")
        return "other"


def get_sales_context(query: str) -> str:
    try:
        if perplexity_api_key:
            try:
                response = requests.post(
                    "https://api.perplexity.ai/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {perplexity_api_key}"},
                    json={
                        "model": "sonar",
                        "messages": [
                            {
                                "role": "user",
                                "content": f"Provide general factual information about typical telecom plans or devices regarding: {query}\n"
                                          f"Focus on specs, features, or general market offerings.\n"
                                          f"Keep response concise (2-3 sentences max)."
                            }
                        ]
                    }
                )

                if response.status_code == 200:
                    result = response.json()
                    context = result.get("choices", [{}]).get("message", {}).get("content", "")
                    logger.info("Context retrieved from Perplexity")
                    return context[:500]

            except Exception as e:
                logger.warning(f"Perplexity failed, falling back to Gemini: {e}")
        
        if gemini_model:
            response = gemini_model.generate_content(
                f"Provide general factual information about typical telecom plans or devices regarding: {query}\n"
                f"Focus on specs and features.\n"
                f"Keep response concise (2-3 sentences max)."
            )

            context = response.text
            logger.info("Context retrieved from Gemini (fallback)")
            return context[:500]
        
        return "Context unavailable."
    
    except Exception as e:
        logger.error(f"Context retrieval failed: {e}")
        return "Unable to retrieve context."


def generate_sales_response(agent_type: str, customer_message: str, context: str) -> str:
    if not gemini_model:
        return "I apologize, I am currently offline."

    system_prompts = {
        "new_customer": "You are a New Customer Specialist. Welcome the user and highlight the benefits of joining our service. Be enthusiastic and persuasive.",
        "upgrade": "You are an Upgrade Specialist. Help existing customers find better plans or newer devices. Focus on value and loyalty benefits.",
        "device_inquiry": "You are a Device Expert. Provide detailed, accurate info about smartphones, tablets, and accessories. Compare features if asked.",
        "promotion": "You are a Promotions Specialist. Explain current deals, bundles, and limited-time offers clearly. Create a sense of urgency.",
        "other": "You are a General Sales Agent. Assist with any sales-related inquiries professionally and persuasively."
    }
    
    system_prompt = system_prompts.get(agent_type, system_prompts["other"])
    
    try:
        response = gemini_model.generate_content(
            f"{system_prompt}\n\n"
            f"Context (General Info): {context}\n\n"
            f"Customer message: {customer_message}\n\n"
            f"Provide a helpful, persuasive response."
        )

        logger.info(f"Generated response for {agent_type} agent")
        return response.text

    except Exception as e:
        logger.error(f"Response generation failed: {e}")
        return "I apologize, I'm unable to process that request right now. Please try again later."


def text_to_speech(text: str) -> dict:
    try:
        elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        if not elevenlabs_api_key:
            logger.warning("ELEVENLABS_API_KEY not found, TTS unavailable")
            return {"success": False, "message": "API key not configured"}
        
        from elevenlabs.client import ElevenLabs
        client = ElevenLabs(api_key=elevenlabs_api_key)
        audio = client.generate(
            text=text,
            voice="Rachel",
            model="eleven_monolingual_v1"
        )
        logger.info("Text-to-speech conversion successful")
        return {"success": True, "message": "Audio generated", "audio": audio}
        
    except Exception as e:
        logger.warning(f"Text-to-speech failed: {e}")
        return {"success": False, "message": str(e)}
