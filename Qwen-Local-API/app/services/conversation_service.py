from app.services.llm_service import LLMService

llm_service = LLMService()


class ConversationService:
    def __init__(self):
        self.sessions = {}

    def create_session(self, session_id: str):
        if session_id not in self.sessions:
            self.sessions[session_id] = []

    def build_prompt(self, session_id: str) -> str:
        history = self.sessions[session_id]

        prompt = ""

        for message in history:
            prompt += f"{message['role']}: {message['content']}\n"

        prompt += "assistant:"

        return prompt

    def chat(self, session_id: str, prompt: str) -> str:
        self.create_session(session_id)

        # ذخیره پیام کاربر
        self.sessions[session_id].append(
            {
                "role": "user",
                "content": prompt
            }
        )

        # گرفتن پاسخ از مدل
        full_prompt = self.build_prompt(session_id)

        answer = llm_service.generate(full_prompt)

        # ذخیره پاسخ مدل
        self.sessions[session_id].append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        return answer
    
    def stream_chat(self, session_id: str, prompt: str):

        self.create_session(session_id)

        self.sessions[session_id].append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        full_prompt = self.build_prompt(session_id)

        answer = ""

        for token in llm_service.stream(full_prompt):

            answer += token

            yield token

        self.sessions[session_id].append(
            {
                "role": "assistant",
                "content": answer,
            }
        )