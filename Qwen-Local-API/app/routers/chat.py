from fastapi import APIRouter, HTTPException

from app.schemas import ChatRequest, ChatResponse
from app.ollama_client import generate_response
from app.exceptions import OllamaConnectionError
from app.logger import logger
from app.services.conversation_service import ConversationService
from fastapi.responses import StreamingResponse

conversation_service = ConversationService()

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/", response_model=ChatResponse)
def chat(request: ChatRequest):

    logger.info("Received chat request")

    try:

        answer = conversation_service.chat(
            session_id=request.session_id,
            prompt=request.prompt,
        )

        logger.info("Returning response")

        return ChatResponse(response=answer)

    except OllamaConnectionError:

        logger.exception("LLM service unavailable")

        raise HTTPException(
            status_code=503,
            detail="LLM service is unavailable."
        )

@router.post("/stream")
def stream_chat(request: ChatRequest):

    try:
        return StreamingResponse(
            conversation_service.stream_chat(
                session_id=request.session_id,
                prompt=request.prompt,
            ),
            media_type="text/plain",
        )

    except OllamaConnectionError:
        logger.exception("LLM service unavailable")

        raise HTTPException(
            status_code=503,
            detail="LLM service is unavailable."
        )