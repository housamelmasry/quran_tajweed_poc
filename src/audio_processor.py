import librosa
import numpy as np
import soundfile as sf

class AudioProcessor:
    
    def __init__(self, target_sr=16000):
        self.target_sr = target_sr
    
    def load_and_clean(self, file_path):
        """
        تحميل الصوت وتنظيفه
        """
        # تحميل مع توحيد الـ Sample Rate
        y, sr = librosa.load(
            file_path, 
            sr=self.target_sr,
            mono=True  # تحويل تلقائي لـ Mono
        )
        
        # حذف الصمت من البداية والنهاية
        y, _ = librosa.effects.trim(
            y, 
            top_db=20  # كل ما هو أقل من 20db يُحذف
        )
        
        # Normalize
        y = librosa.util.normalize(y)
        
        return y, self.target_sr
    
    def get_rms_frames(self, y, frame_length=160, hop_length=80):
        """
        حساب RMS لكل Frame (كل 10ms)
        """
        rms = librosa.feature.rms(
            y=y,
            frame_length=frame_length,
            hop_length=hop_length
        )[0]
        
        return rms