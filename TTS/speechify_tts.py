import requests
import time
import base64


API_KEY = ""

BASE_URL = "https://api.sws.speechify.com/v1"


headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def get_available_voices():
    voices_endpoint = f"{BASE_URL}/voices"
    response = requests.get(voices_endpoint, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching voices:", response.status_code, response.text)
        return None


# voices_data = get_available_voices()
# if voices_data:
#     print("Available voices:")
#     for voice in voices_data:
#         print(f"ID: {voice.get('id')}, Language: {voice.get('language')}, Gender: {voice.get('gender')}")
# else:
#     print("No voices retrieved. Please verify the API endpoint and your credentials.")




texts = {
    "German": "Ich nutze KI zur Audiogenerierung und erschaffe eine Vielzahl von Klängen durch die Kraft des Codes. Von Musik bis Sprache fließt alles nahtlos zusammen und erzeugt Stimmen und Klänge, die natürlich wirken. Durch den Einsatz ausgefeilter Algorithmen können wir verschiedene Audioerlebnisse zum Leben erwecken, sei es eine Stimme oder eine Melodie. Die Magie der KI eröffnet endlose Möglichkeiten und ermöglicht kreative Freiheit sowie Innovation in der Klangproduktion. Es ist eine spannende Art, die Grenzen des Möglichen im Audio-Bereich zu erweitern.",
    "English": "I'm using AI to generate audio, creating a wide range of sounds through the power of code. From music to speech, it all flows seamlessly, crafting voices and sounds that feel natural. By leveraging sophisticated algorithms, we can bring various audio experiences to life, whether it's a voice or a melody. The magic of AI unlocks endless possibilities, allowing for creative freedom and innovation in sound production. It’s an exciting way to push the boundaries of what’s possible in audio.",
    "Spanish": "Estoy usando IA para generar audio, creando una amplia gama de sonidos a través del poder del código. Desde música hasta habla, todo fluye sin problemas, dando vida a voces y sonidos que se sienten naturales. Al aprovechar algoritmos sofisticados, podemos crear diversas experiencias de audio, ya sea una voz o una melodía. La magia de la IA desbloquea posibilidades infinitas, permitiendo una libertad creativa e innovación en la producción de sonido. Es una forma emocionante de ampliar los límites de lo que es posible en el audio.",
    "French": "J'utilise l'intelligence artificielle pour générer de l'audio, créant une large gamme de sons grâce à la puissance du code. De la musique à la parole, tout s'enchaîne harmonieusement, donnant naissance à des voix et des sons qui semblent naturels. En exploitant des algorithmes sophistiqués, nous pouvons donner vie à diverses expériences sonores, qu'il s'agisse d'une voix ou d'une mélodie. La magie de l'IA ouvre des possibilités infinies, offrant une liberté créative et une innovation sans limites dans la production audio. C'est une manière passionnante de repousser les frontières du possible en matière de son.",
    "Italian": "Sto usando l'intelligenza artificiale per generare audio, creando una vasta gamma di suoni attraverso la potenza del codice. Dalla musica al parlato, tutto scorre senza interruzioni, dando vita a voci e suoni che sembrano naturali. Sfruttando algoritmi sofisticati, possiamo creare diverse esperienze audio, che si tratti di una voce o di una melodia. La magia dell'IA sblocca infinite possibilità, permettendo libertà creativa e innovazione nella produzione sonora. È un modo entusiasmante per spingere i confini di ciò che è possibile nell'audio.",
    "Portuguese": "Estou usando IA para gerar áudio, criando uma ampla variedade de sons por meio do poder do código. Da música à fala, tudo flui perfeitamente, criando vozes e sons que parecem naturais. Ao aproveitar algoritmos sofisticados, podemos dar vida a diversas experiências sonoras, seja uma voz ou uma melodia. A magia da IA desbloqueia possibilidades infinitas, permitindo liberdade criativa e inovação na produção de som. É uma maneira empolgante de expandir os limites do que é possível no áudio.",
    "Polish": "Używam sztucznej inteligencji do generowania dźwięku, tworząc szeroką gamę brzmień za pomocą kodu. Od muzyki po mowę – wszystko płynie płynnie, kreując głosy i dźwięki, które brzmią naturalnie. Wykorzystując zaawansowane algorytmy, możemy ożywiać różne doświadczenia dźwiękowe, czy to głos, czy melodia. Magia sztucznej inteligencji otwiera nieskończone możliwości, dając swobodę twórczą i innowacje w produkcji dźwięku. To ekscytujący sposób na przesuwanie granic tego, co jest możliwe w świecie audio.",
    "Japanese": "私はAIを使ってオーディオを生成し、コードの力で多様な音を生み出しています。音楽から音声まで、すべてがシームレスに流れ、自然に感じられる声や音を作り出します。高度なアルゴリズムを活用することで、声やメロディーなど、さまざまなオーディオ体験を実現できます。AIの魔法が無限の可能性を解き放ち、音の制作における創造の自由と革新をもたらします。これは、オーディオの可能性を押し広げるエキサイティングな方法です。"
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




language_codes = {
    "German": "de-DE",
    "English": "en-US",
    "Spanish": "es-ES",
    "French": "fr-FR",
    "Italian": "it-IT",
    "Portuguese": "pt-BR",
    "Polish": "pl-PL",
    "Japanese": "ja-JP"
}




for language, text_sample in texts.items():
    voices_for_language = voice_mapping.get(language)
    lang_code = language_codes.get(language)
    if not voices_for_language or not lang_code:
        print(f"Missing voice or language code for {language}. Skipping...")
        continue

    for gender, voice_id in voices_for_language.items():
        print(f"\nSynthesizing {language} ({gender}) voice with voice ID: {voice_id}...")
        payload = {
            "input": text_sample,
            "voice_id": voice_id,
            "output_format": "mp3",
            "language": lang_code
        }
        synth_endpoint = f"{BASE_URL}/audio/speech"
        response = requests.post(synth_endpoint, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            audio_data_base64 = data.get("audio_data")
            if audio_data_base64:
                audio_data = base64.b64decode(audio_data_base64)
                filename = f"{language}_{lang_code}_{gender}.mp3"
                with open(filename, "wb") as audio_file:
                    audio_file.write(audio_data)
                print(f"Audio saved to {filename}")
            else:
                print(f"No audio data found in response for {language} ({gender}).")
        else:
            print(f"Error {response.status_code} for {language} ({gender}): {response.text}")
        time.sleep(5)

