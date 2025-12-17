
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

### ✅ v1.3.2 - Final Stable (2025. 12. 17)
- **Perfect Script**: `m1_flux_perfect.sh` 도입. `vm_stat` 파싱 오류(점/쉼표)를 `sed`로 완전 제거하여 스크립트 안정성 100% 확보.
- **Safety**: `app.py` 내 PyTorch MPS 캐시 청소 로직에 `try-except` 구문을 추가하여 버전 호환성 문제 방지.

### ✅ v1.3.0 - 전문가 최적화
- **Stability**: `MPS_MAX_CONCURRENT=1` 적용으로 GPU 과부하 프리징 차단.
- **Intelligence**: 지능형 메모리 감시 도입.

### ✅ v1.2.0 - VS Code 격리
- **Fix**: VS Code 메모리 누수 방지 설정(`.vscode/settings.json`) 표준화.

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

```

### 2. VS Code 메모리 누수 방지 (필수)

VS Code가 대용량 모델 파일을 읽느라 시스템을 멈추게 하는 것을 방지합니다.

* **파일 생성:** `.vscode/settings.json`
* **내용:**
```json
{
    "files.watcherExclude": { "**/.git/**": true, "**/models/**": true, "**/output/**": true, "**/.venv/**": true },
    "search.exclude": { "**/models": true, "**/output": true, "**/.venv": true },
    "python.analysis.indexing": false,
    "extensions.ignoreRecommendations": true
}

```



### 3. 인증 설정

1. **Hugging Face:** `huggingface-cli login` (Flux 모델 접근용 Write 토큰).
2. **Gemini:** `.env` 파일에 API 키 입력 및 `src/brain.py` 모델 버전 확인.

### 4. App 코드 최적화 (app.py)

`app.py` 상단에 안정성 코드가 포함되어야 합니다.

```python
import os
import torch
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'
os.environ['TORCH_MPS_NO_TRANSLATION_STACK'] = '1'
os.environ['MPS_MAX_CONCURRENT'] = '1' # 핵심 안전장치

try:
    if torch.backends.mps.is_available():
        torch.mps.empty_cache()
except:
    pass

```

---

## 🚀 실행 방법 (Recommended Routine)

**⚠️ 절대 주의:** VS Code 터미널 대신 반드시 아래의 **자동화 스크립트**를 사용하세요.

### 1. 실행 스크립트 생성 (최초 1회)

터미널에 아래 명령어를 전체 복사/붙여넣기 하여 실행 스크립트를 생성합니다.

```bash
cat > ~/m1_flux_perfect.sh << 'EOF'
#!/bin/bash
echo "🚀 M1 Flux.1 완벽 버전"
sudo purge; sync
monitor_memory() {
    while true; do
        sleep 5
        # 숫자 파싱 오류 완전 제거
        FREE_PAGES=$(vm_stat | grep "Pages free" | awk '{print $3}' 2>/dev/null || echo 9999)
        FREE_PAGES_CLEAN=$(echo $FREE_PAGES | sed 's/\.//g' | sed 's/,//g')
        if [ ! -z "$FREE_PAGES_CLEAN" ] && [ "$FREE_PAGES_CLEAN" -lt 2000 ] 2>/dev/null; then
            echo "⚠️ 메모리 부족 감지 → 자동 정리"
            sudo purge > /dev/null 2>&1
        fi
    done
}
monitor_memory &
MONITOR_PID=$!
trap "kill $MONITOR_PID 2>/dev/null" EXIT

cd "/Volumes/Macbook_dat/Python/Korean_Edu_Factory" || exit 1
source .venv/bin/activate
pkill -9 -f code 2>/dev/null
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
export TORCH_MPS_NO_TRANSLATION_STACK=1
export MPS_MAX_CONCURRENT=1
echo "✅ Flux.1 시작 (3분 로딩 예상)"
streamlit run app.py --server.maxUploadSize=500
EOF

chmod +x ~/m1_flux_perfect.sh

```

### 2. 앱 실행

터미널에서 아래 명령어로 실행합니다.

```bash
~/m1_flux_perfect.sh

```

---

## 📂 폴더 구조

```
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
├── m1_flux_perfect.sh  # [New] 최종 완벽 실행 스크립트
├── app.py              # 메인 실행 파일
└── .env                # API 키 (비공개)

```

```
