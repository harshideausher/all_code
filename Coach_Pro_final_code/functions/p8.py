import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

vector_store_id = "vs_680f1bf79f3081919b4362573359f9bc"
file_id = "file-ELsvSm2Wvu6taQ9yahcVm6"

def foundational_skills(user_query):
    prompt = (
        f"The user wants to develop foundational network marketing skills regarding '{user_query}'. "
        "Using *only* the content and formatting style from the foundational_skills_in_network_marketing.txt file, provide a response that includes:\n"
        "- A clear definition or explanation of the skill or concept the user is asking about\n"
        "- The key principles or best practices related to developing this skill\n"
        "- Practical examples of how to apply this skill in network marketing\n"
        "- Actionable exercises or steps the user can take to improve in this area\n"
        "- A reflective question to help the user assess their progress with this skill\n"
        "Keep the tone instructive and professional, and structure your response with clear headings and bullet points for readability. "
        "If the user's query is unrelated to network marketing foundational skills or unclear, ask them to clarify their request."
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







# Example questions for testing
"""
How can I practice active listening to build better rapport with prospects?
What's the simplest way to structure my prospecting daily so I never run out of leads?
Teach me a step-by-step system for onboarding new recruits to duplicate my process.
Which non-verbal cues should I focus on to appear more confident during presentations?
How do I transition from a 'salesy' mindset to seeing selling as helping?
Give me three scripts for handling the 'I'm not interested' objection professionally.
What are the key components of an effective follow-up without being pushy?
Help me identify my ideal prospect profile—what traits should I look for?
How do I build trust quickly with someone skeptical of network marketing?
Outline a daily blueprint for warm-market prospecting and asking for referrals.
What's the difference between addition vs. multiplication in network marketing growth?
Walk me through creating a simple new-recruit success plan for their first 30 days.
How can I use storytelling to make my product presentations more compelling?
What's the art of teaching duplication so my team can grow independently?
Which trust-building practices keep customers and team members engaged long-term?
Share best practices for consistent communication to maintain trust in my downline.
How do I overcome my fear of cold-market prospecting?
What metrics should I track to monitor my team's duplication progress?
Give me an empathy-based approach to handle price objections effectively.
How can I master the art of closing without being pushy?
If I notice my team isn't following the new-recruit success plan, what corrective actions should I take?
When my prospect seems hesitant, what conditional rapport-building questions can I ask to re-engage them?
If I only have 10 minutes, what's the most effective follow-up template I can use?
How should I adjust my prospecting approach if my cold-market response rate drops below 10%?
If a recruit fails to hit their first-week activity goals, what supportive steps can I implement?
When presenting online versus in person, which non-verbal cues change and why?
If a prospect raises a price objection, under what conditions should I pivot to a value story?
What conditional criteria should I use to decide between warm-market and cold-market prospecting on a given day?
If I want to prioritize building leaders, what delegation strategy should I follow based on their activity level?
Under what circumstances would you recommend shortening the onboarding checklist for fast starters?
If my daily prospect list falls below 15 names, what automated tools can I use to refill it?
When is it appropriate to escalate an objection about time versus price, and how do I handle each?
If my social media posts aren't generating engagement, what conditional tweaks can I make to my messaging?
Under what conditions should I switch from text-based follow-up to a quick voice note?
If a team member consistently misses duplication KPIs, what conditional coaching framework should I apply?
"""
