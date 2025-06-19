import requests
import time
import os
import base64
import json



output_dir = 'spechify_voice'
ids_path = 'ids.json'
     
with open(ids_path, 'r') as file:
    data = json.load(file)

API_KEY = data['speechify_key_id']

BASE_URL = "https://api.sws.speechify.com/v1"



headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

languages = {
    "German": "de-DE",
    "English": "en-US",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "Italian": "it-IT",
    "Portuguese": "pt-BR",
    "Polish": "pl-PL",
    "Japanese": "ja-JP"
}

voice_mapping = {
    "German":    {"male": "henry",    "female": "bwyneth"},
    "English":   {"male": "joe",      "female": "lisa"},
    "Spanish":   {"male": "rob",      "female": "emily"},
    "French":    {"male": "mason",    "female": "victoria"},
    "Italian":   {"male": "peter",    "female": "julie"},
    "Portuguese":{"male": "nick",     "female": "tasha"},
    "Polish":    {"male": "phil",     "female": "stacy"},
    "Japanese":  {"male": "oliver",   "female": "carly"}
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


    voice_id = voice_mapping[lang][gender]
    lang_code = languages[lang]
    print(f'{lang_code = }')

    print(f"\nGenerating {lang} ({gender}) speech with voice ID: {voice_id}...")

    start_time = time.time()
    payload = {
        "input": text,
        "voice_id": voice_id,
        "output_format": "mp3",
        "language": lang_code
    }


    response = requests.post(f"{BASE_URL}/audio/speech", headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        audio_data_base64 = data.get("audio_data")
        if audio_data_base64:
            audio_data = base64.b64decode(audio_data_base64)
            filename = f"{lang}_{gender}.mp3"
            output_path = os.path.join(output_dir,filename)
            with open(output_path, "wb") as audio_file:
                audio_file.write(audio_data)
            print(f"Speech generated successfully! Saved as {filename}")
        else:
            print(f"No audio data found in response for {lang} ({gender}).")
    else:
        print(f"Error {response.status_code}: {response.text}")

    elapsed_time = time.time() - start_time
    print(f"\nProcessing time: {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
