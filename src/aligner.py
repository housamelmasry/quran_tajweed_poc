import librosa
import numpy as np
from dtaidistance import dtw
from config.settings import settings



class DTWAligner:
    def __init__(self):
        self.sr = settings.audio.sample_rate
        self.n_mfcc = settings.feature.n_mfcc
        self.hop_length = settings.feature.hop_length
        self.step = settings.dtw.step
        self.dims = settings.dtw.mfcc_dims_used

    # ───────────────────────────────
    # Feature Extraction
    # ───────────────────────────────
    def extract_features(self, y):
        mfcc = librosa.feature.mfcc(
            y=y,
            sr=self.sr,
            n_mfcc=self.n_mfcc,
            hop_length=self.hop_length
        )
        return mfcc.T  # (frames, n_mfcc)

    # ───────────────────────────────
    # Distance Calculation
    # ───────────────────────────────
    def compute_distance(self, window, reference):
        """
        حساب المسافة بين نافذة من المستخدم والكلمة المرجعية
        """
        # تقليل الأبعاد لتحسين الأداء
        dims = min(self.dims, self.n_mfcc)

        total = 0
        for i in range(dims):
            total += dtw.distance(
                window[:, i],
                reference[:, i]
            )

        return total

    # ───────────────────────────────
    # Core Matching
    # ───────────────────────────────
    def find_best_match(self, user_feat, ref_feat):
        ref_len = len(ref_feat)

        if len(user_feat) < ref_len:
            return None

        best_score = float('inf')
        best_start = 0

        for start in range(0, len(user_feat) - ref_len, self.step):
            window = user_feat[start:start + ref_len]

            score = self.compute_distance(window, ref_feat)

            if score < best_score:
                best_score = score
                best_start = start

        best_end = best_start + ref_len

        return best_start, best_end, best_score

    # ───────────────────────────────
    # Public API: Align Single Word
    # ───────────────────────────────
    def align_word(self, user_audio, ref_audio):
        user_feat = self.extract_features(user_audio)
        ref_feat = self.extract_features(ref_audio)

        result = self.find_best_match(user_feat, ref_feat)

        if result is None:
            return None

        start, end, score = result

        start_time = librosa.frames_to_time(
            start,
            sr=self.sr,
            hop_length=self.hop_length
        )

        end_time = librosa.frames_to_time(
            end,
            sr=self.sr,
            hop_length=self.hop_length
        )

        confidence = 1 / (1 + score / len(ref_feat))

        return {
            "start_time": round(start_time, 3),
            "end_time": round(end_time, 3),
            "duration": round(end_time - start_time, 3),
            "confidence": round(confidence, 3)
        }

    # ───────────────────────────────
    # Public API: Align Sequence
    # ───────────────────────────────
    def align_sequence(self, user_audio, references):
        """
        references: [
            {"word": "الله", "audio": np.array(...)},
            ...
        ]
        """
        results = []
        offset_time = 0

        for ref in references:
            # نقطع الصوت من آخر موضع وصلنا له
            start_sample = int(offset_time * self.sr)
            user_slice = user_audio[start_sample:]

            alignment = self.align_word(
                user_slice,
                ref["audio"]
            )

            if alignment is None:
                results.append({
                    "word": ref["word"],
                    "found": False,
                    "confidence": 0
                })
                continue

            # تصحيح التوقيت
            alignment["start_time"] += offset_time
            alignment["end_time"] += offset_time
            alignment["word"] = ref["word"]
            alignment["found"] = True

            results.append(alignment)

            # تحديث مكان البحث
            offset_time = alignment["end_time"]

        return results