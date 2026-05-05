from dtaidistance import dtw
import librosa
import numpy as np

class AudioAligner:
    
    def __init__(self, sr=16000):
        self.sr = sr
    
    def extract_mfcc(self, y):
        """استخراج MFCC كبصمة صوتية للمقطع"""
        mfcc = librosa.feature.mfcc(
            y=y, 
            sr=self.sr,
            n_mfcc=13
        )
        return mfcc.T  # (frames, 13)
    
    def align_word_to_audio(
        self, 
        user_audio,      # الصوت الكامل للمستخدم
        reference_word,  # صوت الكلمة المرجعية المعزولة
        search_window    # نافذة البحث بالثواني
    ):
        """
        إيجاد موضع الكلمة في صوت المستخدم
        """
        user_mfcc = self.extract_mfcc(user_audio)
        ref_mfcc = self.extract_mfcc(reference_word)
        
        ref_len = len(ref_mfcc)
        best_score = float('inf')
        best_start = 0
        best_end = 0
        
        # البحث بنافذة منزلقة
        step = 5  # تتحرك 5 frames في كل مرة
        
        for start in range(0, len(user_mfcc) - ref_len, step):
            end = start + ref_len
            window = user_mfcc[start:end]
            
            # مقارنة DTW لكل MFCC coefficient
            total_distance = 0
            for coef in range(13):
                dist = dtw.distance(
                    window[:, coef],
                    ref_mfcc[:, coef]
                )
                total_distance += dist
            
            if total_distance < best_score:
                best_score = total_distance
                best_start = start
                best_end = end
        
        # تحويل من Frames إلى ثواني
        start_time = librosa.frames_to_time(
            best_start, sr=self.sr
        )
        end_time = librosa.frames_to_time(
            best_end, sr=self.sr
        )
        
        return {
            'start_time': start_time,
            'end_time': end_time,
            'confidence': 1 / (1 + best_score),  # 0 إلى 1
            'duration': end_time - start_time
        }