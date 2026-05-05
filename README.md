# Quran Tajweed POC (Proof of Concept)

## ⚠️ Audio Notice

Audio files are **NOT included** in this repository due to licensing restrictions.

- You must provide your own audio files
- Ensure you have the right to use any Quran recitations
- See `DATA_POLICY.md` for full details

## 📖 Disclaimer

This project is for **educational and research purposes only**.

It does NOT replace:

- Learning with a qualified Quran teacher
- Formal Tajweed study

Results may not be fully accurate and should be used as a supportive tool only.

## 📖 Project Overview

This is a **Proof of Concept** project for analyzing Quran recitations with a focus on **Tajweed** rules. It uses audio processing, signal alignment, and machine learning techniques to compare user Quran recitations against reference recordings and provide feedback on proper pronunciation, timing, and Tajweed rule adherence.

## 🎯 Project Goals

- **Audio Analysis**: Process and analyze Quran recitation audio files
- **Word Alignment**: Match and align words from user audio with reference recordings
- **Tajweed Analysis**: Detect and analyze specific Tajweed rules (particularly **Madd** - elongation rules)
- **Visualization**: Provide visual feedback to help users improve their recitation
- **Feedback System**: Generate actionable insights for learners

## 📁 Project Structure

```
quran_tajweed_poc/
├── audio/
│   ├── reference/           # Reference recordings for comparison
│   │   ├── words/          # Isolated word recordings
│   │   │   ├── bismi.wav
│   │   │   ├── allah.wav
│   │   │   ├── alrahman.wav
│   │   │   └── alraheem.wav
│   │   └── full/           # Full Ayah (verse) recordings
│   │       └── fatiha.wav
│   └── user/               # User recordings to analyze
│       └── test.wav
├── data/
│   └── fatiha_madood.json  # Metadata: word timings, Madd rules, etc.
├── src/
│   ├── audio_processor.py  # Audio loading, preprocessing, cleaning
│   ├── aligner.py          # Word alignment between user and reference audio
│   ├── madd_analyzer.py    # Tajweed Madd rule detection and analysis
│   ├── audio_aligner.py    # Additional alignment utilities
│   ├── onset_detector.py   # Sound onset detection
│   └── visualizer.py       # Generate visualizations of analysis results
├── main.py                 # Main entry point for the POC
├── structure.md            # Project structure documentation
└── .gitignore              # Git ignore rules (excludes audio files)
```

## 🔧 Technology Stack

### Core Libraries

- **librosa**: Audio processing and feature extraction
- **numpy**: Numerical computations
- **scipy**: Scientific computing (signal processing)
- **soundfile**: WAV file I/O
- **matplotlib**: Data visualization
- **dtaidistance**: Dynamic Time Warping (DTW) for audio alignment

### Python Version

- Python 3.14.0+

## 🚀 Getting Started

### Prerequisites

- Python 3.14+
- pip (Python package manager)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/housamelmasry/quran_tajweed_poc.git
cd quran_tajweed_poc
```

2. Install dependencies:

```bash
pip install librosa numpy scipy matplotlib soundfile dtaidistance
```

### Running the POC

```bash
python main.py
```

The main script will:

1. Load reference audio files
2. Process user-provided audio
3. Align words between user and reference recordings
4. Analyze Tajweed rules (Madd)
5. Generate visualizations
6. Output results to the `output/` folder

## 📊 Data Format

### Audio Files

- **Format**: WAV or MP3
- **Samples per second**: Configurable (typically 22050 Hz or 44100 Hz)
- **Reference audio**: Clean, professionally recorded Quran recitation
- **User audio**: Input for analysis

### Metadata (JSON)

Example structure in `fatiha_madood.json`:

```json
{
  "ayah": "Surah Al-Fatiha, Ayah 1",
  "words": [
    {
      "word": "بسم",
      "file": "bismi.wav",
      "start_time": 0.0,
      "end_time": 0.5,
      "madd_rules": ["iddah"]
    },
    ...
  ]
}
```

## 🎓 Key Concepts

### Tajweed

Islamic rules for proper Quran recitation, including pronunciation, timing, and elongation rules.

### Madd (المد)

Elongation or prolongation of vowel sounds in specific conditions. The project analyzes:

- **Madd Asli** (Natural Madd)
- **Madd Tabee** (Lenient Madd)
- **Madd Farq** (Differentiating Madd)
- Other advanced Madd rules

### Word Alignment (DTW)

Uses Dynamic Time Warping to match words in user audio with reference recordings, accounting for different speaking speeds.

## 🔄 Workflow

```
User Audio Input
       ↓
Audio Processing (noise reduction, normalization)
       ↓
Feature Extraction (MFCC, spectrograms)
       ↓
Word Alignment (DTW against reference)
       ↓
Tajweed Rule Analysis (Madd detection)
       ↓
Visualization & Feedback Report
       ↓
Output (Graphs, JSON results)
```

## 📝 Core Modules

### `audio_processor.py`

- `AudioProcessor` class for loading, cleaning, and preprocessing audio
- Noise reduction, normalization
- Feature extraction (spectrograms, MFCCs)

### `aligner.py`

- `WordAligner` class for aligning user audio with reference recordings
- Uses DTW (Dynamic Time Warping) for time-series matching
- Handles variable speech rates

### `madd_analyzer.py`

- `MaddAnalyzer` class for detecting Tajweed Madd rules
- Analyzes vowel elongation patterns
- Compares user performance against reference

### `visualizer.py`

- `Visualizer` class for creating visual feedback
- Waveform plots, spectrograms, alignment visualizations
- Saves results to `output/` folder

## 🚫 Git Ignoring

Audio files (`.wav`, `.mp3`) and the `audio/` folder are not tracked by Git to keep the repository lightweight. Store audio files locally.

## 📦 Output Files

Analysis results are saved to the `output/` folder:

- `alignment_plot.png` - Visual alignment of user vs reference
- `spectrogram_comparison.png` - Spectrogram analysis
- `results.json` - Detailed analysis results
- `feedback_report.txt` - Human-readable feedback

## 🔮 Future Enhancements

- [ ] Web interface for user testing
- [ ] Real-time audio processing
- [ ] Machine learning model for automated Tajweed grading
- [ ] Support for multiple Quranic chapters
- [ ] Mobile application
- [ ] Multi-user feedback and progress tracking

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source. Check LICENSE file for details.

## ⚠️ Audio Notice

Audio files are not included in this repository due to licensing restrictions.
Please refer to DATA_POLICY.md for details.

## 💬 Questions & Support

For questions or support, please open an issue on the GitHub repository.

---

**Last Updated**: May 2026  
**Project Status**: Proof of Concept (Active Development)
