import os
import sys
import librosa
import numpy as np

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def debug_audio(user_path, ref_dir):
    
    print("=" * 50)
    print("DEBUG — Audio Analysis")
    print("=" * 50)
    
    # check audio user 
    y_user, sr = librosa.load(user_path, sr=None, mono=True)
    print(f"\n📁 User Audio:")
    print(f"   Duration:    {len(y_user)/sr:.2f}s")
    print(f"   Sample Rate: {sr}Hz")
    print(f"   Samples:     {len(y_user)}")
    
    # check audio ref words
    words = [
        "001_001_001.mp3",
        "001_001_002.mp3", 
        "001_001_003.mp3",
        "001_001_004.mp3"
    ]
    labels = ["بِسْمِ", "اللَّهِ", "الرَّحْمَٰنِ", "الرَّحِيمِ"]
    
    print(f"\n📁 Reference Words:")
    total_ref_duration = 0
    for f, label in zip(words, labels):
        path = f"{ref_dir}/{f}"
        y, sr_r = librosa.load(path, sr=None, mono=True)
        dur = len(y)/sr_r
        total_ref_duration += dur
        print(f"   {label:15} → {dur:.2f}s")
    
    print(f"\n   Total reference duration: {total_ref_duration:.2f}s")
    print(f"   User audio duration:      {len(y_user)/sr:.2f}s")
    
    if len(y_user)/sr < total_ref_duration * 0.7:
        print("\n⚠️  WARNING: User audio is too short!")
        print("   The recording may be incomplete.")
    else:
        print("\n✅ Duration looks reasonable")
    
    # check audio level
    y_norm, _ = librosa.load(user_path, sr=22050, mono=True)
    rms = np.sqrt(np.mean(y_norm**2))
    print(f"\n📊 Audio Level (RMS): {rms:.4f}")
    if rms < 0.01:
        print("   ⚠️  Very quiet — possible silence or bad recording")
    elif rms > 0.5:
        print("   ⚠️  Very loud — possible clipping")
    else:
        print("   ✅ Level is good")

if __name__ == "__main__":
    debug_audio(
        user_path="audio/user/test1.wav",
        ref_dir="audio/reference/words"
    )