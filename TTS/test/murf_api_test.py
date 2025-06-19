import requests
import json
import base64
import time
import os


ids_path = 'ids.json'
output_dir = "murf_voice"
     
with open(ids_path, 'r') as file:
    data = json.load(file)



API_KEY = data['murf_key_id']
URL = "https://api.murf.ai/v1/speech/generate"



voice_configs = {
    "German": {
        "Female": {"voiceId": "de-DE-lia", "multiNativeLocale": "de-DE", "style": "Conversational"},
        "Male":   {"voiceId": "de-DE-matthias", "multiNativeLocale": "de-DE", "style": "Conversational"}
    },
    "English": {
        "Female": {"voiceId": "en-US-natalie", "multiNativeLocale": "en-US", "style": "Neutral"},
        "Male":   {"voiceId": "en-US-miles", "multiNativeLocale": "en-US", "style": "Neutral"}
    },
    "Spanish": {
        "Female": {"voiceId": "es-ES-elvira", "multiNativeLocale": "es-ES", "style": "Conversational"},
        "Male":   {"voiceId": "es-ES-enrique", "multiNativeLocale": "es-ES", "style": "Conversational"}
    },
    "French": {
        "Female": {"voiceId": "fr-FR-adélie", "multiNativeLocale": "fr-FR", "style": "Conversational"},
        "Male":   {"voiceId": "fr-FR-maxime", "multiNativeLocale": "fr-FR", "style": "Conversational"}
    },
    "Italian": {
        "Female": {"voiceId": "it-IT-greta", "multiNativeLocale": "it-IT", "style": "Conversational"},
        "Male":   {"voiceId": "it-IT-lorenzo", "multiNativeLocale": "it-IT", "style": "Conversational"}
    },
    "Portuguese": {
        "Female": {"voiceId": "pt-BR-isadora", "multiNativeLocale": "pt-BR", "style": "Conversational"},
        "Male":   {"voiceId": "pt-BR-heitor", "multiNativeLocale": "pt-BR", "style": "Conversational"}
    },
    "Polish": {
        "Female": {"voiceId": "pl-PL-kasia", "multiNativeLocale": "pl-PL", "style": "Conversational"},
        "Male":   {"voiceId": "pl-PL-jacek", "multiNativeLocale": "pl-PL", "style": "Conversational"}
    }
}

def get_user_selection():
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    available_languages = list(voice_configs.keys())
    print("Select a language:")
    for i, lang in enumerate(available_languages, 1):
        print(f"{i}. {lang}")


    choice = int(input("Enter the number of your choice: "))
    lang = available_languages[choice - 1]

    gender = input("Select gender (male/female): ").capitalize()

    text = input(f"Enter the text in {lang} to convert to speech: ")


    return lang, gender , text


def generate_audio(text, language, gender):
    
    
    config = voice_configs[language][gender]

    print(f"\nSynthesizing {language} ({gender}) voice with voice ID {config['voiceId']}...")

    payload = json.dumps({
        "voiceId": config["voiceId"],
        "style": config["style"],
        "text": text,
        "rate": 0,
        "pitch": 0,
        "sampleRate": 48000,
        "format": "MP3",
        "channelType": "MONO",
        "pronunciationDictionary": {},
        "encodeAsBase64": True,
        "variation": 1,
        "audioDuration": 0,
        "modelVersion": "GEN2",
        "multiNativeLocale": config["multiNativeLocale"]
    })

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'api-key': API_KEY
    }

    try:
        response = requests.post(URL, headers=headers, data=payload)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            json_resp = response.json()
            encoded_audio = json_resp.get("encodedAudio")

            if encoded_audio:
                audio_bytes = base64.b64decode(encoded_audio)
                filename = f"{output_dir}/{language}_{gender}.mp3"

                with open(filename, "wb") as f:
                    f.write(audio_bytes)

                print(f"Audio saved as {filename}")
            else:
                print("Audio data not found in response.")
        else:
            print(f"Error: {response.text}")

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    
    language, gender , text = get_user_selection()

    start_time = time.time()
    generate_audio(text, language, gender)
    elapsed_time = time.time() - start_time
    print(f"\nProcessing time: {elapsed_time:.2f} seconds.")


if __name__ == "__main__":
    main()
