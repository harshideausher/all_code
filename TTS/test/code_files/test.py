from tts_maker import TextToSpeechSynthesizer



credentials_file = "iyovia-ai-prod-aab1ff6e038c.json"
synthesizer = TextToSpeechSynthesizer(credentials_file)

sample_text = "I'm using AI to generate audio, creating a wide range of sounds through the power of code."
language = "en"
gender = "male"


audio_content = synthesizer.synthesize(sample_text, language, gender)


output_filename = f"{language}_{gender}.mp3"
with open(output_filename, "wb") as out_file:
    out_file.write(audio_content)

print(f"Audio content saved to {output_filename}")



