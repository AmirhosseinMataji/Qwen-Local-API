from app.ollama_client import generate_response , stream_response


class LLMService:

    def generate(self, prompt: str) -> str:
        return generate_response(prompt)
    
    def stream(self, prompt):
        return stream_response(prompt)