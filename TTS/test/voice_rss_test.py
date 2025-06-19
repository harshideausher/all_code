import os
import requests
import json
import time

output_dir = 'voice_rss_voice'
ids_path = 'ids.json'

with open(ids_path, 'r') as file:
    data = json.load(file)

API_KEY = data['voice_rss_key_id']


languages = {
    "Spanish":    {"code": "es-es", "male": "Diego",  "female": "Camila"},
    "English":    {"code": "en-us", "male": "John",   "female": "Linda"},
    "French":     {"code": "fr-fr", "male": "Axel",   "female": "Bette"},
    "Italian":    {"code": "it-it", "male": "Pietro", "female": "Bria"},
    "Portuguese": {"code": "pt-pt", "male": "Dinis",  "female": "Leonor"},
    "Polish":     {"code": "pl-pl", "male": "Jan",    "female": "Julia"},
    "Japanese":   {"code": "ja-jp", "male": "Akira",  "female": "Hina"},
    "German":     {"code": "de-de", "male": "Jonas",  "female": "Hanna"}
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

    return lang, gender, text

def generate_audio(text, language_code, voice, output_file):
    url = "https://api.voicerss.org/"
    params = {
        "key": API_KEY,
        "hl": language_code,
        "src": text,
        "r": "0",
        "c": "mp3",
        "f": "44khz_16bit_stereo",
        "v": voice
    }

    print(f"\nGenerating speech with voice '{voice}' ({language_code})...")
    response = requests.get(url, params=params)


    if response.status_code == 200 and response.content.startswith(b'ERROR'):
        print("Error: Invalid API response. Check API key or parameters.")
        return False

    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Audio saved as {output_file}")
        return True
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return False

def main():
    lang, gender, text = get_user_selection()
    lang_details = languages[lang]
    voice = lang_details[gender]
    lang_code = lang_details["code"]

    file_name = f"{lang}_{gender}.mp3"
    output_path = os.path.join(output_dir, file_name)
    
    

    start_time = time.time()
    success = generate_audio(text, language_code=lang_code, voice=voice, output_file=output_path)
    elapsed_time = time.time() - start_time
    print(f"\nProcessing time: {elapsed_time:.2f} seconds.")
    if success:
        print("Speech generated successfully!")
    else:
        print("Speech generation failed.")

if __name__ == "__main__":
    main()
