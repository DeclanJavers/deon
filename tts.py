from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play

# Function to convert text to speech and adjust speed
def speak(text, speed=1.3):
    output_path = "response.mp3"
    tts = gTTS(text=text, lang='en-US', tld='com', slow=False)
    tts.save(output_path)
    
    # Load the audio file and adjust the speed
    sound = AudioSegment.from_file(output_path)
    altered_speed_sound = sound.speedup(playback_speed=speed)
    
    # Play the altered audio
    play(altered_speed_sound)


