from resemble import Resemble
import requests
Resemble.api_key('')


projects = Resemble.v2.projects.all(1, 10)
if 'items' in projects and projects['items']:
    project_uuid = projects['items'][0]['uuid']
else:
    raise ValueError("No projects found in your Resemble AI account.")

# Fetch all voices and get the first voice UUID
voices = Resemble.v2.voices.all(1, 10)
if 'items' in voices and voices['items']:
    voice_uuid = voices['items'][0]['uuid']
else:
    raise ValueError("No voices found in your Resemble AI account.")


body = """I'm using AI to generate audio, creating a wide range of sounds through the power of code.
From music to speech, it all flows seamlessly, crafting voices and sounds that feel natural.
By leveraging sophisticated algorithms, we can bring various audio experiences to life, whether it's a voice or a melody.
The magic of AI unlocks endless possibilities, allowing for creative freedom and innovation in sound production.
It’s an exciting way to push the boundaries of what’s possible in audio."""


response = Resemble.v2.clips.create_sync(
    project_uuid,
    voice_uuid,
    body,
    title=None,
    sample_rate=None,
    output_format=None,
    precision=None,
    include_timestamps=None,
    is_archived=None,
    raw=None
)

if 'audio_src' in response:
    audio_url = response['audio_src']
    print("Generated Audio URL:", audio_url)

    audio_response = requests.get(audio_url)
    if audio_response.status_code == 200:
        with open("output_speech.mp3", "wb") as file:
            file.write(audio_response.content)
        print("Audio saved as output_speech.mp3")
    else:
        print("Error downloading the audio:", audio_response.status_code)
else:
    print("Error: 'audio_src' not found in response", response)