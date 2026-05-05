# quick_test.py
import librosa
import numpy as np
from src.DTWAligner import DTWAligner

DTWAligner = DTWAligner()

# تحميل الصوتين
user, sr  = librosa.load("audio/user/test1.wav", sr=22050, mono=True)
ref_bismi, _ = librosa.load(
    "audio/reference/words/001_001_001.mp3", 
    sr=22050, mono=True
)
ref_allah, _ = librosa.load(
    "audio/reference/words/001_001_002.mp3", 
    sr=22050, mono=True
)
ref_rahman, _ = librosa.load(
    "audio/reference/words/001_001_003.mp3", 
    sr=22050, mono=True
)
ref_raheem, _ = librosa.load(
    "audio/reference/words/001_001_004.mp3", 
    sr=22050, mono=True
)

refs = [
    {"word": "بِسْمِ",        "audio": ref_bismi},
    {"word": "اللَّهِ",       "audio": ref_allah},
    {"word": "الرَّحْمَٰنِ", "audio": ref_rahman},
    {"word": "الرَّحِيمِ",   "audio": ref_raheem},
]

results = DTWAligner.align_sequence(user, refs)

print("\nResults after fix:")
for r in results:
    if r["found"]:
        print(
            f"✅ {r['word']:15} "
            f"{r['start_time']:.2f}s → {r['end_time']:.2f}s "
            f"conf={r['confidence']:.0%}"
        )
    else:
        print(f"❌ {r['word']:15} Not found")