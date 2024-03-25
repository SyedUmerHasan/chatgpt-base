from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import openai
import config

app = FastAPI()


class ChatGPTRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    model: str = "gpt-3.5-turbo"


client = openai.OpenAI(
    api_key=config.API_KEY,
)

conversation = [
    {"role": "user", "content": "You are a helpful assistant."},
    {"role": "assistant", "content": "Ok."}
]


@app.post("/chatgpt")
def generate_chatgpt_response(request_data: ChatGPTRequest):
    try:

        conversation.append({"role": "user", "content": f"{request_data.prompt}"})

        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=conversation)

        result = response.choices[0].message.content
        conversation.append({"role": "assistant", "content": f"{result}"})

        return result
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to connect to ChatGPT API: {e}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
