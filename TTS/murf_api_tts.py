import requests
import json
import base64
import time


url = "https://api.murf.ai/v1/speech/generate"
api_key = ""


texts = {
    "German": "Ich nutze KI zur Audiogenerierung und erschaffe eine Vielzahl von Klängen durch die Kraft des Codes. Von Musik bis Sprache fließt alles nahtlos zusammen und erzeugt Stimmen und Klänge, die natürlich wirken. Durch den Einsatz ausgefeilter Algorithmen können wir verschiedene Audioerlebnisse zum Leben erwecken, sei es eine Stimme oder eine Melodie. Die Magie der KI eröffnet endlose Möglichkeiten und ermöglicht kreative Freiheit sowie Innovation in der Klangproduktion. Es ist eine spannende Art, die Grenzen des Möglichen im Audio-Bereich zu erweitern.",
    "English": "I'm using AI to generate audio, creating a wide range of sounds through the power of code. From music to speech, it all flows seamlessly, crafting voices and sounds that feel natural. By leveraging sophisticated algorithms, we can bring various audio experiences to life, whether it's a voice or a melody. The magic of AI unlocks endless possibilities, allowing for creative freedom and innovation in sound production. It’s an exciting way to push the boundaries of what’s possible in audio.",
    "Spanish": "Estoy usando IA para generar audio, creando una amplia gama de sonidos a través del poder del código. Desde música hasta habla, todo fluye sin problemas, dando vida a voces y sonidos que se sienten naturales. Al aprovechar algoritmos sofisticados, podemos crear diversas experiencias de audio, ya sea una voz o una melodía. La magia de la IA desbloquea posibilidades infinitas, permitiendo una libertad creativa e innovación en la producción de sonido. Es una forma emocionante de ampliar los límites de lo que es posible en el audio.",
    "French": "J'utilise l'intelligence artificielle pour générer de l'audio, créant une large gamme de sons grâce à la puissance du code. De la musique à la parole, tout s'enchaîne harmonieusement, donnant naissance à des voix et des sons qui semblent naturels. En exploitant des algorithmes sophistiqués, nous pouvons donner vie à diverses expériences sonores, qu'il s'agisse d'une voix ou d'une mélodie. La magie de l'IA ouvre des possibilités infinies, offrant une liberté créative et une innovation sans limites dans la production audio. C'est une manière passionnante de repousser les frontières du possible en matière de son.",
    "Italian": "Sto usando l'intelligenza artificiale per generare audio, creando una vasta gamma di suoni attraverso la potenza del codice. Dalla musica al parlato, tutto scorre senza interruzioni, dando vita a voci e suoni che sembrano naturali. Sfruttando algoritmi sofisticati, possiamo creare diverse esperienze audio, che si tratti di una voce o di una melodia. La magia dell'IA sblocca infinite possibilità, permettendo libertà creativa e innovazione nella produzione sonora. È un modo entusiasmante per spingere i confini di ciò che è possibile nell'audio.",
    "Portuguese": "Estou usando IA para gerar áudio, criando uma ampla variedade de sons por meio do poder do código. Da música à fala, tudo flui perfeitamente, criando vozes e sons que parecem naturais. Ao aproveitar algoritmos sofisticados, podemos dar vida a diversas experiências sonoras, seja uma voz ou uma melodia. A magia da IA desbloqueia possibilidades infinitas, permitindo liberdade criativa e inovação na produção de som. É uma maneira empolgante de expandir os limites do que é possível no áudio.",
    "Polish": "Używam sztucznej inteligencji do generowania dźwięku, tworząc szeroką gamę brzmień za pomocą kodu. Od muzyki po mowę – wszystko płynie płynnie, kreując głosy i dźwięki, które brzmią naturalnie. Wykorzystując zaawansowane algorytmy, możemy ożywiać różne doświadczenia dźwiękowe, czy to głos, czy melodię. Magia sztucznej inteligencji otwiera nieskończone możliwości, dając swobodę twórczą i innowacje w produkcji dźwięku. To ekscytujący sposób na przesuwanie granic tego, co jest możliwe w świecie audio.",
    "Japanese": "私はAIを使ってオーディオを生成し、コードの力で多様な音を生み出しています。音楽から音声まで、すべてがシームレスに流れ、自然に感じられる声や音を作り出します。高度なアルゴリズムを活用することで、声やメロディーなど、さまざまなオーディオ体験を実現できます。AIの魔法が無限の可能性を解き放ち、音の制作における創造の自由と革新をもたらします。これは、オーディオの可能性を押し広げるエキサイティングな方法です。"
}



voice_configs = {
    "German": {
        "Female": {"voiceId": "de-DE-lia", "multiNativeLocale": "de-DE", "style": "Conversational"},
        "Male":   {"voiceId": "de-DE-matthias", "multiNativeLocale": "de-DE", "style": "Conversational"}
    },
    "English": {
        "Female": {"voiceId": "en-US-natalie", "multiNativeLocale": "en-US", "style": "Neutral"},
        "Male":   {"voiceId": "en-GB-william", "multiNativeLocale": "en-GB", "style": "Neutral"}
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


languages = ["German", "English", "Spanish", "French", "Italian", "Portuguese", "Polish"]


for language in languages:
    text_sample = texts.get(language)
    config_by_gender = voice_configs.get(language)
    if not text_sample or not config_by_gender:
        print(f"Missing text or voice configuration for {language}. Skipping...")
        continue

    for gender, config in config_by_gender.items():
        print(f"\nSynthesizing {language} ({gender}) voice with voice ID {config['voiceId']}...")
        payload = json.dumps({
            "voiceId": config["voiceId"],
            "style": config["style"],
            "text": text_sample,
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

        headers_request = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'api-key': api_key
        }

        try:
            response = requests.post(url, headers=headers_request, data=payload)
            print(f"Status Code for {language} ({gender}): {response.status_code}")
            json_resp = response.json()

            encoded_audio = json_resp.get("encodedAudio")
            if encoded_audio:
                audio_bytes = base64.b64decode(encoded_audio)
                filename = f"{language}_{config['multiNativeLocale']}_{gender}_voice.mp3"
                with open(filename, "wb") as f:
                    f.write(audio_bytes)
                print(f"Audio saved as {filename}")
            else:
                print(f"Audio data not found in response for {language} ({gender}).")
        except Exception as e:
            print(f"An error occurred for {language} ({gender}): {e}")
        time.sleep(5)

