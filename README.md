# 🏭 M1 한국어 교육 영상 공장 (Korean Edu Factory)

Mac M1 환경에서 AI를 활용해 한국어 교육용 숏폼 영상을 자동으로 생성하는 파이프라인 프로젝트입니다.
기획(Brain)부터 이미지(Visual), 음성(Audio), 편집(Editor)까지 버튼 하나로 자동화합니다.

## 🚀 프로젝트 소개
외국인 노동자 및 학생을 위한 한국어 단어 학습 영상을 대량 생산하기 위해 구축되었습니다.
사용자가 주제(예: 병원)만 입력하면, AI가 단어를 선정하고 예문을 만들며, 그림과 목소리까지 생성해 영상으로 합칩니다.

### 🛠 Tech Stack
- **OS**: macOS (Apple Silicon M1)
- **Environment**: Python 3.11 / VS Code
- **Storage**: External SSD (APFS Format)
- **Key Libraries**:
  - `Streamlit`: 웹 UI 인터페이스
  - `Google Gemini`: 콘텐츠 기획 및 프롬프트 생성
  - `Flux (Diffusers)`: 고품질 일러스트 생성 (On-device)
  - `Edge TTS`: 자연스러운 한국어 음성 생성
  - `MoviePy`: 영상 편집 및 자막 합성

## 📅 Development Log (개발 일지)

### ✅ v1.0.0 - 최초 가동 성공 (2025. 12. 16)
- **Status**: MVP (Minimum Viable Product) 구현 완료
- **Key Achievements**:
  - Gemini API 연동을 통한 자동 기획 로직 구현
  - Flux 모델을 Mac M1 GPU(MPS)로 구동 성공
  - MoviePy 버전 호환성 문제 해결 (`moviepy` vs `moviepy.editor`)
  - **Critical Fix**: 외장하드 파일 시스템 문제(ExFAT → APFS)로 인한 한글 인코딩(`0xb0`) 에러 완벽 해결

## ⚙️ 설치 및 실행 방법 (How to Run)

### 1. 환경 설정
이 프로젝트는 Mac M1 및 APFS 포맷된 저장소에 최적화되어 있습니다.

```bash
# 1. 가상환경 생성 및 활성화
python3.11 -m venv .venv
source .venv/bin/activate

# 2. 필수 라이브러리 설치
pip install -r requirements.txt

# 3. API 키 설정 (필수) 
GEMINI_API_KEY=your_api_key_here

# 4. 실행
streamlit run app.py


# 📂 폴더 구조
Korean_Edu_Factory/
├── src/
│   ├── brain.py        # 기획 (Gemini)
│   ├── visual.py       # 이미지 (Flux)
│   ├── audio.py        # 음성 (EdgeTTS)
│   ├── editor.py       # 편집 (MoviePy)
│   └── config.py       # 환경 설정
├── output/             # 결과물 (자동 생성)
├── models/             # AI 모델 캐시
├── app.py              # 메인 실행 파일
├── requirements.txt    # 라이브러리 목록
└── .env                # API 키 (비공개)


# 🏭 Mac M1 한국어 교육 영상 공장 (Korean_Edu_Factory)

## 🛠️ 필수 설정 가이드 (설치 후 최초 1회)

### 1. Hugging Face 토큰 설정 (이미지 생성용)
이 프로젝트는 고성능 이미지 모델인 **Flux.1-schnell**을 사용합니다. 이 모델을 다운로드하려면 승인된 토큰이 필요합니다.

1. [Hugging Face](https://huggingface.co/join) 회원가입.
2. [Flux.1-schnell 모델 페이지](https://huggingface.co/black-forest-labs/FLUX.1-schnell) 접속 후 **"Agree and access repository"** 버튼 클릭 (필수).
3. [Settings > Access Tokens](https://huggingface.co/settings/tokens)에서 `Write` 권한으로 새 토큰 발급.
4. 터미널에서 로그인:
   ```bash
   huggingface-cli login


   
