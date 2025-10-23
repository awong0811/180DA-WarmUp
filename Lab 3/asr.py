import sounddevice as sd
from scipy.io.wavfile import write
import whisper

fs = 16000
seconds = 5

print("🎙️  Recording... Speak now!")
audio = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()
write("recording.wav", fs, audio)
print("✅ Saved as recording.wav")


model = whisper.load_model("tiny.en")
result = model.transcribe("recording.wav")
print(result["text"])
