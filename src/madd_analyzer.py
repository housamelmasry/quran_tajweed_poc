import numpy as np

class MaddAnalyzer:
    
    # هامش القبول
    ACCEPTANCE_MARGIN = 0.5  # نصف حركة
    
    def calculate_harakah_duration(self, segments):
        """
        حساب متوسط زمن الحركة الواحدة
        من الحركات القصيرة المجاورة
        """
        durations = [s['duration'] for s in segments]
        
        # الحركات القصيرة = تحت الـ Percentile 40
        threshold = np.percentile(durations, 40)
        short_durations = [d for d in durations 
                          if d <= threshold]
        
        if not short_durations:
            return np.mean(durations)
            
        return np.mean(short_durations)
    
    def measure_madd(self, segment, harakah_duration):
        """
        قياس عدد الحركات الفعلية في المد
        """
        actual_harakaat = segment['duration'] / harakah_duration
        return round(actual_harakaat, 2)
    
    def evaluate_madd(self, actual, required_min, required_max=None):
        """
        الحكم على المد
        """
        if required_max is None:
            required_max = required_min
        
        # داخل الهامش
        if (required_min - self.ACCEPTANCE_MARGIN 
                <= actual <= 
                required_max + self.ACCEPTANCE_MARGIN):
            return {
                'status': 'صحيح',
                'severity': None,
                'difference': 0
            }
        
        # نقصان
        elif actual < required_min - self.ACCEPTANCE_MARGIN:
            diff = required_min - actual
            return {
                'status': 'نقصان',
                'severity': 'جسيم' if diff > 1 else 'بسيط',
                'difference': round(diff, 2)
            }
        
        # زيادة
        else:
            diff = actual - required_max
            return {
                'status': 'زيادة',
                'severity': 'جسيم' if diff > 1 else 'بسيط',
                'difference': round(diff, 2)
            }