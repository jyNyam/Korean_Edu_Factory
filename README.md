
# 🏭 M1 한국어 교육 영상 공장 (Korean Edu Factory) - MLX Edition

**Mac M1(Silicon) 16GB 환경**에 최적화된 로컬 AI 영상 생성 파이프라인입니다.

기존 PyTorch/Diffusers 기반의 메모리 부족(OOM) 이슈를 해결하기 위해 **Apple MLX 프레임워크**를 도입하였습니다. 이를 통해 **M1 16GB 환경에서도 Flux.1 모델을 100% 안정적**으로 구동하며, 고품질의 교육용 숏폼 영상을 자동 생성합니다.

---

## 🚀 프로젝트 핵심 기능

사용자가 주제(예: "병원")를 입력하면 기획부터 영상 렌더링까지 전 과정이 자동화됩니다.

1. **Brain (Gemini):** 교육용 어휘 선정, 예문 작성 및 이미지 프롬프트 기획
2. **Visual (Flux.1-schnell on MLX):** **4-bit 양자화(Quantization)** 모델을 로컬에서 구동하여 고품질 일러스트 생성 (평균 메모리 점유 6~8GB)
3. **Audio (Edge TTS):** 자연스러운 한국어 AI 음성 합성
4. **Editor (MoviePy):** 이미지, 음성, 자막을 자동으로 합성하여 MP4 렌더링

### 🛠 Tech Stack (M1 Optimized)

* **OS**: macOS (Apple Silicon M1/M2/M3)
* **Language**: Python 3.11
* **Core Engine**: **Apple MLX (mflux)** - *Native Metal Performance*
* **Key Libraries**:
* `Streamlit`: 웹 기반 인터페이스(Web UI)
* `Google Gemini`: 콘텐츠 기획 및 로직 처리
* `mflux`: 로컬 이미지 생성 (Local Source Integration)
* `Edge TTS`: 음성 합성
* `MoviePy`: 영상 편집 및 자막 처리



---

## 📅 Development Log (개발 일지)

### ✅ v2.0.0 - The MLX Revolution (2025. 12. 17)

* **Engine Swap**: 기존 PyTorch/Diffusers 백엔드를 **Apple MLX (mflux)**로 전면 교체.
* **Memory Optimization**: `bfloat16` 로딩 시 발생하던 OOM(Process Killed) 현상을 **4-bit Quantization(`quantize=4`)** 적용으로 완벽 해결.
* **Stability Improvement**: 외부 라이브러리 의존성 충돌 방지를 위해 `mflux` 코어 소스를 `src/mflux`에 **직접 이식(Local Vendor)**.
* **Refactoring**: 불안정한 메모리 관리 스크립트(`sh`) 및 `sudo purge` 의존성 제거.

### ⚠️ Post-Mortem (이전 이슈 및 해결)

* **Issue**: M1 16GB 환경에서 Flux 모델 로딩 시 활성 메모리 초과로 인한 프로세스 강제 종료.
* **Cause**: PyTorch MPS 백엔드가 16GB 메모리 한계 상황에서 높은 오버헤드를 발생시킴.
* **Resolution**: Apple Silicon에 최적화된 MLX 프레임워크로 전환하여 메모리 점유율을 기존 대비 약 1/3 수준으로 절감.

---

## ⚙️ 설치 및 실행 가이드

### 1. 필수 라이브러리 설치

터미널에서 가상환경을 활성화한 후, MLX 및 필수 패키지를 설치합니다.

```bash
source .venv/bin/activate
pip install mlx mlx-lm numpy pillow huggingface_hub sentencepiece protobuf psutil streamlit google-generativeai edge-tts moviepy watchdog

```

### 2. 프로젝트 구조 (Local Source)

`mflux` 라이브러리와의 버전 충돌을 방지하기 위해 핵심 소스코드가 내장되어 있습니다.

```text
Korean_Edu_Factory/
├── src/
│   ├── mflux/          # [Core] MLX 엔진 소스코드 (Local Porting)
│   ├── visual.py       # MLX 기반 이미지 생성 모듈
│   ├── brain.py        # Gemini 기반 콘텐츠 기획 모듈
│   ├── audio.py        # TTS 처리 모듈
│   └── config.py       # 환경 설정
├── app.py              # 메인 실행 파일 (Sys Path Patch 적용)
└── .env                # API Key 설정 파일

```

### 3. 인증 설정 (.env)

프로젝트 루트 경로에 `.env` 파일을 생성하고 Gemini API 키를 입력합니다.

```env
GEMINI_API_KEY=your_api_key_here

```

---

## 🚀 실행 방법

별도의 복잡한 스크립트 없이 Streamlit 명령어로 즉시 실행 가능합니다.

```bash
# 가상환경 활성화
source .venv/bin/activate

# 애플리케이션 실행 (서버 리소스 최적화 옵션)
streamlit run app.py --server.maxUploadSize=50 --server.headless=true

```

1. 브라우저에서 `http://localhost:8501` 접속
2. 사이드바에 주제 입력 후 **[영상 생성 시작]** 버튼 클릭
3. 터미널 로그를 통해 진행 상황 확인

---

> **Note:** 본 프로젝트는 M1 환경에서의 로컬 AI 파이프라인 구축 가능성을 입증하며, 효율적인 영상 자동화 워크플로우를 제공합니다.
