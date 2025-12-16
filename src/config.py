import os
from pathlib import Path
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 프로젝트의 뿌리 경로(Root) 설정
PROJECT_ROOT = Path(os.getcwd())

# ---------------------------------------------------------
# [폴더 자동 생성]
# 코드가 실행될 때 필요한 폴더가 없으면 자동으로 만듭니다.
# ---------------------------------------------------------
OUTPUT_DIR = PROJECT_ROOT / 'output'
IMAGES_DIR = OUTPUT_DIR / 'images'
AUDIO_DIR = OUTPUT_DIR / 'audio'
FINAL_DIR = OUTPUT_DIR / 'final'
MODELS_DIR = PROJECT_ROOT / 'models'
LOGS_DIR = PROJECT_ROOT / 'logs'

# 반복문을 돌면서 폴더 생성
for directory in [OUTPUT_DIR, IMAGES_DIR, AUDIO_DIR, FINAL_DIR, MODELS_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# API 키 가져오기
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("⚠️ 경고: .env 파일에서 API 키를 찾을 수 없습니다.")

# 각종 설정값 (상수)
FLUX_MODEL = "black-forest-labs/FLUX.1-schnell" # 이미지 모델명
IMAGE_SIZE = 768
TTS_VOICE = "ko-KR-SunHiNeural" # 목소리 설정
VIDEO_FPS = 24
FONT_PATH = "/System/Library/Fonts/Supplemental/AppleGothic.ttf" # 맥 한글 폰트