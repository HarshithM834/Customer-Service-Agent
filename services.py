# LLM Integrations

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
    raise ValueError("GEMINI_API_KEY not found in environment variables")

genai.configure(api_key = gemini_api_key)
logger.info("Gemini API key loaded successfully")

gemini_model = genai.GenerativeModel('gemini-2.0-flash-lite')

perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")

def classify_intent(customer_message: str) -> str: 
    try:
        response = gemini_model.generate_content(
            f"Classify this customer message as ONE of: billing, sales, technical_support, other."
            f"Focus on the primary intent only."
            f"Reply with ONLY the classification (one word). \n\n"
            f"Message: {customer_message}"
        )

        classification = response.text.strip().lower()
        valid_intents = ["billing", "sales", "technical_support", "other"]
        if classification in valid_intents:
            logger.info(f"Classified as: {classification}")
            return classification

        else:
            logger.warning(f"Invalid classification: {classification}, defaulting to 'other'")
            return "other"
        
    except Exception as e:
        logger.error(f"Intent Classification Failed: {e}")
        return "other"


def get_context_from_perplexity(query: str) -> str:
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
                                "content": f"Provide accurate information about: {query}\n"
                                          f"Focus on facts, not recommendations.\n"
                                          f"Keep response concise (2-3 sentences max).\n"
                                          f"Include relevant details."
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
        
        response = gemini_model.generate_content(
            f"Provide accurate information about: {query}\n"
            f"Focus on facts, not recommendations.\n"
            f"Keep response concise (2-3 sentences max).\n"
            f"Include relevant details like account status, plan details, policies if applicable."
        )

        context = response.text
        logger.info("Context retrieved from Gemini (fallback)")
        return context[:500]
    
    except Exception as e:
        logger.error(f"Context retrieval failed: {e}")
        return "Unable to retrieve context."


def generate_response(agent_type: str, customer_message: str, context: str) -> str:
    system_prompts = {
        "billing": "You are a billing support agent for a major telecom provider. Be helpful, professional, and concise. Explain charges clearly and offer solutions.",
        "sales": "You are a sales agent for a major telecom provider. Help customers understand plans and benefits. Be persuasive but honest.",
        "technical_support": "You are a technical support agent for a major telecom provider. Help customers troubleshoot issues. Provide clear, step-by-step guidance.",
        "other": "You are a customer service agent for a major telecom provider. Help the customer efficiently and professionally."
    }
    
    system_prompt = system_prompts.get(agent_type, system_prompts["other"])
    
    try:
        response = gemini_model.generate_content(
            f"{system_prompt}\n\n"
            f"Customer context: {context}\n\n"
            f"Customer message: {customer_message}\n\n"
            f"Provide a helpful, professional response."
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

