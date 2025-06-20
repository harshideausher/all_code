import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

vector_store_id = "vs_680f1bf79f3081919b4362573359f9bc"
file_id = "file-2BQLQLVNgpEe1debBpZVC8"

def ibo_resources(user_query):
    prompt = (
        f"The user is looking for an overview of the '{user_query}' in the IBO Resources Hub. "
        "You have access *only* to the uploaded Copy_of_IBO_Resources_Hub.pdf file. Using *only* the content "
        "and any formatting guidelines in that file, craft a response that includes:\n"
        "- A list of all video codes and titles in the 300 series\n"
        "- The total number of videos in that series\n"
        "- Any Y/N status indicators next to each video\n"
        "- One actionable recommendation on which video to start with\n"
        "- A reflective question to help the user plan their learning\n"
        "Keep the tone informative and concise, and adhere strictly to the file's formatting rules."
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




"""

"I’m a health coach for busy executives—help me craft a UVP that speaks to their pain points.  ",
"What are two authority‐asset ideas I could create this month to attract more leads?  ",
"How do I apply social proof stacking + reciprocity + storytelling to my current launch?  ",
"Give me a 30/60/90-day roadmap with SMART milestones to build my influence from scratch.  ",
"Do I need a big following before I start sharing authority content?  ",
"I don’t feel expert enough—how do I overcome that barrier?  ",
"Can you plug-and-play me a UVP generator based on my niche?  ",
"I want a funnel script template to onboard webinar attendees—what should it look like?  ",
"How do I plan weekly Reels so they feed into my link-in-bio funnel?  ",
"What’s a simple PDF guide topic I can create this week for busy parents?  ",
"Outline a 10-minute video training on overcoming skepticism in my niche.  ",
"How do I set up a lead-magnet funnel with automated follow-ups?  ",
"Suggest three collaboration ideas (podcast, IG Live, mini-course) to expand my reach.  ",
"How should I track and celebrate hitting my first passive-income sale by Day 90?  ",
"What accountability checkpoints should I build into my 60-day plan?  ",
"How do I use scarcity and identity resonance as influence triggers?  ",
"Can you answer the FAQ: ‘What if I don’t feel “expert enough”?’”  ",
"I want to host a mini-masterclass—what’s the step-by-step outline?  ",
"Help me expand my digital presence with IG auto-DMs and weekly emails.  ",
"Offer me a plug-and-play weekly Reels planner tailored to my audience.  ",
"Walk me through crafting a joint IG Live with an influencer in my space.  ",
"I need a milestone calendar for publishing my UVP, asset, and first funnel.  ",
"What’s the fastest way to assemble and launch an authority-building checklist?  ",
"How can I leverage reciprocity loops to boost my email-list signups?  ",
"Can you build me a 30/60/90-day action plan plus FAQs and tool offer at the end?",

"""



