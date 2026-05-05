import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ───────────────────────────────
# Audio Settings
# ───────────────────────────────
@dataclass
class AudioConfig:
    sample_rate: int = int(os.getenv("AUDIO_SR", 16000))
    mono: bool = True
    normalize: bool = True
    trim_db: int = 20


# ───────────────────────────────
# Feature Extraction
# ───────────────────────────────
@dataclass
class FeatureConfig:
    n_mfcc: int = 13
    hop_length: int = 128


# ───────────────────────────────
# DTW Alignment
# ───────────────────────────────
@dataclass
class DTWConfig:
    step: int = 10
    mfcc_dims_used: int = 3   # For performance optimization


# ───────────────────────────────
# Visualization
# ───────────────────────────────
@dataclass
class VisualizationConfig:
    save_path: str = "output/analysis_result.png"
    dpi: int = 150


# ───────────────────────────────
# Root Settings Object
# ───────────────────────────────
@dataclass
class Settings:
    audio: AudioConfig = field(default_factory=AudioConfig)
    feature: FeatureConfig = field(default_factory=FeatureConfig)
    dtw: DTWConfig = field(default_factory=DTWConfig)
    visualization: VisualizationConfig = field(default_factory=VisualizationConfig)


# Singleton instance
settings = Settings()