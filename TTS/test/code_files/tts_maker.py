# -*- coding: utf-8 -*-

from google.cloud import texttospeech
from google.oauth2 import service_account

class TextToSpeechSynthesizer:
    
    VOICE_MAP = {
        ('en', 'male'): 'en-US-Chirp3-HD-Orus',
        ('en', 'female'): 'en-US-Chirp3-HD-Kore',
        ('ja', 'male'): 'ja-JP-Chirp3-HD-Orus',
        ('ja', 'female'): 'ja-JP-Chirp3-HD-Kore',
        ('es', 'male'): 'es-ES-Chirp3-HD-Orus',
        ('es', 'female'): 'es-ES-Chirp3-HD-Kore',
        ('de', 'male'): 'de-DE-Chirp3-HD-Orus',
        ('de', 'female'): 'de-DE-Chirp3-HD-Kore',
        ('it', 'male'): 'it-IT-Chirp3-HD-Orus',
        ('it', 'female'): 'it-IT-Chirp3-HD-Kore',
        ('fr', 'male'): 'fr-FR-Chirp3-HD-Orus',
        ('fr', 'female'): 'fr-FR-Chirp3-HD-Kore',
        ('ar', 'male'): 'ar-XA-Chirp3-HD-Orus',
        ('ar', 'female'): 'ar-XA-Chirp3-HD-Kore',
        ('ru', 'male'): 'ru-RU-Chirp3-HD-Orus',
        ('ru', 'female'): 'ru-RU-Chirp3-HD-Kore',
        ('pl', 'male'): 'pl-PL-Chirp3-HD-Orus',
        ('pl', 'female'): 'pl-PL-Chirp3-HD-Kore',
        ('pt', 'male'): 'pt-PT-Standard-F',
        ('pt', 'female'): 'pt-PT-Standard-E'
    }

    def __init__(self, credentials_path: str):

        credentials = service_account.Credentials.from_service_account_file(credentials_path)
        self.client = texttospeech.TextToSpeechClient(credentials=credentials)

    def synthesize(self, text: str, language: str, gender: str) -> bytes:
 
        key = (language.lower(), gender.lower())
        if key not in self.VOICE_MAP:
            raise ValueError(f"No voice mapping found for language '{language}' and gender '{gender}'.")

        voice_name = self.VOICE_MAP[key]
        # Derive language code (e.g., 'en-US' from 'en-US-Chirp3-HD-Orus')
        language_code = "-".join(voice_name.split("-")[:2])

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice_params = texttospeech.VoiceSelectionParams(
            name=voice_name,
            language_code=language_code
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice_params,
            audio_config=audio_config
        )

        return response.audio_content





