import os
import requests
import time
import json

output_dir = 'zephyra_voice'
ids_path = 'ids.json'

with open(ids_path, 'r') as file:
    data = json.load(file)

API_KEY = data['zephyra_key_id']
BASE_URL = "http://api.zyphra.com/v1/audio/text-to-speech"


HEADERS = {
    "x-api-key": API_KEY,
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

voices = {
    "male": "male",
    "female": "female"
}

def get_user_selection():

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    available_languages = list(languages.keys())
    print("Select a language:")
    for i, lang in enumerate(available_languages, 1):
        print(f"{i}. {lang}")
    
    choice = int(input("\nEnter the number of your choice: "))
    selected_language = available_languages[choice - 1]
    code = languages[selected_language]
    
    gender = input("Select gender (male/female): ").lower()
    
    text = input(f"Enter the text in {selected_language} to convert to speech: ")
    return selected_language, code, gender, text




def generate_audio(voice: str, code: str, text: str, output_filename: str):
    endpoint_url = f"{BASE_URL}?voice={voice}&locale={code}"
    endpoint_url = f"{BASE_URL}?voice={voice}&locale={code}"

    payload = {"text": text}
    
    print(f"\nGenerating speech for {code} ({voice}) voice...")
    
    response = requests.post(endpoint_url, headers=HEADERS, json=payload)
    if response.status_code == 200:
        with open(output_filename, "wb") as audio_file:
            audio_file.write(response.content)
        print(f"Audio saved: {output_filename}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main():
    selected_language, code, gender, text = get_user_selection()
    voice = voices[gender]
    filename = f"{selected_language}_{gender}.mp3"
    output_path = os.path.join(output_dir, filename)
    
    start_time = time.time()
    generate_audio(voice, code, text, output_path)
    elapsed_time = time.time() - start_time
    print(f"\nProcessing time: {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()



