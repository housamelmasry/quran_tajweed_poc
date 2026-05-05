import librosa
import numpy as np
from dtaidistance import dtw

class WordAligner:
    
    def __init__(self, sr=16000):
        self.sr = sr
    
    def extract_mfcc(self, y):
        mfcc = librosa.feature.mfcc(
            y=y,
            sr=self.sr,
            n_mfcc=13,
            hop_length=128
        )
        return mfcc.T  # (frames, 13)
    
    def find_word_in_audio(self, user_audio, ref_word_audio):
        """
        إيجاد موضع الكلمة المرجعية في صوت المستخدم
        يرجع: start_time, end_time, confidence
        """
        user_mfcc = self.extract_mfcc(user_audio)
        ref_mfcc  = self.extract_mfcc(ref_word_audio)
        
        ref_len    = len(ref_mfcc)
        best_score = float('inf')
        best_start = 0
        
        # نافذة البحث — تتحرك كل 5 frames
        step = 5
        search_end = len(user_mfcc) - ref_len
        
        if search_end <= 0:
            return None
        
        for start in range(0, search_end, step):
            window = user_mfcc[start:start + ref_len]
            
            # مقارنة DTW على كل الـ 13 معامل
            total_dist = sum(
                dtw.distance(
                    window[:, i],
                    ref_mfcc[:, i]
                )
                for i in range(13)
            )
            
            if total_dist < best_score:
                best_score = total_dist
                best_start = start
        
        best_end = best_start + ref_len
        
        start_time = librosa.frames_to_time(
            best_start,
            sr=self.sr,
            hop_length=128
        )
        end_time = librosa.frames_to_time(
            best_end,
            sr=self.sr,
            hop_length=128
        )
        
        confidence = round(1 / (1 + best_score / ref_len), 3)
        
        return {
            'start_time': round(start_time, 3),
            'end_time':   round(end_time, 3),
            'duration':   round(end_time - start_time, 3),
            'confidence': confidence
        }
    
    def align_all_words(self, user_audio, word_references):
        """
        محاذاة كل كلمات الآية بالترتيب
        
        word_references: قائمة مرتبة من
        {'word': 'الرحمن', 'audio': np.array(...)}
        """
        results     = []
        search_from = 0  # نبحث دائماً بعد الكلمة السابقة
        
        for ref in word_references:
            # قطع الصوت من موضع البحث فصاعداً
            user_slice = user_audio[
                int(search_from * self.sr):
            ]
            
            alignment = self.find_word_in_audio(
                user_slice,
                ref['audio']
            )
            
            if alignment is None:
                results.append({
                    'word':       ref['word'],
                    'found':      False,
                    'start_time': None,
                    'end_time':   None,
                    'duration':   None,
                    'confidence': 0
                })
                continue
            
            # تصحيح الوقت — نضيف الـ offset
            alignment['start_time'] += search_from
            alignment['end_time']   += search_from
            alignment['word']        = ref['word']
            alignment['found']       = True
            
            results.append(alignment)
            
            # الكلمة التالية تبدأ من نهاية الحالية
            search_from = alignment['end_time']
        
        return results