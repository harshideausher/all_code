import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

vector_store_id = "vs_680f1bf79f3081919b4362573359f9bc"
file_id = "file-MgxJewiAPmrvfKLLARFMER"

def pay_plan_info(user_query):
    prompt = (
        f"The user is looking for comprehensive details on '{user_query}' from the IYOVIA Pay Plan document. "
        "You have access *only* to the IYOVIA_PAY_PLAN.txt file. Using *only* its content and formatting conventions, craft a response that includes:\n"
        "- A clear explanation of the specific pay plan feature the user is asking about\n"
        "- Any relevant qualification criteria, thresholds, or requirements\n"
        "- Specific bonus amounts, percentages, or calculation methods\n"
        "- Timeline considerations (weekly payouts, holding periods, etc.)\n"
        "- One actionable strategy for optimizing this aspect of the pay plan\n"
        "- A reflective follow-up question to help the user implement this knowledge\n"
        "Keep the tone precise, aligned with the file's style, and include any bold headings or list formatting exactly as shown in the source. "
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

"I'd like to go through a quick discovery session so you can tailor your coaching to my needs.",
"Can you assess my current network-marketing skill level and suggest where I should focus?",
"How can I improve my online recruiting strategy—my success rate is only 3/10.",
"I'm struggling with duplication: walk me through building a standardized onboarding process.",
"My outreach messages aren't getting replies. Here's my script—optimize it for engagement.",
"Help me craft a 30/60/90-day action plan with SMART milestones for scaling my team.",
"Which automation tools or CRMs would you recommend to streamline my follow-up?",
"How do I ensure my social-media promotions stay FTC-compliant while still converting?",
"My team churns after three months—what retention and recognition programs should I set up?",
"Explain how to structure my compensation-plan strategy for maximum commissions.",
"I want to expand my business globally—what steps should I take for international growth?",
"Can you help me build a high-converting group-meeting script using persuasion psychology?",
"What are my top three income-producing activities, and how do I prioritize them?",
"I need a follow-up email sequence using AI chatbots—can you draft that for me?",
"How do I strengthen my personal brand and attraction-marketing funnel?",
"Audit my current prospecting method and recommend improvements.",
"What leadership routines should I implement to develop independent leaders on my team?",
"I'm overwhelmed—help me eliminate distractions and focus on the highest-impact tasks.",
"How should I leverage paid ads (Facebook/Google) for targeted recruitment?",
"What compliance checkpoints must I include in my marketing materials to avoid legal issues?",

"""
