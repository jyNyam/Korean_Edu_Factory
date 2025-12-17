# src/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
PROJECT_ROOT = Path(os.getcwd())

# [안전 프로파일 - M1 16GB 전용]
FLUX_MODEL = "black-forest-labs/FLUX.1-schnell"
IMAGE_SIZE = 512  # 1024→512로 변경 (메모리 60% 절감)
BATCH_SIZE = 1    # 무조건 1로 고정

TTS_VOICE = "ko-KR-SunHiNeural"
VIDEO_FPS = 24
FONT_PATH = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"

# 경로 설정
OUTPUT_DIR = PROJECT_ROOT / 'output'
IMAGES_DIR = OUTPUT_DIR / 'images'
AUDIO_DIR = OUTPUT_DIR / 'audio'
FINAL_DIR = OUTPUT_DIR / 'final'
MODELS_DIR = PROJECT_ROOT / 'models'
LOGS_DIR = PROJECT_ROOT / 'logs'

# API 키 검증
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("❌ .env 파일을 확인해주세요! API 키가 없습니다.")
