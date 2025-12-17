
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

### ✅ v1.3.0 - 최종 전문가 최적화 (2025. 12. 17)
- **Stability**: `MPS_MAX_CONCURRENT=1` 환경변수 적용으로 GPU 과부하로 인한 프리징 원천 차단.
- **Intelligence**: Mac 네이티브 `vm_stat` 기반 지능형 메모리 감시 스크립트(`m1_flux_final.sh`) 도입. (무조건적인 Purge가 아닌, 실제 스왑 발생 시에만 작동)
- **Safety**: 스크립트 종료 시 모니터링 프로세스 자동 정리(`trap`) 기능 추가.

### ✅ v1.2.0 - VS Code 격리 및 워크플로우 개선
- **Critical Fix**: VS Code 메모리 누수(22GB+) 해결을 위해 인덱싱 차단 설정(`.vscode/settings.json`) 표준화.
- **Workflow**: 실행과 편집 환경의 물리적 분리.

### ✅ v1.1.0 - 메모리 효율화
- **Performance**: 이미지 생성 직후 즉시 가비지 컬렉션(GC) 수행.
- **UX**: CPU Offload 전략으로 모델 로딩 속도와 메모리 효율의 균형 확보.

### ✅ v1.0.0 - MVP 가동 성공 (2025. 12. 16)
- **Status**: 최초 파이프라인(Gemini-Flux-TTS-MoviePy) 연결 성공.

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

`app.py` 상단에 M1 안정성을 위한 환경변수 설정이 포함되어야 합니다.

```python
import os
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'
os.environ['TORCH_MPS_NO_TRANSLATION_STACK'] = '1'
os.environ['MPS_MAX_CONCURRENT'] = '1' # 핵심: 동시 작업 제한

```

---

## 🚀 실행 방법 (Recommended Routine)

**⚠️ 절대 주의:** VS Code 내부 터미널에서 실행하지 마십시오. 반드시 아래의 **자동화 스크립트**를 사용하여 실행해야 Mac 멈춤 현상을 방지할 수 있습니다.

### 1. 실행 스크립트 생성 (최초 1회)

터미널에 아래 명령어를 전체 복사/붙여넣기 하여 실행 스크립트를 생성합니다.

```bash
cat > ~/m1_flux_final.sh << 'EOF'
#!/bin/bash
echo "🚀 M1 Flux.1 최종 솔루션 (전문가 버전)"

# 초기화
sudo purge; sync

# 지능형 메모리 감시 (스왑 발생 시에만 정리)
monitor_memory() {
    while true; do
        PRESSURE=$(vm_stat | awk '/"Pageouts"/ {print $2}' | sed 's/\.//')
        if [ "$PRESSURE" -gt 1000 ]; then
             echo "⚠️ 메모리 압력 감지! 긴급 청소..."
             sudo purge > /dev/null 2>&1
             sync
        fi
        sleep 3
    done
}
monitor_memory &
MONITOR_PID=$!
trap "kill $MONITOR_PID 2>/dev/null" EXIT

# 실행 환경 설정
cd "/Volumes/Macbook_dat/Python/Korean_Edu_Factory" || exit 1
source .venv/bin/activate
pkill -9 -f code 2>/dev/null # VS Code 강제 격리

# 환경변수 적용
export PYTORCH_MPS_HIGH_WATERMARK_RATIO=0.0
export TORCH_MPS_NO_TRANSLATION_STACK=1
export MPS_MAX_CONCURRENT=1

echo "✅ Flux.1 로딩 시작 (첫 로딩 2-3분 소요, 절대 끄지 마세요)"
streamlit run app.py --server.maxUploadSize=500
EOF

chmod +x ~/m1_flux_final.sh

```

### 2. 앱 실행

터미널에서 아래 명령어로 실행합니다.

```bash
~/m1_flux_final.sh

```

*(비밀번호 입력 후, 메모리 정리와 함께 웹 페이지가 자동으로 열립니다.)*

---

## ❓ 트러블슈팅 (Troubleshooting)

**Q1. "Loading pipeline components..." 에서 멈춘 것 같아요.**

* **정상입니다.** M1 GPU 쉐이더 컴파일 및 메모리 스왑 과정으로, 최초 실행 시 3~5분까지 소요될 수 있습니다. 끄지 말고 기다리시면 반드시 실행됩니다.

**Q2. 실행 중 Mac이 멈춥니다.**

* `MPS_MAX_CONCURRENT=1` 설정이 적용되었는지 확인하세요. 반드시 `m1_flux_final.sh` 스크립트를 통해 실행해야 이 설정이 적용됩니다.

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
├── m1_flux_final.sh    # [New] 최종 전문가 실행 스크립트
├── app.py              # 메인 실행 파일
└── .env                # API 키 (비공개)

```

```
