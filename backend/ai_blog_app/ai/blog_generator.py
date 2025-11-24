from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from .agents import get_blogs_agent
from .llms import get_ai_model

def generate_blog_from_transcript(transcription, length='medium'):
    prompt = f"Based on your required tasks. apply it here on this transcript: {transcription}"

    blog_agent = get_blogs_agent(length=length)
    response = blog_agent.invoke(
        {"messages": [{
        "role": 'user',
        "content": prompt
    }
    ]})
    output = {
        "generated_text": str(response['messages'][-1].content),
        "model": get_ai_model().model
    }
    return output


