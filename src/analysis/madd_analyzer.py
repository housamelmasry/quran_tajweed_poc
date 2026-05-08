# src/core/madd_analyzer.py
import numpy as np
import librosa

class MaddAnalyzer:
    
    ACCEPTANCE_MARGIN = 0.5 
    
    def calculate_harakah_duration(self, segments):
        """Calculate the average duration of a single harakah (vowel sound)"""
        if not segments:
            return 0.2 # Default value if calculation fails
            
        durations = [s['duration'] for s in segments if s['duration'] is not None]
        
        # Consider short words (like "Bismi" and "Allah") as reference for natural vowels
        threshold = np.percentile(durations, 50)
        short_durations = [d for d in durations if d <= threshold]
        
        if not short_durations:
            return np.mean(durations) / 2 # Assume word is 2 harakahs on average
            
        # Divide short word duration by 2 (roughly) to get single harakah duration
        return np.mean(short_durations) / 2

    def measure_madd_smart(self, audio_segment, sr, harakah_duration):
        """
        Measure lengthening based on audio energy (RMS) within the word segment.
        """
        if audio_segment is None or len(audio_segment) == 0:
            return 0
            
        # 1. Extract audio energy
        rms = librosa.feature.rms(y=audio_segment)[0]
        
        # 2. Identify segments with actual "lengthened sound" (above 25% of peak energy)
        # This ignores silence or consonants at the start and end of the word
        active_frames = np.where(rms > np.max(rms) * 0.25)[0]
        
        if len(active_frames) == 0:
            return 0
            
        # 3. Convert frames to seconds
        # Using hop_length=512 (librosa default)
        vowel_duration = librosa.frames_to_time(len(active_frames), sr=sr)
        
        # 4. Calculate number of harakaat
        actual_harakaat = vowel_duration / harakah_duration
        return round(actual_harakaat, 1)

    def evaluate_madd(self, actual, required_min, required_max=None):
        """Evaluate if the lengthening (Madd) is correct or not"""
        if required_max is None:
            required_max = required_min
        
        if (required_min - self.ACCEPTANCE_MARGIN <= actual <= required_max + self.ACCEPTANCE_MARGIN):
            return {'status': 'Correct', 'severity': None, 'difference': 0}
        
        elif actual < required_min - self.ACCEPTANCE_MARGIN:
            diff = required_min - actual
            return {'status': 'Short', 'severity': 'Major' if diff > 1.5 else 'Minor', 'difference': round(diff, 2)}
        
        else:
            diff = actual - required_max
            return {'status': 'Long', 'severity': 'Major' if diff > 1.5 else 'Minor', 'difference': round(diff, 2)}