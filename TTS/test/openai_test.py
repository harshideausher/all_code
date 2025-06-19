import os
import time
from openai import OpenAI
import json



output_dir = 'openai_voice'
ids_path = 'ids.json'
     
with open(ids_path, 'r') as file:
    data = json.load(file)


client = OpenAI(api_key=data['open_ai_key_id'])


languages = {
    "German": "de",
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "Italian": "it",
    "Portuguese": "pt",
    "Polish": "pl",
    "Japanese": "ja"
}

voices = {
    "male": "alloy",
    "female": "nova"
}


def get_user_selection():
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    available_languages = list(languages.keys())
    print("Select a language:")
    for i, lang in enumerate(available_languages, 1):
        print(f"{i}. {lang}")


    choice = int(input("Enter the number of your choice: "))
    lang = available_languages[choice - 1]

    gender = input("Select gender (male/female): ").lower()

    text = input(f"Enter the text in {lang} to convert to speech: ")


    return lang, gender , text

def main():


    lang , gender , text = get_user_selection()

    voice = voices[gender]

    print(f"Generating speech in {lang} ({gender})...")
    start_time = time.time()
    
    response = client.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        response_format="mp3"
    )
    
    filename = f"{lang}_{gender}.mp3"
    output_path = os.path.join(output_dir,filename)
    with open(output_path, "wb") as audio_file:
        audio_file.write(response.content)
    
    elapsed_time = time.time() - start_time
    print(f"Speech generated successfully! Saved as {filename}")
    print(f"\nProcessing time: {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
