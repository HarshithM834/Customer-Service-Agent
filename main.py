# FastAPI backend with all endpoints

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services import classify_intent, get_context_from_perplexity, generate_response, text_to_speech
from agents import AgentRouter
import logging
from typing import Optional
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="AI Customer Support Agent",
    description="Multi-agent customer support system",
    version="1.0.0"
)


interaction_log = []


router = AgentRouter()



class CustomerMessage(BaseModel):
    """Customer message request"""
    message: str
    customer_id: str = "demo_customer"


class AgentResponse(BaseModel):
    """Agent response with metadata"""
    agent_type: str
    response: str
    context_used: str
    cost_estimate: float


class InteractionLog(BaseModel):
    """Single interaction log entry"""
    timestamp: str
    customer_id: str
    customer_message: str
    agent_type: str
    response: str
    context: str


@app.post("/chat", response_model=AgentResponse)
async def chat(msg: CustomerMessage) -> AgentResponse:
    try:
        logger.info(f"Received: {msg.message[:50]}...")
        
        intent = classify_intent(msg.message)
        logger.info(f"Classified as: {intent}")
        
        context = get_context_from_perplexity(msg.message)
        logger.info(f"Context retrieved: {context[:50]}...")
        
        agent_name, response = router.route(intent, msg.message)
        logger.info(f"Generated response from {agent_name}")
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "customer_id": msg.customer_id,
            "customer_message": msg.message,
            "agent_type": intent,
            "response": response,
            "context": context[:200]
        }
        interaction_log.append(log_entry)
        
        cost_estimate = 0.023  # Rough estimate per interaction
        
        return AgentResponse(
            agent_type=intent,
            response=response,
            context_used=context[:200],
            cost_estimate=cost_estimate
        )
    
    except Exception as e:
        logger.error(f"Error in /chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/voice")
async def voice_chat(msg: CustomerMessage) -> dict:
    """
    Voice chat endpoint: returns both text response and voice availability
    """
    try:
        logger.info(f"Voice request received: {msg.message[:50]}...")
        
        response = await chat(msg)
        
        tts_result = text_to_speech(response.response)
        
        return {
            "text_response": response.response,
            "agent_type": response.agent_type,
            "audio_available": tts_result["success"],
            "audio_message": tts_result["message"],
            "cost_estimate": response.cost_estimate
        }
    
    except Exception as e:
        logger.error(f"Error in /voice: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/logs")
async def get_logs() -> dict:
    logger.info(f"Logs requested: {len(interaction_log)} interactions")
    return {
        "total_interactions": len(interaction_log),
        "logs": interaction_log
    }


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", \"service\": "AI Customer Support Agent"}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting AI Customer Support Agent backend")
    uvicorn.run(app, host="0.0.0.0", port=8000)
