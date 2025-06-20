import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

vector_store_id = "vs_680f1bf79f3081919b4362573359f9bc"
file_id = "file-8vk4cz9u6oEvG7GhJyisUD"

def discovery_session(user_query):
    prompt = (
        f"The user says: '{user_query}'. "
        "You have access to a file via the file_search tool, which contains the specific wording and structure for the IYOVIA Coach Pro discovery session. "
        "Before proceeding, check the user's query for any discovery details they might have already provided, such as their name, location, experience in network marketing, etc. "
        "If such information is present, acknowledge it and proceed to the next relevant question without asking for it again. "
        "For example, if they've shared their name, you might say, 'Great to meet you, [Name]! Let's move on to the next question.' "
        "Using exclusively the wording and structure from that file, craft a conversational reply that:\n"
        "- Opens with a single agreement question inviting the user to start the discovery session\n"
        "- Asks only the next relevant discovery question (based on what information is still needed) to begin, ensuring questions are presented one at a time\n"
        "- Briefly summarizes the four skill-rating tiers (Basic 1–30, Intermediate 31–70, Advanced 71–90, Ultra Professional 91–100) in a natural way, without disrupting the flow\n"
        "- Ends with a reflective prompt asking if they'd like to continue\n"
        "Do not reveal any internal step numbers or process labels—present everything as a seamless dialogue."
        "No external knowledge from you training data , reponse only with file search data information , no external informations"
    )

    file_search_tool = {
        "type": "file_search",
        "vector_store_ids": [vector_store_id],
        "max_num_results": 1,
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

# Example questions for testing
"""

"Can you give me an overview of the 300 series in the IBO Resources Hub?",
"List all the video codes and titles in the 300 series, please.",
"How many videos are there in the 300 series, and which ones are marked done?",
"What are the Y/N status indicators for each 300 series video?",
"Which 300 series video should I start with first?",
"I’d like the full list of 300 series codes, titles, and done status.",
"Tell me the titles of all 300 series videos and their completion status.",
"Give me the total count and breakdown of the 300 series videos.",
"Which video in the 300 series is best for setting goals?",
"Provide a concise list of 300-series video codes, titles, and Y/N flags.",
"What actionable recommendation do you have for a first-timer in the 300 series?",
"I need a reflective question to help me plan my learning for the 300 series.",
"Show me all IBO 301–309 titles with their completed (Y/N) markers.",
"How many videos are in the 300 series, and which ones aren’t done yet?",
"Which 300 series video would you suggest starting with, and why?",
"Give me a formatted list of 300 series videos and their status indicators.",
"What’s the first video I should watch in the 300 series to maximize growth?",
"List 300 series videos, count them, note Y/N, and then recommend one to begin.",
"I’m looking for a reflective plan question after seeing the 300 series list.",
"Outline the 300 series videos with their Y/N status and a roadmap question",
"
"""




