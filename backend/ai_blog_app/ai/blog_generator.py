from django.conf import settings
from langchain_google_genai import ChatGoogleGenerativeAI
from .agents import get_blogs_agent

def generate_blog_from_transcript(transcription):
    prompt = f"Based on your required tasks. apply it here on this transcript: {transcription}"
    
    blog_agent = get_blogs_agent()
    response = blog_agent.invoke(
        {"messages": [{
        "role": 'user',
        "content": prompt
    }
    ]})
    output = str(response['messages'][-1].content)
    return output
