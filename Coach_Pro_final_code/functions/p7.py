import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

vector_store_id = "vs_680f1bf79f3081919b4362573359f9bc"
file_id = "file-CA5tm6FZ6NDpXGa38AMc67"

def rank_progression(user_query):
    prompt = (
        f"The user wants information about '{user_query}' related to IYOVIA's rank progression, compensation plan, and payout structure. "
        "Using ONLY the content from the iyoviacompplan2024.pdf file, provide a detailed and accurate response. "
        "Your response should include:"
        "\n- Specific rank qualifications (PRSV, QGV, etc.) if relevant to the query"
        "\n- Precise payout amounts and calculations"
        "\n- Exact bonus structures and conditions"
        "\n- Any other relevant details from the compensation plan document"
        "\nMaintain a professional tone and use bullet points, tables or structured formatting where appropriate to make the information clear. "
        "If the information cannot be found in the document, clearly state this fact and explain what related information is available."
        "No external knowledge from you training data , reponse only with file search data information , no external informations"
    )

    file_search_tool = {
        "type": "file_search",
        "vector_store_ids": [vector_store_id],
        "max_num_results": 5,  # Increased to get more context
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
If I hit 600 PRSV but only reach 10,000 QGV, which rank will I qualify for?
Under what conditions would my Silver rank pay out $60 instead of $75 in a five-Monday month?
If one leg contributes more than 40% of my QGV, then how does that affect my Weekly Volume Achievement Bonus?
When my Enrollment Tree RSV hits $10,000 in 180 days, what Customer Accumulation Bonus do I earn?
If a customer fails to renew in the 7-day grace period, then what happens to my Customer Retention Bonus?
Which rank first requires 872 Single Product subscribers, and what are its PRSV and monthly payout?
If I maintain 150 PSV in three legs but only 800 QGV total, will I still qualify for Silver?
Under what conditions can I earn the $2,500 one-time bonus in my first 365 days?
If IBO fees increase, then where can I find the updated numbers for getting started?
When I hit 25,000 Enrollment Tree RSV in 240 days, what payout should I expect?
If months have five Mondays, then how do I calculate my Diamond rank weekly payment?
Under what circumstances would my Transform Bundle enrollment *not* trigger the $25 bonus?
"""



