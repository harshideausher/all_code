import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))



vector_store_id = "vs_680f1bf79f3081919b4362573359f9bc"
file_id = "file-Xijo7WKWUDtqYGu1QpwfQa"

def authority_building(user_query):
    prompt = (
        f"The user says: '{user_query}'. "
        "You have access *only* to the “Authority & Influence Building for Network Marketing Professionals” file. "
        "Using *only* the frameworks, examples, and step-by-step processes in that file, craft a tailored, high-impact response that includes:\n"
        "- A customized UVP formulation based on their niche and pain points\n"
        "- Two authority‐asset ideas (e.g. PDF guide, video training) with clear formats and topics\n"
        "- A detailed social proof + reciprocity + trigger influence framework applied to their situation\n"
        "- A 30/60/90-day action plan with SMART milestones and accountability checkpoints\n"
        "- Answers to at least one relevant FAQ from the file\n"
        "- An offer of a plug-and-play tool (UVP generator, funnel script, or Reels planner)\n"
        "Keep the tone strategic, empowering, and focused on sustainable, long-term growth."
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
"I just had three people say ‘no’ in one day and I’m feeling defeated. What can I do?",
"I feel like I’m failing because I haven’t made a sale in weeks. How do I bounce back?",
"I’m exhausted from constantly reaching out to prospects and getting ghosted. Any tips?",
"I beat myself up every time someone doesn’t join my team. How can I be kinder to myself?",
"Yesterday, a downline left me and it crushed my confidence. How do I reframe this?",
"I’m burned out and can’t find motivation to keep going—what should I try?",
"Every time I hit a setback, I feel like giving up. How can I build resilience?",
"I don’t have anyone to talk to about my frustrations. How do I find support?",
"I’m overwhelmed balancing work hours and personal life. How can I set healthier boundaries?",
" I’m proud of signing one lead, but it feels insignificant next to my goals. How can I celebrate small wins?",
" I keep replaying rejections in my head—how do I stop dwelling on them?",
" I want to stay positive long-term, even when growth is slow. Any mindset shifts?",
" I feel lonely in this business—what can I do today to recharge?",
" How do I learn from a conversation that didn’t go well without beating myself up?",
" I’m worried about burning out before I reach my targets. What practical stress-management tip can help?",
" My confidence dips every time I face rejection—how can I remind myself I’m capable?",
" No one in my family understands this business. How do I build an external support system?",
" I need help reframing a recent failure—can you guide me through that?",
" I’m feeling a lot of self-doubt after a teammate’s departure. How do I recover emotionally?",
" What daily habits can I adopt to strengthen my emotional resilience?",

"""




