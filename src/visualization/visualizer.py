import librosa
import librosa.display
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from config.settings import settings
import numpy as np

class Visualizer:
    
    def __init__(self, sr=16000):
        self.sr = sr
    
    def plot_alignment_results(
        self, 
        user_audio, 
        alignment_results,
        madd_evaluations
    ):
        """
        Comprehensive plot showing:
        - Waveform with word positions
        - Evaluation result for each Madd
        """
        fig, axes = plt.subplots(3, 1, figsize=(14, 10))
        fig.suptitle(
            'Recitation Analysis — Surah Al-Fatiha',
            fontsize=14,
            fontweight='bold'
        )
        
        # ── First Plot: Waveform with Word Positions ──
        ax1 = axes[0]
        librosa.display.waveshow(
            user_audio,
            sr=self.sr,
            ax=ax1,
            color='steelblue',
            alpha=0.7
        )
        ax1.set_title('Waveform with Word Alignment')
        ax1.set_xlabel('Time (seconds)')
        
        # Word region coloring
        colors = {
            'Correct': '#2ecc71',  # Green
            'Short':   '#e67e22',  # Orange
            'Long':    '#3498db',  # Blue
            'Error':   '#e74c3c'   # Red
        }
        
        for result in alignment_results:
            if not result['found']:
                continue
            
            # Find Madd evaluation for this word
            madd_eval = next(
                (m for m in madd_evaluations 
                 if m['word'] == result['word']),
                None
            )
            
            color = '#95a5a6'  # Gray — No Madd
            label = result['word']
            
            if madd_eval:
                status = madd_eval['evaluation']['status']
                color  = colors.get(status, '#95a5a6')
                label  = (
                    f"{result['word']}\n"
                    f"{madd_eval['actual']}/"
                    f"{madd_eval['required']} Harakah"
                )
            
            ax1.axvspan(
                result['start_time'],
                result['end_time'],
                alpha=0.3,
                color=color
            )
            ax1.text(
                (result['start_time'] + result['end_time']) / 2,
                ax1.get_ylim()[1] * 0.8,
                label,
                ha='center',
                fontsize=8
            )
        
        # ── Second Plot: RMS Energy ──
        ax2 = axes[1]
        rms = librosa.feature.rms(
            y=user_audio,
            frame_length=512,
            hop_length=128
        )[0]
        times = librosa.frames_to_time(
            np.arange(len(rms)),
            sr=self.sr,
            hop_length=128
        )
        ax2.plot(times, rms, color='darkorange', linewidth=1.5)
        ax2.set_title('RMS Energy — Volume Level')
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('RMS')
        ax2.grid(True, alpha=0.3)
        
        # ── Third Plot: Madd Evaluation Results ──
        ax3 = axes[2]
        
        words   = [m['word']     for m in madd_evaluations]
        actual  = [m['actual']   for m in madd_evaluations]
        
        # Required — Take the midpoint of the range
        required = []
        for m in madd_evaluations:
            req = m['required']
            if isinstance(req, str) and '-' in req:
                mn, mx = req.split('-')
                required.append(
                    (float(mn) + float(mx)) / 2
                )
            else:
                required.append(float(req))
        
        x = np.arange(len(words))
        w = 0.35
        
        bars1 = ax3.bar(
            x - w/2, required,
            w, label='Required',
            color='steelblue', alpha=0.8
        )
        bars2 = ax3.bar(
            x + w/2, actual,
            w, label='Actual',
            color=[
                colors.get(
                    m['evaluation']['status'],
                    '#95a5a6'
                )
                for m in madd_evaluations
            ],
            alpha=0.8
        )
        
        ax3.set_title('Madd Comparison — Required vs Actual')
        ax3.set_xticks(x)
        ax3.set_xticklabels(words, fontsize=9)
        ax3.set_ylabel('Harakaat')
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Color Legend
        patches = [
            mpatches.Patch(
                color=c, label=s
            )
            for s, c in colors.items()
        ]
        ax3.legend(
            handles=patches,
            loc='upper right',
            fontsize=8
        )
        
        plt.tight_layout()
        plt.savefig(
            settings.visualization.save_path,
            dpi=settings.visualization.dpi
        )
        # plt.show()
        print(f"✅ Plot saved to {settings.visualization.save_path}")