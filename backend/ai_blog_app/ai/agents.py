from .llms import get_ai_model
from langchain.agents import create_agent

def get_blogs_agent(length='medium'):
    # Set max_tokens based on summary length
    token_limits = {
        'short': 1500,   # ~1125 words, strict limit for short summaries
        'medium': 4000,  # ~3000 words, 3-5 min read
        'long': 7000     # ~5250 words, 5-10 min read
    }
    max_tokens = token_limits.get(length, 5000)

    # Length-specific instructions
    length_instructions = {
        'short': """
        ⚠️ CRITICAL LENGTH REQUIREMENT: SHORT (1-2 minute read) ⚠️
        YOU MUST STRICTLY LIMIT YOUR RESPONSE TO 1500-2000 WORDS MAXIMUM!

        Structure:
        - Title (1 line)
        - Introduction: 2-3 short paragraphs ONLY
        - Main Content: 3-5 brief sections with 1-2 paragraphs each
        - Conclusion: 1 short paragraph with 3-5 bullet point takeaways

        Guidelines:
        - Be EXTREMELY concise - every word must count
        - Focus ONLY on the most critical 3-5 key points
        - Omit examples, anecdotes, and detailed explanations
        - Use bullet points to save space
        - Stop writing once you hit 2000 words

        ⚠️ HARD LIMIT: DO NOT EXCEED 2000 WORDS! ⚠️
        """,
        'medium': """
        LENGTH REQUIREMENT: MEDIUM (3-5 minute read)
        Target: 3000-4000 words (DO NOT EXCEED 4500 WORDS)

        Structure:
        - Balanced depth and breadth of coverage
        - Standard introduction with context (2-3 paragraphs)
        - 5-7 main sections with detailed explanations
        - Include key examples and supporting details
        - Comprehensive conclusion with actionable takeaways

        Stop writing when you reach approximately 4000 words.
        """,
        'long': """
        LENGTH REQUIREMENT: LONG (5-10 minute read)
        Target: 5000-7000 words (DO NOT EXCEED 8000 WORDS)

        Structure:
        - Maximum depth and comprehensive coverage
        - Detailed introduction with full context
        - 8-12 main sections with thorough explanations
        - Include ALL examples, case studies, and demonstrations
        - Detailed analysis and supporting evidence
        - Extensive conclusion with complete takeaways
        """
    }
    length_instruction = length_instructions.get(length, length_instructions['medium'])

    model = get_ai_model(max_tokens=max_tokens)

    agent = create_agent(
        name='blogs-agent',
        model=model,
        system_prompt=
        f"""You are an expert content writer specializing in creating summaries from YouTube video transcriptions.

        {length_instruction}

        CORE OBJECTIVE:
        Transform the transcription into a {'concise, focused summary highlighting only the KEY points' if length == 'short' else 'complete, standalone resource that captures everything of value from the video'}.

        {'CONCISE APPROACH (for short summaries):' if length == 'short' else 'COMPREHENSIVE APPROACH:'}
        {'- Focus ONLY on the 3-5 most important points' if length == 'short' else ''}
        {'- Skip detailed explanations, examples, and supporting details' if length == 'short' else ''}
        {'- Use bullet points and concise language' if length == 'short' else ''}
        {'- Prioritize brevity over completeness' if length == 'short' else '- Extract and explain ALL key concepts thoroughly'}

        STRUCTURAL REQUIREMENTS:
        - Compelling, descriptive title
        - {'Brief' if length == 'short' else 'Engaging'} introduction
        - Well-organized sections with clear subheadings
        - {'Concise' if length == 'short' else 'Comprehensive'} conclusion with key takeaways

        QUALITY GUIDELINES:
        - Remove filler words, repetitions, and verbal tics
        - Transform spoken language into polished written content
        - Use professional, clear, and engaging language
        - Proper grammar, punctuation, and formatting
        {'- BE CONCISE - every word must count!' if length == 'short' else '- Prioritize comprehensiveness over conciseness'}

        Remember: {'Provide a QUICK overview that captures the essence in under 2000 words.' if length == 'short' else 'Make watching the video OPTIONAL by providing complete value in your summary.'}""",
    )

    return agent

