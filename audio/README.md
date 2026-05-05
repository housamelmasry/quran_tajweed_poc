# Audio Files Guide

This folder contains all audio files for the Quran Tajweed POC project.

## 📁 Folder Structure

```
audio/
├── reference/
│   ├── words/     # Individual word recordings (one word per file)
│   └── full/      # Full ayah recordings
└── user/          # User test recordings (not tracked in git)
```

## 🔒 Storage & Privacy

- Audio files are stored **locally only**
- They are excluded via `.gitignore`
- Do NOT upload copyrighted recitations to public repositories

## 🎙️ How to Add Your Own Audio Files

### 1. **Reference Audio Files**

These are professional, correct Quran recitations used as a baseline for comparison.

#### Words Directory (`reference/words/`)

- **Purpose**: Store isolated Quranic words
- **File naming**: Use Arabic transliteration or phonetic names
- **Examples**:
  - `bismi.wav` - "بسم"
  - `allah.wav` - "الله"
  - `alrahman.wav` - "الرحمن"
  - `alraheem.wav` - "الرحيم"

**How to create word recordings:**

1. Record a professional Quran reciter pronouncing a single word
2. Save as `.wav` or `.mp3` format
3. Keep the audio clean (minimal background noise)
4. Trim silence at the beginning and end
5. Name the file clearly with the transliteration
6. Place in `reference/words/` folder

#### Full Directory (`reference/full/`)

- **Purpose**: Store complete Ayah (verse) recordings
- **File naming**: Use Surah name and Ayah number
- **Examples**:
  - `fatiha_001.wav` - Al-Fatiha, Ayah 1
  - `fatiha_002.wav` - Al-Fatiha, Ayah 2
  - `baqarah_001.wav` - Al-Baqarah, Ayah 1

**How to create full Ayah recordings:**

1. Record the complete Ayah from a professional recitation
2. Save as `.wav` or `.mp3` format
3. Ensure good audio quality
4. Include the entire Ayah without cutting off vowels
5. Use consistent naming: `{surah_name}_{ayah_number}.wav`
6. Place in `reference/full/` folder

### 2. **User Audio Files**

These are test recordings from learners that you want to analyze.

#### User Directory (`user/`)

- **Purpose**: Store user test recordings
- **File naming**: Use descriptive names with date or version
- **Examples**:
  - `test_001.wav` - First test recording
  - `user_fatiha_v1.wav` - User's Al-Fatiha recording, version 1
  - `2026_05_05_practice.wav` - Date-based naming

**How to record user audio:**

1. Record yourself or a learner reciting Quranic text
2. Use a quiet room to minimize background noise
3. Speak clearly and naturally
4. Save as `.wav` or `.mp3` format
5. Use clear naming with version/date information
6. Place in `user/` folder

## 🎵 Audio Format Requirements

### Recommended Specifications

- **Format**: WAV (preferred for quality) or MP3 (for compression)
- **Sample Rate**: 22050 Hz or 44100 Hz
- **Bit Depth**: 16-bit (for WAV files)
- **Channels**: Mono or Stereo (mono preferred for clarity)
- **Duration**:
  - Words: 0.5 - 2 seconds
  - Full Ayahs: 3 - 15 seconds

### File Size Guidelines

- **WAV files**: ~1-5 MB per file
- **MP3 files**: ~100-500 KB per file (much smaller)

## 🛠️ Tools to Record and Edit Audio

### Recording

- **Mac**: GarageBand, Audacity (free), Voice Memos
- **Windows**: Audacity (free), Windows Voice Recorder, OBS Studio
- **Linux**: Audacity (free), SoundRecorder
- **Online**: Vocaroo.com, WebRTC Audio Recorder

### Editing & Processing

- **Audacity** (Free, Cross-platform)
  - Remove silence
  - Normalize audio levels
  - Trim and cut
  - Export to WAV/MP3

- **Adobe Audition** (Paid)
- **GarageBand** (Mac only, free)
- **ffmpeg** (Command-line, free)

## 📝 Audio Processing Tips

1. **Remove Silence**: Trim beginning/end silence
2. **Normalize**: Set audio level to -3dB to prevent clipping
3. **Reduce Noise**: Use noise reduction filters
4. **Check Levels**: Ensure consistent volume across files
5. **Test Playback**: Play before submitting to verify quality
6. **Label Clearly**: Use descriptive file names

## 📊 Updating the Metadata

After adding audio files, update the corresponding JSON metadata file:

**Location**: `data/fatiha_madood.json`

**Example structure:**

```json
{
  "ayah": "Surah Al-Fatiha, Ayah 1",
  "words": [
    {
      "word": "بسم",
      "transliteration": "bismi",
      "file": "bismi.wav",
      "start_time": 0.0,
      "end_time": 0.5,
      "madd_rules": ["natural"]
    },
    {
      "word": "الله",
      "transliteration": "allah",
      "file": "allah.wav",
      "start_time": 0.6,
      "end_time": 1.2,
      "madd_rules": ["lenient"]
    }
  ]
}
```

## 🚀 Next Steps

1. Add reference word recordings to `reference/words/`
2. Add full Ayah recordings to `reference/full/`
3. Add your test recordings to `user/`
4. Update `data/fatiha_madood.json` with file paths and timings
5. Run `main.py` to analyze and visualize results

## ⚠️ Important Notes

- **Privacy**: These audio files are NOT uploaded to GitHub (see `.gitignore`)
- **Storage**: Store files locally only
- **Quality**: Professional reference audio produces better analysis
- **Consistency**: Use same recording conditions for all files
- **Backup**: Keep backups of important recordings

## 📞 Support

For issues with audio recording or processing:

1. Check audio file is in correct format (WAV/MP3)
2. Verify file path matches metadata JSON
3. Ensure sample rate is between 16kHz - 48kHz
4. Test audio plays correctly before processing

---

**Last Updated**: May 2026
