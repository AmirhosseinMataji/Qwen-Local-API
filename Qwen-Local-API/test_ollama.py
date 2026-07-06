import requests

response = requests.post(
    "http://127.0.0.1:8000/chat/stream",
    json={
        "session_id": "test",
        "prompt": "Explain charles dickens most famous book in just one paragraph"
    },
    stream=True,
)

for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
    if chunk:
        print(chunk, end="", flush=True)