import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_blog_app.settings')
django.setup()

from ai_blog_app.ai.agents import agent

# Test with a sample transcription
sample_transcription = """
So today I'm going to show you, um, how to make the best chocolate cake ever.
Like, it's really amazing. So first, you know, you need to preheat your oven to 350 degrees.
Then, uh, you mix the flour, sugar, and cocoa powder together. Make sure you sift it.
After that, you add the eggs and milk and just mix it all up. Pour it in a pan and bake for 30 minutes.
Trust me, this is like the best cake you'll ever make!
"""

response = agent.invoke({"messages": [{"role": "user", "content": sample_transcription}]})
print(response)
