
# 🏭 M1 한국어 교육 영상 공장 (Korean Edu Factory) - MLX Edition

**Mac M1(Silicon) 16GB 환경**에 최적화된 로컬 AI 영상 생성 파이프라인입니다.

기존 PyTorch/Diffusers 방식의 메모리 부족(OOM) 문제를 극복하기 위해 **Apple MLX 프레임워크**를 도입하여, **M1 16GB에서도 Flux.1 모델을 100% 안정적**으로 구동합니다.

---

## 🚀 프로젝트 핵심 기능
사용자가 주제(예: "병원")를 입력하면 버튼 하나로 영상이 완성됩니다.
1.  **Brain (Gemini):** 교육용 단어 선정, 예문 작성, 이미지 프롬프트 기획
2.  **Visual (Flux.1-schnell on MLX):** **4-bit 양자화**된 로컬 모델로 고품질 일러스트 생성 (메모리 사용량 6~8GB)
3.  **Audio (Edge TTS):** 자연스러운 한국어 AI 음성 생성
4.  **Editor (MoviePy):** 이미지+음성+자막 자동 합성을 통한 MP4 렌더링

### 🛠 Tech Stack (M1 Optimized)
- **OS**: macOS (Apple Silicon M1/M2/M3)
- **Language**: Python 3.11
- **Core Engine**: **Apple MLX (mflux)** - *Native Metal Performance*
- **Key Libraries**:
  - `Streamlit`: 웹 UI
  - `Google Gemini`: 기획 LLM
  - `mflux`: 이미지 생성 (Local Source Integration)
  - `Edge TTS`: 음성 합성
  - `MoviePy`: 영상 편집

---

## 📅 Development Log (개발 일지)

### ✅ v2.0.0 - The MLX Revolution (2025. 12. 17)
- **Engine Swap**: PyTorch/Diffusers → **Apple MLX (mflux)** 전면 교체.
- **Memory Fix**: `bfloat16` 로딩 시 발생하던 OOM(Killed) 현상을 **4-bit Quantization(`quantize=4`)**으로 완벽 해결.
- **Stability**: 외부 라이브러리 경로 꼬임 방지를 위해 `mflux` 소스코드를 `src/mflux`에 **직접 이식(Local Vendor)**.
- **Legacy Removal**: 불안정한 메모리 청소 스크립트(`sh`) 및 `sudo purge` 의존성 제거.

### ⚠️ 이전 이슈 해결 (Post-Mortem)
- **문제**: M1 16GB에서 Flux 모델 로딩 시 활성 메모리 폭주로 프로세스 강제 종료.
- **원인**: PyTorch의 MPS 백엔드가 16GB 메모리 한계에서 오버헤드 발생.
- **해결**: Apple이 직접 최적화한 MLX 프레임워크로 전환하여 메모리 사용량을 1/3 수준으로 절감.

---

## ⚙️ 설치 및 실행 가이드

### 1. 필수 라이브러리 설치
터미널에서 가상환경 진입 후, MLX 및 필수 패키지를 설치합니다.

```bash
source .venv/bin/activate
pip install mlx mlx-lm numpy pillow huggingface_hub sentencepiece protobuf psutil streamlit google-generativeai edge-tts moviepy watchdog

```

### 2. 프로젝트 구조 (Local Source)

`mflux` 라이브러리 충돌 방지를 위해 소스코드가 내장되어 있습니다.

```
Korean_Edu_Factory/
├── src/
│   ├── mflux/          # [핵심] MLX 엔진 소스코드 (직접 이식됨)
│   ├── visual.py       # MLX 기반 이미지 생성기 (경로 최적화됨)
│   ├── brain.py        # Gemini 기획
│   ├── audio.py        # TTS
│   └── config.py       # 설정
├── app.py              # 메인 실행 파일 (Sys Path Patch 적용)
└── .env                # GEMINI_API_KEY 저장

```

### 3. 인증 설정 (.env)

프로젝트 루트에 `.env` 파일을 생성하고 키를 입력하세요.

```env
GEMINI_API_KEY=your_api_key_here

```

---

## 🚀 실행 방법

더 이상 복잡한 스크립트가 필요 없습니다. Streamlit만 실행하면 됩니다.

```bash
# 가상환경 활성화
source .venv/bin/activate

# 앱 실행 (메모리 절약 옵션 권장)
streamlit run app.py --server.maxUploadSize=50 --server.headless=true

```

1. 브라우저에서 `http://localhost:8501` 접속
2. 주제 입력 후 **[영상 생성 시작]** 클릭
3. 터미널에서 다운로드/생성 로그 확인

```


**이제 M1 맥북은 훌륭한 영상 공장이 되었습니다. 개발을 즐기세요!**