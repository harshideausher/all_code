import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

vector_store_id = "vs_680f1bf79f3081919b4362573359f9bc"
file_id = "file-Xa855b8QAvJtJJBpEJTBth"

def psychological_support(user_query):
    prompt = (
        f"The user says: '{user_query}'. "
        "You have access *only* to the “Psychological Support in Network Marketing: Emotional Resilience "
        "and Empathy Guide” file. Using *only* the advice, key concepts, and example responses in that file, "
        "craft a tailored, resilience-building answer that includes:\n"
        "- An empathetic acknowledgment of their current emotional state\n"
        "- Reframing any rejection or setback as a learning opportunity\n"
        "- Two concrete resilience-building habits (e.g., daily affirmations, boundary setting)\n"
        "- A self-compassion prompt to counter any self-criticism\n"
        "- Guidance on reaching out to or strengthening their support system\n"
        "- A reminder to focus on long-term growth and celebrate small wins\n"
        "- A reflective question to promote self-insight\n"
        "- A practical tip for managing stress or preventing burnout\n"
        "Keep the tone warm, validating, and empowering—focused entirely on emotional well-being."
        "If the user's query is unrelated or unclear, ask them to clarify their request."
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





