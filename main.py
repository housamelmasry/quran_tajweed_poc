import librosa
import numpy as np
import json
import os
import argparse
from src.core.audio_processor import AudioProcessor
from src.core.DTWAligner import DTWAligner
from src.analysis.madd_analyzer import MaddAnalyzer
from src.visualization.visualizer import Visualizer
from config.settings import settings

def load_word_references(words_dir, word_list):
    """
    Load reference audio files for each word
    """
    processor = AudioProcessor()
    references = []
    
    for item in word_list:
        file_path = os.path.join(
            words_dir,
            item['file']  # Filename from JSON
        )
        
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {file_path}")
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
    aligner    = DTWAligner()
    analyzer   = MaddAnalyzer()
    visualizer = Visualizer(sr=settings.audio.sample_rate)
    
    print("=" * 50)
    print("Recitation Analysis — POC")
    print("=" * 50)
    
    # 1. Load user audio
    print("\n1. Loading audio...")
    user_audio, sr = processor.load_and_clean(user_audio_path)
    print(f"   Recording duration: {len(user_audio)/sr:.2f} seconds")
    
    # 2. Load reference words
    print("\n2. Loading reference words...")
    references = load_word_references(
        words_dir,
        ayah_data['words']
    )
    print(f"   Loaded {len(references)} words")
    
    # 3. Word alignment
    print("\n3. Aligning words...")
    alignment_results = aligner.align_sequence(
        user_audio,
        references
    )
    
    print("\n   Results:")
    for r in alignment_results:
        if r['found']:
            print(
                f"   ✅ {r['word']:15} "
                f"{r['start_time']:.2f}s → {r['end_time']:.2f}s "
                f"(Confidence: {r['confidence']:.0%})"
            )
        else:
            print(f"   ❌ {r['word']:15} Not found")
    
    # 4. Madd (Lengthening) analysis
    print("\n4. Analyzing Madd (Lengthening)...")
    
    harakah_duration = analyzer.calculate_harakah_duration([
        {'duration': r['duration']}
        for r in alignment_results
        if r['found'] and r['duration']
    ])
    print(f"   Harakah duration: {harakah_duration:.3f}s")
    
    madd_evaluations = []
    for madd in ayah_data['madood']:
        
        # Find alignment result for the word
        aligned = next(
            (r for r in alignment_results
             if r['word'] == madd['word'] and r['found']),
            None
        )
        
        if not aligned:
            print(f"   ⚠️  Word not found: {madd['word']}")
            continue
        
        # Measure Madd
        actual = analyzer.measure_madd(
            aligned,
            harakah_duration
        )
        
        # Evaluate
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
            'Correct':  '✅',
            'Short':    '⚠️',
            'Long':     '🔵',
        }.get(evaluation['status'], '❌')
        
        print(
            f"\n   {status_icon} {madd['word']}"
            f"\n      Type:     {madd['type']}"
            f"\n      Required: {madd_evaluations[-1]['required']} Harakaat"
            f"\n      Actual:   {actual} Harakaat"
            f"\n      Status:   {evaluation['status']}"
            + (f" — {evaluation['severity']}"
               if evaluation['severity'] else "")
        )
    
    # 5. Visual report
    print("\n5. Generating visual report...")
    visualizer.plot_alignment_results(
        user_audio,
        alignment_results,
        madd_evaluations
    )
    
    # 6. Overall result
    correct = sum(
        1 for m in madd_evaluations
        if m['evaluation']['status'] == 'Correct'
    )
    total   = len(madd_evaluations)
    score   = round(correct / total * 100) if total else 0
    
    print("\n" + "=" * 50)
    print(f"Overall Score: {score}%")
    print(f"Correct: {correct}/{total} Madd")
    print("=" * 50)
    
    return {
        'alignment':  alignment_results,
        'madood':     madd_evaluations,
        'score':      score
    }
def parse_args():
    parser = argparse.ArgumentParser(
        description="Quran Tajweed Analysis CLI"
    )

    subparsers = parser.add_subparsers(dest="command")

    # ───────── analyze command ─────────
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze user recitation audio"
    )

    analyze_parser.add_argument(
        "--file",
        required=True,
        help="Path to user audio file"
    )

    analyze_parser.add_argument(
        "--surah",
        default="fatiha",
        help="Surah name (default: fatiha)"
    )

    analyze_parser.add_argument(
        "--output",
        help="Path to save JSON output"
    )

    return parser.parse_args()


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)


if __name__ == "__main__":
    args = parse_args()

    if args.command == "analyze":
        import json

        data_path = f"data/{args.surah}_madood.json"

        with open(data_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            exit(1)

        results = run_poc(
            user_audio_path=args.file,
            ayah_data=data["ayat"][0],
            words_dir="audio/reference/words"
        )

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(
                    results, 
                    f, 
                    ensure_ascii=False, 
                    indent=4, 
                    cls=NumpyEncoder
                )
            print(f"\n✅ Results saved to: {args.output}")

    else:
        print("❌ Please provide a command. Use --help")

    print("⚙️ Config Loaded:")
    print(settings)

