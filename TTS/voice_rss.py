import requests

# Your voicerss API key
API_KEY = ""

languages = {
    1: {"name": "English", "code": "en-us", "male": "John", "female": "Linda"},
    2: {"name": "Spanish", "code": "es-es", "male": "Diego", "female": "Camila"},
    3: {"name": "French", "code": "fr-fr", "male": "Axel", "female": "Bette"},
    4: {"name": "Italian", "code": "it-it", "male": "Pietro", "female": "Bria"},
    5: {"name": "Portuguese", "code": "pt-pt", "male": "Dinis", "female": "Leonor"},
    6: {"name": "Polish", "code": "pl-pl", "male": "Jan", "female": "Julia"},
    7: {"name": "Japanese", "code": "ja-jp", "male": "Akira", "female": "Hina"},
    8: {"name": "German", "code": "de-de", "male": "Jonas", "female": "Hanna"},
}

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
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        with open(output_file, "wb") as f:
            f.write(response.content)
        print(f"Audio saved as {output_file}")
    else:
        print("Error")

def main():

    print("Select a language by entering its number:")
    for num, details in languages.items():
        print(f"{num}. {details['name']}")

    try:
        choice = int(input("\nEnter the number of your choice: "))
        if choice not in languages:
            print("Invalid selection. Please try again.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    selected_lang = languages[choice]
    lang_name = selected_lang["name"]
    lang_code = selected_lang["code"]

    text = input("\nEnter the text : ")

    for gender in ["male", "female"]:
        voice = selected_lang[gender]
        file_name = f"{lang_name}_{gender}.mp3"
        
        generate_audio(text, language_code=lang_code, voice=voice, output_file=file_name)

if __name__ == "__main__":
    main()
