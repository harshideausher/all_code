import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

vector_store_id = "vs_680f1bf79f3081919b4362573359f9bc"
file_id = "file-MgxJewiAPmrvfKLLARFMER"

def customer_bonus(user_query):
    prompt = (
        f"The user is looking to understand the '{user_query}' from the IYOVIA compensation structure. "
        "Using *only* the content and formatting style from the IYOVIA_PAY_PLAN.txt file, provide a response that includes:\n"
        "- A summary of what the Customer Accumulation Bonus is and how it works\n"
        "- All volume thresholds, timeframes, and payout amounts involved\n"
        "- Any qualifying rules or limitations clearly listed in the file\n"
        "- A real-world example of how an IBO could reach one of the bonus levels\n"
        "- A reflective question to help the user assess their current progress toward earning it\n"
        "Keep the tone informative and use clear, structured bullet points or lists to match the file's style."
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
What are the exact steps and fees to get started as an IBO?
Define Active, PSV, PRSV, QGV, and Enrollment Tree RSV.
Which products and bundles qualify for the one-time Customer Enrollment Bonus, and how much is each?
Outline the Weekly Volume Achievement Bonus requirements and payouts for the Diamond rank.
List PRSV, QGV, Single Product Subscribers, Bundle Subscribers, and monthly/weekly pay for Gold.
Explain the 40/40/20 Line Max Rule—what counts and how is it applied?
How does the 55/45 Customer Rule work for counting QGV?
Detail the Customer Accumulation Bonus tiers, volumes, timeframes, and payouts.
How is the Customer Retention Bonus structured after 84 days, and what are the ongoing payments?
What are the PRSV and QGV thresholds (and max QGV per leg) for Star Titanium, and what does it pay?
What enrollment and recurring volumes count for the Transform Bundle?
When are IBO commissions and bonuses paid, and what's the weekly pay cycle?
What does 'Active' status mean for an IBO vs. a Customer, and when does inactivity occur?
Summarize the Income Disclaimer and the 2022 average IBO earnings.
How are weekly bonus payments adjusted in months with five Mondays?
What is the per-cycle volume value for a Foreign Exchange subscription?
Which rank first requires 354 Single Subs, and what is its monthly payout?
Where can I find current IBO fees, policies, and the IBO handbook online?
Explain Spillover and how enrollments from upline place people in your Marketing Organization.
If I hit 600 PRSV and 26,600 QGV, which rank have I achieved and what will my payouts be?


"""
