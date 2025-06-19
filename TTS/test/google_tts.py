# -*- coding: utf-8 -*-

import os
import time 
from google.cloud import texttospeech
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file("iyovia-ai-prod-aab1ff6e038c.json")
client = texttospeech.TextToSpeechClient(credentials=credentials)
output_dir = 'google_voices'
os.makedirs(output_dir , exist_ok=True)



# client = texttospeech.TextToSpeechClient()


# en: "English",
# ja: "Japanese",
# es: "Spanish",
# de: "German",
# it: "Italian",
# fr: "French",
# pt: "Portuguese",
# ar: "Arabic",
# ru: "Russian",
# pl: "Polish"

#For the Male voice, please use Chirp 3 Orus. For the Female voice please use Chirp 3 Kore. Use these voices for all languages.


en_male     = ['en-US-Casual-K' ,'en-US-Chirp-HD-D' , 'en-US-Chirp3-HD-Charon' , 'en-US-Chirp3-HD-Fenrir', 'en-US-Chirp3-HD-Orus',
                'en-US-Chirp3-HD-Puck' ,'en-US-Neural2-A' , 'en-US-Neural2-D' , 'en-US-Neural2-I' ,'en-US-Neural2-J' , 'en-US-News-N',
                'en-US-Polyglot-1' , 'en-US-Standard-A' , 'en-US-Standard-B' ,'en-US-Standard-D' , 'en-US-Standard-I', 'en-US-Standard-J',
                'en-US-Studio-Q' , 'en-US-Wavenet-A', 'en-US-Wavenet-B', 'en-US-Wavenet-D', 'en-US-Wavenet-I' , 'en-US-Wavenet-J'
                ]

en_female   = ['en-US-Chirp-HD-F' , 'en-US-Chirp-HD-O' , 'en-US-Chirp3-HD-Aoede' , 'en-US-Chirp3-HD-Kore' ,'en-US-Chirp3-HD-Leda',
                'en-US-Chirp3-HD-Zephyr' , 'en-US-Neural2-C' ,'en-US-Neural2-E' , 'en-US-Neural2-F' ,'en-US-Neural2-G',
                'en-US-Neural2-H' , 'en-US-News-K' ,'en-US-News-L' , 'en-US-Standard-C' , 'en-US-Standard-E', 'en-US-Standard-F',
                'en-US-Standard-G' , 'en-US-Standard-H' ,'en-US-Studio-O' , 'en-US-Wavenet-C', 'en-US-Wavenet-E' , 'en-US-Wavenet-F',
                'en-US-Wavenet-G', 'en-US-Wavenet-H'
                ]


ja_male     = [ 'ja-JP-Chirp3-HD-Charon' , 'ja-JP-Chirp3-HD-Fenrir' , 'ja-JP-Chirp3-HD-Orus' , 'ja-JP-Chirp3-HD-Puck' ,
                'ja-JP-Neural2-C' , 'ja-JP-Neural2-D', 'ja-JP-Standard-C' ,'ja-JP-Standard-D' , 'ja-JP-Wavenet-C' , 'ja-JP-Wavenet-D'
                ]

ja_female   = [ 'ja-JP-Chirp3-HD-Aoede' , 'ja-JP-Chirp3-HD-Kore' , 'ja-JP-Chirp3-HD-Leda' ,'ja-JP-Chirp3-HD-Zephyr' ,
                'ja-JP-Neural2-B' , 'ja-JP-Standard-A' , 'ja-JP-Standard-A' , 'ja-JP-Wavenet-A' , 'ja-JP-Wavenet-B'
                ]


es_male     = [ 'es-ES-Chirp-HD-D' , 'es-ES-Chirp3-HD-Charon' , 'es-ES-Chirp3-HD-Fenrir' ,'es-ES-Chirp3-HD-Orus' , 'es-ES-Chirp3-HD-Puck',
                'es-ES-Neural2-F' , 'es-ES-Neural2-G' , 'es-ES-Polyglot-1' , 'es-ES-Standard-B' , 'es-ES-Standard-E' , 'es-ES-Standard-G',
                'es-ES-Studio-F' , 'es-ES-Wavenet-B' , 'es-ES-Wavenet-E' , 'es-ES-Wavenet-G'
                ]

es_female   = [ 'es-ES-Chirp-HD-F' , 'es-ES-Chirp-HD-O' , 'es-ES-Chirp3-HD-Aoede' , 'es-ES-Chirp3-HD-Kore' , 'es-ES-Chirp3-HD-Leda',
                'es-ES-Chirp3-HD-Zephyr' , 'es-ES-Neural2-A' , 'es-ES-Neural2-E' , 'es-ES-Neural2-H' , 'es-ES-Standard-A' , 'es-ES-Standard-C' ,
                'es-ES-Standard-D' , 'es-ES-Standard-F' , 'es-ES-Standard-H' , 'es-ES-Studio-C'  , 'es-ES-Wavenet-C' , 'es-ES-Wavenet-D' ,
                'es-ES-Wavenet-F' , 'es-ES-Wavenet-H'
                ]


de_male     = ['de-DE-Chirp-HD-D' , 'de-DE-Chirp3-HD-Charon' , 'de-DE-Chirp3-HD-Fenrir' , 'de-DE-Chirp3-HD-Orus' , 'de-DE-Chirp3-HD-Puck',
               'de-DE-Neural2-H' , 'de-DE-Polyglot-1' , 'de-DE-Standard-B'  , 'de-DE-Standard-D'  , 'de-DE-Standard-E' , 'de-DE-Standard-H',
               'de-DE-Studio-B' , 'de-DE-Wavenet-B' , 'de-DE-Wavenet-D' , 'de-DE-Wavenet-E' , 'de-DE-Wavenet-H'
                ]

de_female   = ['de-DE-Chirp-HD-F' , 'de-DE-Chirp-HD-O' , 'de-DE-Chirp3-HD-Aoede' , 'de-DE-Chirp3-HD-Kore', 'de-DE-Chirp3-HD-Leda' , 'de-DE-Chirp3-HD-Zephyr',
               'de-DE-Neural2-G'  , 'de-DE-Standard-A'  , 'de-DE-Standard-C'  , 'de-DE-Standard-F'  , 'de-DE-Standard-G' , 'de-DE-Studio-C' ,
               'de-DE-Wavenet-A' , 'de-DE-Wavenet-C' , 'de-DE-Wavenet-F' , 'de-DE-Wavenet-G'
                ]


it_male     = ['it-IT-Chirp-HD-D' , 'it-IT-Chirp3-HD-Charon' ,'it-IT-Chirp3-HD-Fenrir' ,'it-IT-Chirp3-HD-Orus' ,'it-IT-Chirp3-HD-Puck' ,
               'it-IT-Neural2-F' , 'it-IT-Standard-C', 'it-IT-Standard-D' , 'it-IT-Standard-F' ,
                'it-IT-Wavenet-C' , 'it-IT-Wavenet-D' , 'it-IT-Wavenet-F'
                ]

it_female = ['it-IT-Chirp-HD-F' , 'it-IT-Chirp-HD-O' , 'it-IT-Chirp3-HD-Aoede' ,'it-IT-Chirp3-HD-Kore' ,'it-IT-Chirp3-HD-Leda' ,
             'it-IT-Chirp3-HD-Zephyr' ,'it-IT-Neural2-A' ,'it-IT-Neural2-E' , 'it-IT-Standard-A', 'it-IT-Standard-B', 
             'it-IT-Standard-E' , 'it-IT-Wavenet-A' , 'it-IT-Wavenet-B' , 'it-IT-Wavenet-E'
                ]


fr_male   = ['fr-FR-Chirp-HD-D' ,'fr-FR-Chirp3-HD-Charon' , 'fr-FR-Chirp3-HD-Fenrir' , 'fr-FR-Chirp3-HD-Orus' , 'fr-FR-Chirp3-HD-Puck',
             'fr-FR-Neural2-G'  , 'fr-FR-Polyglot-1' , 'fr-FR-Standard-B', 'fr-FR-Standard-D', 'fr-FR-Standard-G' , 'fr-FR-Studio-D',
             'fr-FR-Wavenet-B' ,'fr-FR-Wavenet-D' ,'fr-FR-Wavenet-G'
                ]

fr_female = ['fr-FR-Chirp-HD-F' ,'fr-FR-Chirp-HD-O' ,'fr-FR-Chirp3-HD-Aoede' ,'fr-FR-Chirp3-HD-Kore' , 'fr-FR-Chirp3-HD-Leda' ,
             'fr-FR-Chirp3-HD-Zephyr' , 'fr-FR-Neural2-F' , 'fr-FR-Standard-A', 'fr-FR-Standard-C', 'fr-FR-Standard-E',
             'fr-FR-Standard-F', 'fr-FR-Studio-A' ,'fr-FR-Wavenet-A' ,'fr-FR-Wavenet-C' ,'fr-FR-Wavenet-E' ,
             'fr-FR-Wavenet-F' 
                ]


pt_male   = ['pt-PT-Standard-B' , 'pt-PT-Standard-C' , 'pt-PT-Standard-F' , 'pt-PT-Wavenet-B' , 'pt-PT-Wavenet-C' ,
              'pt-PT-Wavenet-F'
            ]

pt_female = ['pt-PT-Standard-A' , 'pt-PT-Standard-D' , 'pt-PT-Standard-E' , 'pt-PT-Wavenet-A' , 'pt-PT-Wavenet-D' , 
             'pt-PT-Wavenet-E'
            ]


ar_male   = ['ar-XA-Chirp3-HD-Charon' , 'ar-XA-Chirp3-HD-Fenrir' , 'ar-XA-Chirp3-HD-Orus' , 'ar-XA-Chirp3-HD-Puck',
             'ar-XA-Standard-B' , 'ar-XA-Standard-C' , 'ar-XA-Wavenet-B' , 'ar-XA-Wavenet-C'
            ]

ar_female = ['ar-XA-Chirp3-HD-Aoede' , 'ar-XA-Chirp3-HD-Kore' , 'ar-XA-Chirp3-HD-Leda' , 'ar-XA-Chirp3-HD-Zephyr',
             'ar-XA-Standard-D' , 'ar-XA-Standard-D' , 'ar-XA-Wavenet-A' , 'ar-XA-Wavenet-D'
            ]


ru_male   = ['ru-RU-Chirp3-HD-Charon' , 'ru-RU-Chirp3-HD-Fenrir' , 'ru-RU-Chirp3-HD-Orus' , 'ru-RU-Chirp3-HD-Puck',
             'ru-RU-Standard-B' , 'ru-RU-Standard-D' , 'ru-RU-Wavenet-B' , 'ru-RU-Wavenet-D'

            ]

ru_female = ['ru-RU-Chirp3-HD-Aoede' , 'ru-RU-Chirp3-HD-Kore' , 'ru-RU-Chirp3-HD-Leda' , 'ru-RU-Chirp3-HD-Zephyr',
             'ru-RU-Standard-A' , 'ru-RU-Standard-C' ,'ru-RU-Standard-E' ,'ru-RU-Wavenet-A' , 'ru-RU-Wavenet-C' ,
             'ru-RU-Wavenet-E'
            ]

pl_male   = ['pl-PL-Chirp3-HD-Charon' , 'pl-PL-Chirp3-HD-Fenrir' , 'pl-PL-Chirp3-HD-Orus' , 'pl-PL-Chirp3-HD-Puck',
             'pl-PL-Standard-B' , 'pl-PL-Standard-C' , 'pl-PL-Standard-G' , 'pl-PL-Wavenet-B' , 'pl-PL-Wavenet-C',
             'pl-PL-Wavenet-G'
            ]

pl_female = ['pl-PL-Chirp3-HD-Aoede' , 'pl-PL-Chirp3-HD-Kore' , 'pl-PL-Chirp3-HD-Leda' , 'pl-PL-Chirp3-HD-Zephyr',
             'pl-PL-Standard-A' , 'pl-PL-Standard-D' , 'pl-PL-Standard-E' , 'pl-PL-Standard-F',
             'pl-PL-Wavenet-A' , 'pl-PL-Wavenet-D' , 'pl-PL-Wavenet-E' , 'pl-PL-Wavenet-F'
            ]




def synthesize_text(text, voice_name , code):
    start = time.time()
    synthesis_input = texttospeech.SynthesisInput(text=text)


    voice = texttospeech.VoiceSelectionParams(
        name=voice_name,
        language_code=code
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    taken_time = time.time() - start
    return response.audio_content , taken_time

gender_dict_en = {"en_male": en_male, "en_female": en_female}
gender_dict_ja = {"ja_male": ja_male, "ja_female": ja_female}
gender_dict_es = {"es_male": es_male, "es_female": es_female}
gender_dict_de = {"de_male": de_male, "de_female": de_female}
gender_dict_it = {"it_male": it_male, "it_female": it_female}
gender_dict_fr = {"fr_male": fr_male, "fr_female": fr_female}
gender_dict_pt = {"pt_male": pt_male, "pt_female": pt_female}
gender_dict_ar = {"ar_male": ar_male, "ar_female": ar_female}
gender_dict_ru = {"ru_male": ru_male, "ru_female": ru_female}
gender_dict_pl = {"pl_male": pl_male, "pl_female": pl_female}


text_en = "I'm using AI to generate audio, creating a wide range of sounds through the power of code. From music to speech, it all flows seamlessly, crafting voices and sounds that feel natural. By leveraging sophisticated algorithms, we can bring various audio experiences to life, whether it's a voice or a melody. The magic of AI unlocks endless possibilities, allowing for creative freedom and innovation in sound production. It’s an exciting way to push the boundaries of what’s possible in audio."
text_ja = "私はAIを使ってオーディオを生成し、コードの力で多様な音を生み出しています。音楽から音声まで、すべてがシームレスに流れ、自然に感じられる声や音を作り出します。高度なアルゴリズムを活用することで、声やメロディーなど、さまざまなオーディオ体験を実現できます。AIの魔法が無限の可能性を解き放ち、音の制作における創造の自由と革新をもたらします。これは、オーディオの可能性を押し広げるエキサイティングな方法です。"
text_es = "Estoy usando IA para generar audio, creando una amplia gama de sonidos a través del poder del código. Desde música hasta habla, todo fluye sin problemas, dando vida a voces y sonidos que se sienten naturales. Al aprovechar algoritmos sofisticados, podemos crear diversas experiencias de audio, ya sea una voz o una melodía. La magia de la IA desbloquea posibilidades infinitas, permitiendo una libertad creativa e innovación en la producción de sonido. Es una forma emocionante de ampliar los límites de lo que es posible en el audio."
text_de = "Ich nutze KI zur Audiogenerierung und erschaffe eine Vielzahl von Klängen durch die Kraft des Codes. Von Musik bis Sprache fließt alles nahtlos zusammen und erzeugt Stimmen und Klänge, die natürlich wirken. Durch den Einsatz ausgefeilter Algorithmen können wir verschiedene Audioerlebnisse zum Leben erwecken, sei es eine Stimme oder eine Melodie. Die Magie der KI eröffnet endlose Möglichkeiten und ermöglicht kreative Freiheit sowie Innovation in der Klangproduktion. Es ist eine spannende Art, die Grenzen des Möglichen im Audio-Bereich zu erweitern."
text_it = "Sto usando l'intelligenza artificiale per generare audio, creando una vasta gamma di suoni attraverso la potenza del codice. Dalla musica al parlato, tutto scorre senza interruzioni, dando vita a voci e suoni che sembrano naturali. Sfruttando algoritmi sofisticati, possiamo creare diverse esperienze audio, che si tratti di una voce o di una melodia. La magia dell'IA sblocca infinite possibilità, permettendo libertà creativa e innovazione nella produzione sonora. È un modo entusiasmante per spingere i confini di ciò che è possibile nell'audio."
text_fr = "J'utilise l'intelligence artificielle pour générer de l'audio, créant une large gamme de sons grâce à la puissance du code. De la musique à la parole, tout s'enchaîne harmonieusement, donnant naissance à des voix et des sons qui semblent naturels. En exploitant des algorithmes sophistiqués, nous pouvons donner vie à diverses expériences sonores, qu'il s'agisse d'une voix ou d'une mélodie. La magie de l'IA ouvre des possibilités infinies, offrant une liberté créative et une innovation sans limites dans la production audio. C'est une manière passionnante de repousser les frontières du possible en matière de son."
text_pt = "Estou usando IA para gerar áudio, criando uma ampla variedade de sons por meio do poder do código. Da música à fala, tudo flui perfeitamente, criando vozes e sons que parecem naturais. Ao aproveitar algoritmos sofisticados, podemos dar vida a diversas experiências sonoras, seja uma voz ou uma melodia. A magia da IA desbloqueia possibilidades infinitas, permitindo liberdade criativa e inovação na produção de som. É uma maneira empolgante de expandir os limites do que é possível no áudio."
text_ar = "أنا أستخدم الذكاء الاصطناعي لإنشاء الصوت، وإنتاج مجموعة واسعة من الأصوات من خلال قوة البرمجة. من الموسيقى إلى الكلام، يتدفق كل شيء بسلاسة، مما يخلق أصواتًا وأصواتًا تبدو طبيعية. من خلال الاستفادة من الخوارزميات المتطورة، يمكننا إحياء تجارب صوتية متنوعة، سواء كانت صوتًا بشريًا أو لحنًا موسيقيًا. سحر الذكاء الاصطناعي يفتح آفاقًا لا حصر لها، مما يسمح بحرية إبداعية وابتكار في إنتاج الصوت. إنها طريقة مثيرة لدفع حدود ما هو ممكن في عالم الصوت."
text_ru = "Я использую ИИ для генерации аудио, создавая широкий спектр звуков с помощью кода. От музыки до речи — всё звучит естественно и плавно, формируя голоса и звуки, которые ощущаются живыми. Благодаря сложным алгоритмам мы можем воплощать в жизнь различные аудиовпечатления, будь то голос или мелодия. Магия ИИ открывает бесконечные возможности, позволяя творческой свободе и инновациям в создании звука. Это захватывающий способ раздвинуть границы возможного в аудиопроизводстве."
text_pl = "Używam sztucznej inteligencji do generowania dźwięku, tworząc szeroką gamę brzmień za pomocą kodu. Od muzyki po mowę – wszystko płynie płynnie, kreując głosy i dźwięki, które brzmią naturalnie. Wykorzystując zaawansowane algorytmy, możemy ożywiać różne doświadczenia dźwiękowe, czy to głos, czy melodię. Magia sztucznej inteligencji otwiera nieskończone możliwości, dając swobodę twórczą i innowacje w produkcji dźwięku. To ekscytujący sposób na przesuwanie granic tego, co jest możliwe w świecie audio."

# code_en = 'en-US'
# code_ja = 'ja-JP'
# code_es = 'es-ES'
# code_de = 'de-DE'
# code_it = 'it-IT'
# code_fr = 'fr-FR'
# code_pt = 'pt-PT'
# code_ar = 'ar-XA'
# code_ru = 'ru-RU'
# code_pl = 'pl-PL'


time_total = 0
voice_count = 0

for folder_name, voice_list in gender_dict_pl.items():
    folder_path = os.path.join(output_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    log_file_path = os.path.join(folder_path, f"{folder_name}.txt")

    with open(log_file_path, "w") as log_file:
        for voice in voice_list:
            audio_content, tt_time = synthesize_text(text_pl, voice, voice[:5])
            time_total += tt_time
            output_filename = f"{voice[6:]}.mp3"
            output_filepath = os.path.join(folder_path, output_filename)
            voice_count += 1

            with open(output_filepath, "wb") as out:
                out.write(audio_content)

            log_message = f"Audio file name: {output_filename} , and total time : {round(tt_time,2)}\n"
            print(log_message)
            log_file.write(log_message)


print(time_total)
print(time_total / voice_count)