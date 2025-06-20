import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

vector_store_id = "vs_680f1bf79f3081919b4362573359f9bc"
file_id = "file-CA5tm6FZ6NDpXGa38AMc67"

def pay_plan_info(user_query):
    prompt = (
        f"The user is looking for information on '{user_query}' related to IYOVIA Resources and Tools. "
        "You have access *only* to the iyoviacompplan2024.pdf file. Using *only* its content "
        "and formatting conventions, craft a response that includes:\n"
        "- A description of the specific resource, tool, or system the user is inquiring about\n"
        "- How to access or utilize this resource (links, platforms, login procedures)\n"
        "- Any specific functionality or features that address the user's query\n"
        "- Best practices for implementation within their business\n"
        "- Relevant integration points with other IYOVIA systems or processes\n"
        "- One actionable tip for maximizing value from this resource\n"
        "- A follow-up question to help the user apply this information effectively\n"
        "Keep the tone clear, instructional, and align with the document's formatting style."
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

# Example questions for testing
"""
Where can I find the IBO back office login page?
What marketing materials are available for social media promotion?
How do I access the team communication tools?
What training resources are available for new IBOs?
Is there a mobile app for IYOVIA business management?
How do I set up automated follow-ups with prospects?
What CRM tools are integrated with the IYOVIA system?
Where can I find presentation templates for opportunity meetings?
How do I track my team's performance and activity?
What customer service channels are available for product support?
Are there tools for creating personalized marketing content?
How do I access the replicated website for my business?
What reporting features are available to track my commissions?
Is there a resource library for product information?
How do I order business cards or branded merchandise?
What compliance tools are available to ensure my marketing is compliant?
Where can I find the event calendar for corporate trainings?
How do I register new team members on the platform?
What resources are available for international market expansion?
Is there a recognition program management tool?
"""


