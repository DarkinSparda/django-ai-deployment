from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI

api = settings.GEMINI_API_KEY
def get_model_api_key():
    return api

def get_ai_model(model='gemini-2.5-flash-lite', max_tokens=150):
    return ChatGoogleGenerativeAI(
        model=model,
        api_key=api,
        temperature=1,
        max_tokens=max_tokens,
    )