import boto3
import time
import os
import json


ids_path = 'ids.json'

with open(ids_path, 'r') as file:
    data = json.load(file)



polly = boto3.client(
    'polly',
    aws_access_key_id=data['aws_access_key_id'],
    aws_secret_access_key=data['aws_secret_access_key'],
    region_name='us-east-1'
)

texts = {
    "German": "Ich nutze KI zur Audiogenerierung und erschaffe eine Vielzahl von Klängen durch die Kraft des Codes. Von Musik bis Sprache fließt alles nahtlos zusammen und erzeugt Stimmen und Klänge, die natürlich wirken. Durch den Einsatz ausgefeilter Algorithmen können wir verschiedene Audioerlebnisse zum Leben erwecken, sei es eine Stimme oder eine Melodie. Die Magie der KI eröffnet endlose Möglichkeiten und ermöglicht kreative Freiheit sowie Innovation in der Klangproduktion. Es ist eine spannende Art, die Grenzen des Möglichen im Audio-Bereich zu erweitern.",
    "English": "I'm using AI to generate audio, creating a wide range of sounds through the power of code. From music to speech, it all flows seamlessly, crafting voices and sounds that feel natural. By leveraging sophisticated algorithms, we can bring various audio experiences to life, whether it's a voice or a melody. The magic of AI unlocks endless possibilities, allowing for creative freedom and innovation in sound production. It’s an exciting way to push the boundaries of what’s possible in audio.",
    "Spanish": "Estoy usando IA para generar audio, creando una amplia gama de sonidos a través del poder del código. Desde música hasta habla, todo fluye sin problemas, dando vida a voces y sonidos que se sienten naturales. Al aprovechar algoritmos sofisticados, podemos crear diversas experiencias de audio, ya sea una voz o una melodía. La magia de la IA desbloquea posibilidades infinitas, permitiendo una libertad creativa e innovación en la producción de sonido. Es una forma emocionante de ampliar los límites de lo que es posible en el audio.",
    "French": "J'utilise l'intelligence artificielle pour générer de l'audio, créant une large gamme de sons grâce à la puissance du code. De la musique à la parole, tout s'enchaîne harmonieusement, donnant naissance à des voix et des sons qui semblent naturels. En exploitant des algorithmes sophistiqués, nous pouvons donner vie à diverses expériences sonores, qu'il s'agisse d'une voix ou d'une mélodie. La magie de l'IA ouvre des possibilités infinies, offrant une liberté créative et une innovation sans limites dans la production audio. C'est une manière passionnante de repousser les frontières du possible en matière de son.",
    "Italian": "Sto usando l'intelligenza artificiale per generare audio, creando una vasta gamma di suoni attraverso la potenza del codice. Dalla musica al parlato, tutto scorre senza interruzioni, dando vita a voci e suoni che sembrano naturali. Sfruttando algoritmi sofisticati, possiamo creare diverse esperienze audio, che si tratti di una voce o di una melodia. La magia dell'IA sblocca infinite possibilità, permettendo libertà creativa e innovazione nella produzione sonora. È un modo entusiasmante per spingere i confini di ciò che è possibile nell'audio.",
    "Portuguese": "Estou usand o IA para gerar áudio, criando uma ampla variedade de sons por meio do poder do código. Da música à fala, tudo flui perfeitamente, criando vozes e sons que parecem naturais. Ao aproveitar algoritmos sofisticados, podemos dar vida a diversas experiências sonoras, seja uma voz ou uma melodia. A magia da IA desbloqueia possibilidades infinitas, permitindo liberdade criativa e inovação na produção de som. É uma maneira empolgante de expandir os limites do que é possível no áudio.",
    "Polish": "Używam sztucznej inteligencji do generowania dźwięku, tworząc szeroką gamę brzmień za pomocą kodu. Od muzyki po mowę – wszystko płynie płynnie, kreując głosy i dźwięki, które brzmią naturalnie. Wykorzystując zaawansowane algorytmy, możemy ożywiać różne doświadczenia dźwiękowe, czy to głos, czy melodię. Magia sztucznej inteligencji otwiera nieskończone możliwości, dając swobodę twórczą i innowacje w produkcji dźwięku. To ekscytujący sposób na przesuwanie granic tego, co jest możliwe w świecie audio.",
    "Japanese": "私はAIを使ってオーディオを生成し、コードの力で多様な音を生み出しています。音楽から音声まで、すべてがシームレスに流れ、自然に感じられる声や音を作り出します。高度なアルゴリズムを活用することで、声やメロディーなど、さまざまなオーディオ体験を実現できます。AIの魔法が無限の可能性を解き放ち、音の制作における創造の自由と革新をもたらします。これは、オーディオの可能性を押し広げるエキサイティングな方法です。"
}


polly_languages = {
    "German": {"code": "de-DE", "male": "Daniel", "female": "Vicki"},
    "English": {"code": "en-US", "male": "Gregory", "female": "Danielle"},
    "Spanish": {"code": "es-ES", "male": "Sergio", "female": "Lucia"},
    "French":  {"code": "fr-FR", "male": "Remi",   "female": "Lea"},
    "Italian": {"code": "it-IT", "male": "Adriano", "female": "Bianca"},
    "Portuguese": {"code": "pt-BR", "male": "Thiago", "female": "Camila"},
    "Polish": {"code": "pl-PL", "male": "Ewa", "female": "Ola"},                            # male voice not present
    "Japanese": {"code": "ja-JP", "male": "Takumi", "female": "Kazuha"}
}

def generate_audio(text, language_code, voice, output_file, engine='neural'):

    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice,
        LanguageCode=language_code,
        Engine=engine
    )
    output_path = os.path.join('polly_voice', output_file)
    if "AudioStream" in response:
        with open(output_path, 'wb') as file:
            file.write(response['AudioStream'].read())
        print(f"Audio file '{output_path}' saved successfully!")
    else:
        print(f"Error: No AudioStream returned for voice {voice}.")



def main():
    time1 = time.time()
    for language, text in texts.items():
        if language in polly_languages:
            details = polly_languages[language]
            lang_code = details["code"]
            for gender in ["male", "female"]:
                voice = details[gender]
                file_name = f"{language}_{gender}.mp3"
                print(f"Generating audio for {language} ({gender} voice: {voice})...")


                engine = 'neural'
                if language == "Polish" and gender == "male":
                    engine = 'standard'

                generate_audio(text, language_code=lang_code, voice=voice, output_file=file_name, engine=engine)
        else:
            print(f"No Amazon Polly configuration found for language: {language}")
    time2 = time.time()
    print(time2-time1)

if __name__ == "__main__":
    main()
