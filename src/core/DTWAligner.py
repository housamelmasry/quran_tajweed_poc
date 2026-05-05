# src/core/DTWAligner.py
import librosa
import numpy as np
from dtaidistance import dtw
from config.settings import settings

class DTWAligner:
    def __init__(self):
        self.sr          = settings.audio.sample_rate
        self.n_mfcc      = settings.feature.n_mfcc
        self.hop_length  = settings.feature.hop_length
        self.step        = settings.dtw.step
        self.dims        = settings.dtw.mfcc_dims_used

    def extract_features(self, y):
        if len(y) < self.hop_length:
            return None
        
        mfcc = librosa.feature.mfcc(
            y=y,
            sr=self.sr,
            n_mfcc=self.n_mfcc,
            hop_length=self.hop_length
        )
        # taking the first N dimensions and doing transpose
        return np.ascontiguousarray(mfcc[:self.dims, :].T, dtype=np.double)

    def compute_distance(self, window, reference):
        """
        Calculates the distance using librosa.sequence.dtw, which is faster
        and natively supports multidimensional features (MFCCs).
        """
        # librosa.dtw expects (dimensions, frames)
        # our features are (frames, dimensions)
        D, wp = librosa.sequence.dtw(X=window.T, Y=reference.T, metric='cosine')        
        # Return the normalized path distance
        return D[-1, -1] / len(wp)
        
    def find_best_match(self, user_feat, ref_feat):
        if user_feat is None or len(user_feat) < 5:
            return None

        ref_len  = len(ref_feat)
        user_len = len(user_feat)

        # in quran, words rarely exceed 1.5 times their original length
        # reducing the scale here is "the key" to the solution
        scale_factors = [0.8, 1.0, 1.2, 1.4] 
        
        best_score = float('inf')
        best_start = 0
        best_end   = ref_len

        # searching in a range of 3 seconds only from the start of the available segment
        max_search_frames = int(librosa.time_to_frames(3.0, sr=self.sr, hop_length=self.hop_length))
        search_range = min(user_len, max_search_frames)

        for scale in scale_factors:
            win_len = int(ref_len * scale)
            if win_len < 5 or win_len > user_len:
                continue

            for start in range(0, search_range - win_len + 1, self.step):
                window = user_feat[start:start + win_len]
                
                # the distance is already normalized inside compute_distance
                score = self.compute_distance(window, ref_feat)

                if score < best_score:
                    best_score = score
                    best_start = start
                    best_end   = start + win_len

        return best_start, best_end, best_score

    def align_word(self, user_audio, ref_audio):
        user_feat = self.extract_features(user_audio)
        ref_feat  = self.extract_features(ref_audio)

        if user_feat is None or ref_feat is None:
            return None

        result = self.find_best_match(user_feat, ref_feat)
        if result is None: return None

        start, end, score = result

        start_time = librosa.frames_to_time(start, sr=self.sr, hop_length=self.hop_length)
        end_time   = librosa.frames_to_time(end, sr=self.sr, hop_length=self.hop_length)

        # because we use cosine, the score will be between 0 and 1 approximately (or slightly more)
        # 0.4 here is an experimental value, you can modify it
        confidence = max(0.0, min(1.0, 1.0 - (score / 0.4))) 

        return {
            "start_time": round(start_time, 3),
            "end_time":   round(end_time, 3),
            "duration":   round(end_time - start_time, 3),
            "confidence": round(confidence, 3)
        }

    def align_sequence(self, user_audio, references):
        results = []
        offset_time = 0.0
        
        # simple buffer (0.2 seconds) for slight overlap between words to ensure no loss of starts
        buffer_time = 0.2 

        for ref in references:
            start_sample = max(0, int((offset_time - buffer_time) * self.sr))
            user_slice = user_audio[start_sample:]

            if len(user_slice) < self.sr * 0.1: # less than 100ms
                print(f"   ⚠️  Skipping {ref['word']}: No audio left.")
                results.append(self._empty_result(ref['word']))
                continue

            print(f"   🔍 Aligning: {ref['word']:15} (Remaining: {len(user_slice)/self.sr:.1f}s)")

            alignment = self.align_word(user_slice, ref["audio"])

            if alignment is None or alignment['confidence'] < 0.1:
                results.append(self._empty_result(ref['word']))
                # don't move the offset in case of failure to give the next word a chance to search
                continue

            # correcting the time based on the offset and the buffer
            actual_start = max(0, alignment["start_time"] + (offset_time - buffer_time))
            actual_end   = alignment["end_time"] + (offset_time - buffer_time)

            alignment.update({
                "start_time": round(actual_start, 3),
                "end_time":   round(actual_end, 3),
                "word":       ref["word"],
                "found":      True
            })

            results.append(alignment)
            offset_time = actual_end 

        return results

    def _empty_result(self, word):
        return {
            "word": word, "found": False, "confidence": 0,
            "start_time": None, "end_time": None, "duration": None
        }