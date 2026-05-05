import librosa
import numpy as np
import soundfile as sf
from config.settings import settings


class AudioProcessor:
    
    def __init__(self):
        self.target_sr = settings.audio.sample_rate
    
    def load_and_clean(self, file_path):
        """
        Load and clean audio file.
        """
        # Load with target Sample Rate
        y, sr = librosa.load(
            file_path, 
            sr=self.target_sr,
            mono=True  # Automatically convert to Mono
        )
        
        # Trim silence from beginning and end
        y, _ = librosa.effects.trim(
            y, 
            top_db=settings.audio.trim_db
        )
        
        # Normalize
        y = librosa.util.normalize(y)
        
        return y, self.target_sr
    
    def get_rms_frames(self, y, frame_length=160, hop_length=80):
        """
        Calculate RMS for each frame (every 10ms).
        """
        rms = librosa.feature.rms(
            y=y,
            frame_length=frame_length,
            hop_length=hop_length
        )[0]
        
        return rms