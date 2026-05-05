import librosa
import numpy as np

class OnsetDetector:
    
    def __init__(self, sr=16000):
        self.sr = sr
    
    def detect_onsets(self, y):
        """
        كشف بداية كل وحدة صوتية
        """
        # Onset Detection
        onset_frames = librosa.onset.onset_detect(
            y=y,
            sr=self.sr,
            wait=1,         # الحد الأدنى بين Onsets
            pre_avg=3,
            post_avg=3,
            pre_max=3,
            post_max=3
        )
        
        # تحويل من Frames إلى ثواني
        onset_times = librosa.frames_to_time(
            onset_frames, 
            sr=self.sr
        )
        
        return onset_times
    
    def get_sound_segments(self, y, onset_times):
        """
        تحديد بداية ونهاية كل مقطع صوتي
        """
        segments = []
        samples = librosa.time_to_samples(
            onset_times, 
            sr=self.sr
        )
        
        for i in range(len(samples)):
            start = samples[i]
            # النهاية = بداية المقطع التالي أو نهاية الملف
            end = samples[i + 1] if i + 1 < len(samples) \
                  else len(y)
            
            segments.append({
                'start_sample': start,
                'end_sample': end,
                'start_time': onset_times[i],
                'end_time': end / self.sr,
                'duration': (end - start) / self.sr
            })
        
        return segments