import librosa
import librosa.display
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
        رسم شامل يوضح:
        - Waveform مع مواضع الكلمات
        - نتيجة كل مد
        """
        fig, axes = plt.subplots(3, 1, figsize=(14, 10))
        fig.suptitle(
            'تحليل التلاوة — سورة الفاتحة',
            fontsize=14,
            fontweight='bold'
        )
        
        # ── الرسم الأول: Waveform مع مواضع الكلمات ──
        ax1 = axes[0]
        librosa.display.waveshow(
            user_audio,
            sr=self.sr,
            ax=ax1,
            color='steelblue',
            alpha=0.7
        )
        ax1.set_title('الموجة الصوتية مع مواضع الكلمات')
        ax1.set_xlabel('الوقت (ثانية)')
        
        # تلوين مناطق الكلمات
        colors = {
            'صحيح':  '#2ecc71',  # أخضر
            'نقصان': '#e67e22',  # برتقالي
            'زيادة': '#3498db',  # أزرق
            'خطأ':   '#e74c3c'   # أحمر
        }
        
        for result in alignment_results:
            if not result['found']:
                continue
            
            # البحث عن نتيجة المد لهذه الكلمة
            madd_eval = next(
                (m for m in madd_evaluations 
                 if m['word'] == result['word']),
                None
            )
            
            color = '#95a5a6'  # رمادي — لا يوجد مد
            label = result['word']
            
            if madd_eval:
                status = madd_eval['evaluation']['status']
                color  = colors.get(status, '#95a5a6')
                label  = (
                    f"{result['word']}\n"
                    f"{madd_eval['actual']}/"
                    f"{madd_eval['required']} حركة"
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
        
        # ── الرسم الثاني: RMS Energy ──
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
        ax2.set_title('RMS Energy — مستوى الصوت')
        ax2.set_xlabel('الوقت (ثانية)')
        ax2.set_ylabel('RMS')
        ax2.grid(True, alpha=0.3)
        
        # ── الرسم الثالث: نتائج المدود ──
        ax3 = axes[2]
        
        words   = [m['word']     for m in madd_evaluations]
        actual  = [m['actual']   for m in madd_evaluations]
        
        # المطلوب — نأخذ القيمة الوسطى للنطاق
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
            w, label='المطلوب',
            color='steelblue', alpha=0.8
        )
        bars2 = ax3.bar(
            x + w/2, actual,
            w, label='الفعلي',
            color=[
                colors.get(
                    m['evaluation']['status'],
                    '#95a5a6'
                )
                for m in madd_evaluations
            ],
            alpha=0.8
        )
        
        ax3.set_title('مقارنة المدود — المطلوب vs الفعلي')
        ax3.set_xticks(x)
        ax3.set_xticklabels(words, fontsize=9)
        ax3.set_ylabel('عدد الحركات')
        ax3.legend()
        ax3.grid(True, alpha=0.3, axis='y')
        
        # Legend للألوان
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
            'output/analysis_result.png',
            dpi=150,
            bbox_inches='tight'
        )
        plt.show()
        print("✅ تم حفظ الرسم في output/analysis_result.png")