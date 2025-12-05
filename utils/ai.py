import os
from groq import Groq
import replicate

# تنظیمات API — تو باید این‌ها رو در Render تنظیم کنی
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

client = Groq(api_key=GROQ_API_KEY)

def generate_text(prompt: str, style="business") -> str:
    system = "You are a professional AI assistant."
    if style == "islamic_minimal":
        system = "Write in a minimal, symbolic, Islamic-inspired tone with spiritual light metaphors."
    chat = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}]
    )
    return chat.choices[0].message.content

def summarize_text(text: str) -> str:
    return generate_text(f"Summarize this in 3 lines:\n{text}")

def generate_image(prompt: str) -> str:
    if not REPLICATE_API_TOKEN:
        return "Image API not configured."
    output = replicate.run(
        "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712102c19081e2701f9e7f6869e51a3b24",
        input={"prompt": prompt + ", minimalist, golden light, symbolic, Islamic art style"}
    )
    return output[0]  # URL تصویر