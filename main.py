import librosa
import numpy as np
import json
import os
from src.audio_processor import AudioProcessor
from src.aligner        import WordAligner
from src.madd_analyzer  import MaddAnalyzer
from src.visualizer     import Visualizer

def load_word_references(words_dir, word_list):
    """
    تحميل الملفات الصوتية المرجعية لكل كلمة
    """
    processor = AudioProcessor()
    references = []
    
    for item in word_list:
        file_path = os.path.join(
            words_dir,
            item['file']  # اسم الملف من الـ JSON
        )
        
        if not os.path.exists(file_path):
            print(f"⚠️  ملف غير موجود: {file_path}")
            continue
        
        audio, _ = processor.load_and_clean(file_path)
        references.append({
            'word':  item['word'],
            'audio': audio
        })
    
    return references

def run_poc(user_audio_path, ayah_data, words_dir):
    
    os.makedirs('output', exist_ok=True)
    
    processor  = AudioProcessor()
    aligner    = WordAligner()
    analyzer   = MaddAnalyzer()
    visualizer = Visualizer()
    
    print("=" * 50)
    print("تحليل التلاوة — POC")
    print("=" * 50)
    
    # ١. تحميل صوت المستخدم
    print("\n١. تحميل الصوت...")
    user_audio, sr = processor.load_and_clean(user_audio_path)
    print(f"   مدة التسجيل: {len(user_audio)/sr:.2f} ثانية")
    
    # ٢. تحميل الكلمات المرجعية
    print("\n٢. تحميل الكلمات المرجعية...")
    references = load_word_references(
        words_dir,
        ayah_data['words']
    )
    print(f"   تم تحميل {len(references)} كلمة")
    
    # ٣. محاذاة الكلمات
    print("\n٣. محاذاة الكلمات...")
    alignment_results = aligner.align_all_words(
        user_audio,
        references
    )
    
    print("\n   النتائج:")
    for r in alignment_results:
        if r['found']:
            print(
                f"   ✅ {r['word']:15} "
                f"{r['start_time']:.2f}s → {r['end_time']:.2f}s "
                f"(ثقة: {r['confidence']:.0%})"
            )
        else:
            print(f"   ❌ {r['word']:15} لم يُعثر عليها")
    
    # ٤. تحليل المدود
    print("\n٤. تحليل المدود...")
    
    harakah_duration = analyzer.calculate_harakah_duration([
        {'duration': r['duration']}
        for r in alignment_results
        if r['found'] and r['duration']
    ])
    print(f"   زمن الحركة: {harakah_duration:.3f}s")
    
    madd_evaluations = []
    for madd in ayah_data['madood']:
        
        # إيجاد نتيجة المحاذاة للكلمة
        aligned = next(
            (r for r in alignment_results
             if r['word'] == madd['word'] and r['found']),
            None
        )
        
        if not aligned:
            print(f"   ⚠️  لم يتم العثور على: {madd['word']}")
            continue
        
        # قياس المد
        actual = analyzer.measure_madd(
            aligned,
            harakah_duration
        )
        
        # الحكم
        evaluation = analyzer.evaluate_madd(
            actual,
            required_min=madd.get(
                'harakaat',
                madd.get('harakaat_min')
            ),
            required_max=madd.get(
                'harakaat',
                madd.get('harakaat_max')
            )
        )
        
        madd_evaluations.append({
            'word':       madd['word'],
            'type':       madd['type'],
            'required':   madd.get(
                            'harakaat',
                            f"{madd.get('harakaat_min')}-"
                            f"{madd.get('harakaat_max')}"
                          ),
            'actual':     actual,
            'evaluation': evaluation
        })
        
        status_icon = {
            'صحيح':  '✅',
            'نقصان': '⚠️',
            'زيادة': '🔵',
        }.get(evaluation['status'], '❌')
        
        print(
            f"\n   {status_icon} {madd['word']}"
            f"\n      النوع:     {madd['type']}"
            f"\n      المطلوب:   {madd_evaluations[-1]['required']} حركات"
            f"\n      الفعلي:    {actual} حركات"
            f"\n      الحكم:     {evaluation['status']}"
            + (f" — {evaluation['severity']}"
               if evaluation['severity'] else "")
        )
    
    # ٥. الرسم البياني
    print("\n٥. إنشاء التقرير البصري...")
    visualizer.plot_alignment_results(
        user_audio,
        alignment_results,
        madd_evaluations
    )
    
    # ٦. النتيجة الإجمالية
    correct = sum(
        1 for m in madd_evaluations
        if m['evaluation']['status'] == 'صحيح'
    )
    total   = len(madd_evaluations)
    score   = round(correct / total * 100) if total else 0
    
    print("\n" + "=" * 50)
    print(f"النتيجة الإجمالية: {score}%")
    print(f"صحيح: {correct}/{total} مد")
    print("=" * 50)
    
    return {
        'alignment':  alignment_results,
        'madood':     madd_evaluations,
        'score':      score
    }

if __name__ == "__main__":
    
    with open('data/fatiha_madood.json', 'r',
              encoding='utf-8') as f:
        data = json.load(f)
    
    run_poc(
        user_audio_path = 'audio/user/test.wav',
        ayah_data       = data['ayat'][0],
        words_dir       = 'audio/reference/words'
    )