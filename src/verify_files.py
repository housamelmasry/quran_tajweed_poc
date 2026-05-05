# verify_files.py
import os
import json

def verify_audio_files(json_path, words_dir):
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    missing = []
    found   = []
    
    for ayah in data['ayat']:
        for word in ayah['words']:
            path = os.path.join(words_dir, word['file'])
            if os.path.exists(path):
                found.append(word['file'])
            else:
                missing.append({
                    'file':  word['file'],
                    'word':  word['word'],
                    'ayah':  ayah['ayah']
                })
    
    print(f"✅ Found:  {len(found)}")
    print(f"❌ Missing:   {len(missing)}")
    
    if missing:
        print("\nmissing files:")
        for m in missing:
            print(
                f"  Ayah {m['ayah']} — "
                f"{m['word']} — "
                f"{m['file']}"
            )
    else:
        print("\n🎉 All files are present — ready for playback")
        # print("\n🎉 جميع الملفات موجودة — جاهز للتشغيل")

if __name__ == "__main__":
    verify_audio_files(
        'data/fatiha_madood.json',
        'audio/reference/words/'
    )