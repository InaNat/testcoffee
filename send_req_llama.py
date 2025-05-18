import base64
from together import Together

client = Together(api_key="0e05bfaf5d5aaa8ed5fa476ff9aa303bb6667fa56c755db8ebee6aa4224ee1ae")

def encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# replace with your image file
b64 = encode_image("/Users/yalcintur/8vchackathon/fig-vs-14.png")

response = client.chat.completions.create(
    model="meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What are some fun things to do here?"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
        ]
    }]
)

print(response.choices[0].message.content)
