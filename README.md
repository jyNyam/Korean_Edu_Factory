# 🏭 M1 한국어 교육 영상 공장 (Korean Edu Factory)

**Mac M1(Silicon) 환경**에서 로컬 AI를 활용하여 외국인 노동자 및 유학생을 위한 **한국어 교육용 숏폼 영상**을 자동으로 생성하는 올인원 파이프라인 프로젝트입니다.

**Gemini (기획)** + **Flux (이미지)** + **Edge TTS (음성)** + **MoviePy (편집)**를 연결하여, 주제만 입력하면 버튼 하나로 영상을 완성합니다.

---

## 🚀 프로젝트 소개
사용자가 주제(예: "병원", "공항")를 입력하면 다음과 같은 과정을 거쳐 영상이 제작됩니다.
1.  **Brain (Gemini):** 주제에 맞는 필수 단어 선정 및 예문 작성, 프롬프트 엔지니어링
2.  **Visual (Flux.1-schnell):** Mac M1 GPU 가속을 활용한 고품질 일러스트 생성
3.  **Audio (Edge TTS):** 자연스러운 한국어 AI 성우 내레이션 생성
4.  **Editor (MoviePy):** 이미지, 자막, 음성을 합성하여 MP4 영상 렌더링

### 🛠 Tech Stack
- **OS**: macOS (Apple Silicon M1/M2/M3)
- **Environment**: Python 3.11 / VS Code
- **Storage**: External SSD (**APFS Format 필수**)
- **Key Libraries**:
  - `Streamlit`: 웹 UI 인터페이스
  - `Google Gemini`: 콘텐츠 기획
  - `Flux (Diffusers)`: 온디바이스 이미지 생성 (MPS 가속)
  - `Edge TTS`: 음성 합성
  - `MoviePy`: 영상 편집

---

## 📅 Development Log (개발 일지)

### ✅ v1.2.0 - 시스템 안정화 및 프리징 해결 (2025. 12. 17)
- **Critical Fix**: VS Code 메모리 누수(22GB+)로 인한 Mac 프리징 현상 해결.
- **Workflow**: `run_factory.sh` 쉘 스크립트 도입. (메모리 청소(`purge`) → 가상환경 실행 → 앱 구동 자동화)
- **Optimization**: VS Code 인덱싱 차단 설정(`.vscode/settings.json`) 표준화.

### ✅ v1.1.0 - 메모리 최적화 (2025. 12. 17)
- **Performance**: 이미지 생성 직후 즉시 가비지 컬렉션(GC) 수행.
- **UX**: 모델 로딩 지연 제거 (CPU Offload 유지 전략).

### ✅ v1.0.0 - 최초 가동 성공 (2025. 12. 16)
- **Status**: MVP 구현 완료.
- **Key Achievements**: Gemini 기획, Flux(MPS) 구동, 한글 자막 인코딩 해결.

---



## ⚙️ 설치 가이드 (Installation)

### 1. 환경 설정 및 라이브러리 설치
터미널을 열고 프로젝트 폴더에서 아래 명령어를 순서대로 실행하세요.

```bash
# 1. 가상환경 생성 및 활성화
python3.11 -m venv .venv
source .venv/bin/activate

# 2. 필수 라이브러리 설치
pip install --upgrade pip
pip install torch torchvision torchaudio diffusers transformers accelerate google-generativeai edge-tts streamlit pandas Pillow python-dotenv moviepy protobuf==3.20.3 watchdog sentencepiece
2. VS Code 메모리 누수 방지 (필수)
VS Code가 대용량 모델 파일을 읽느라 시스템을 멈추게 하는 것을 방지합니다.

파일 생성: .vscode/settings.json

내용:

JSON

{
    "files.watcherExclude": { "**/.git/**": true, "**/models/**": true, "**/output/**": true, "**/.venv/**": true },
    "search.exclude": { "**/models": true, "**/output": true, "**/.venv": true },
    "python.analysis.indexing": false
}
3. 인증 설정
Hugging Face: huggingface-cli login (Flux 모델 접근용 Write 토큰).

Gemini: .env 파일에 API 키 입력 및 src/brain.py 모델 버전 확인.

🚀 실행 방법 (Recommended Routine)
⚠️ 주의: VS Code 내부 터미널에서 실행하지 마십시오. 메모리 부족으로 Mac이 멈출 수 있습니다. 반드시 아래의 자동화 스크립트를 사용하여 실행하세요.

1. 실행 스크립트 생성 (최초 1회)
프로젝트 루트에 run_factory.sh 파일을 생성하고 아래 내용을 붙여넣으세요.

Bash

#!/bin/bash
# run_factory.sh
echo "🧹 Mac 메모리 정리 중 (Password 입력)..."
sudo purge
source .venv/bin/activate
echo "🚀 영상 공장 가동!"
streamlit run app.py --server.maxUploadSize=500
그 후 실행 권한을 부여합니다: chmod +x run_factory.sh

2. 앱 실행
터미널에서 아래 명령어로 실행합니다.

Bash

./run_factory.sh
(비밀번호 입력 후, 메모리 정리와 함께 웹 페이지가 자동으로 열립니다.)

❓ 트러블슈팅 (Troubleshooting)
Q1. 실행 중 Mac이 완전히 멈췄습니다(프리징).

원인: VS Code가 메모리를 과다 점유한 상태에서 모델을 로드했기 때문입니다.

해결: 전원 버튼을 길게 눌러 강제 재부팅 후, 반드시 **run_factory.sh**로 실행하세요.

Q2. "RuntimeError: MPS backend out of memory"

해결: src/visual.py에 CPU Offloading 및 GC 코드가 적용되었는지 확인하세요.



📂 폴더 구조
Korean_Edu_Factory/
├── src/
│   ├── brain.py        # 기획 (Gemini)
│   ├── visual.py       # 이미지 (Flux + GC Optimized)
│   ├── audio.py        # 음성 (EdgeTTS)
│   ├── editor.py       # 편집 (MoviePy)
│   └── config.py       # 환경 설정
├── output/             # 결과물 저장소
├── models/             # AI 모델 캐시 (VS Code 인덱싱 제외됨)
├── .vscode/            # VS Code 최적화 설정
├── run_factory.sh      # [New] 안전 실행 스크립트
├── app.py              # 메인 실행 파일
└── .env                # API 키 (비공개)
