import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

vector_store_id = "vs_680f1bf79f3081919b4362573359f9bc"
rankq_file_id = "file-H9uZm8tgMaGSWKVAVHtExE"
backoffice_file_id = "file-H4eaUbAs57iYsWvDH8n7xp"

def faq_queries(user_query):
    # Determine which file to use based on the user query
    if "rankq" in user_query.lower() or "rank questions" in user_query.lower():
        file_id = rankq_file_id
        instruction = "list all questions from the rankq.txt file. Format them as a numbered list."
    elif "backoffice" in user_query.lower():
        file_id = backoffice_file_id
        instruction = "list all questions that users can ask about the backoffice functionality based on the backoffice.txt file. Format them as a numbered list."
    else:
        # Default to checking both files
        file_id = None
        instruction = "Based on the query, provide relevant information from either the rankq.txt or backoffice.txt files."

    prompt = (
        f"The user asks: '{user_query}'. {instruction}\n\n"
        "If the user is asking to see all questions or what they can ask about a topic, "
        "present the information in a clear, organized way with:\n"
        "- A brief introduction explaining what the list contains\n"
        "- A numbered list of questions/topics they can ask about\n"
        "- Group similar questions together if appropriate\n"
        "- A closing statement inviting them to ask any of these questions\n\n"
        "If they're asking a specific question about rank or backoffice, answer directly "
        "using only information from the knowledge files."
        "No external knowledge from you training data , reponse only with file search data information , no external informations"
    )

    # Create appropriate file search tool
    if file_id:
        # Search in specific file
        file_search_tool = {
            "type": "file_search",
            "vector_store_ids": [vector_store_id],
            "max_num_results": 5,
            "filters": {
                "type": "and",
                "filters": [
                    {"type": "eq", "key": "file_id", "value": file_id}
                ]
            }
        }
    else:
        # Search in both files
        file_search_tool = {
            "type": "file_search",
            "vector_store_ids": [vector_store_id],
            "max_num_results": 5,
            "filters": {
                "type": "or",
                "filters": [
                    {"type": "eq", "key": "file_id", "value": rankq_file_id},
                    {"type": "eq", "key": "file_id", "value": backoffice_file_id}
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
Show me all questions from rankq.txt
What questions can I ask you about my backoffice?
What can I ask about rank progression?
Tell me the common questions about backoffice
What rank questions are available?
Help me understand what information I can get about my rank
What backoffice features can you explain to me?
""" 