import numpy as np

class MaddAnalyzer:
    
    # Acceptance margin
    ACCEPTANCE_MARGIN = 0.5  # half a harakah
    
    def calculate_harakah_duration(self, segments):
        """
        Calculate the average duration of a single harakah
        based on nearby short harakahs.
        """
        durations = [s['duration'] for s in segments]
        
        # Short harakahs = below the 40th percentile
        threshold = np.percentile(durations, 40)
        short_durations = [d for d in durations 
                          if d <= threshold]
        
        if not short_durations:
            return np.mean(durations)
            
        return np.mean(short_durations)
    
    def measure_madd(self, segment, harakah_duration):
        """
        Measure the actual number of harakahs in a Madd (lengthening).
        """
        actual_harakaat = segment['duration'] / harakah_duration
        return round(actual_harakaat, 2)
    
    def evaluate_madd(self, actual, required_min, required_max=None):
        """
        Evaluate the Madd performance.
        """
        if required_max is None:
            required_max = required_min
        
        # Within margin
        if (required_min - self.ACCEPTANCE_MARGIN 
                <= actual <= 
                required_max + self.ACCEPTANCE_MARGIN):
            return {
                'status': 'Correct',
                'severity': None,
                'difference': 0
            }
        
        # Too short (Nuksan)
        elif actual < required_min - self.ACCEPTANCE_MARGIN:
            diff = required_min - actual
            return {
                'status': 'Short',
                'severity': 'Major' if diff > 1 else 'Minor',
                'difference': round(diff, 2)
            }
        
        # Too long (Ziyada)
        else:
            diff = actual - required_max
            return {
                'status': 'Long',
                'severity': 'Major' if diff > 1 else 'Minor',
                'difference': round(diff, 2)
            }