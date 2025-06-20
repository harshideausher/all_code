import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

vector_store_id = "vs_680f1bf79f3081919b4362573359f9bc"
file_id = "file-XzSmrZoVmPUbWpo6fqxfkf"

def inspiration_quotes(user_query):
    prompt = (
        f"The user is looking for motivational guidance on '{user_query}'. "
        "Using *only* the content from the iyoquotes.txt file, craft a supportive response that includes:\n"
        "- 2-3 relevant motivational quotes from the file that directly address their situation\n"
        "- An empowering reframe of any setback or challenge they mentioned\n"
        "- A brief actionable step they can take to apply this motivation\n"
        "- An affirming statement about their potential for success\n"
        "- A reflective question to help them maintain momentum\n"
        "Keep the tone uplifting, energizing, and authentic—focused on building confidence and resilience.\n"
        "If the user's query is unrelated or unclear, ask them to clarify their request."
        "No external knowledge from you training data , reponse only with file search data information , no external informations"
    )

    file_search_tool = {
        "type": "file_search",
        "vector_store_ids": [vector_store_id],
        "max_num_results": 3,
        "filters": {
            "type": "and",
            "filters": [
                {"type": "eq", "key": "file_id", "value": file_id}
            ]
        }
    }

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt,
        tools=[file_search_tool]
    )
    return response.output_text

# Example queries for testing
"""
I'm feeling discouraged after three rejections in a row
I need motivation to keep going in my business
How do I stay positive when my team isn't growing?
I'm working hard but not seeing results yet
What's a good daily affirmation for network marketers?
I feel like giving up after a bad month
How do successful network marketers stay motivated?
I need a boost of confidence before my presentation
What quote can help me overcome fear of rejection?
How do I motivate myself to make more calls today?
""" 