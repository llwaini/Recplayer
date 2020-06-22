from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_wav("recorded.wav")
play(sound)
