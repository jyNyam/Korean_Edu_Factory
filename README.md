
# 🏭 M1 한국어 교육 영상 공장 (Korean Edu Factory) - Hybrid Cloud Edition

**Apple Silicon M1(16GB) 환경**에 최적화된 교육용 콘텐츠 자동 생성 파이프라인입니다. 본 프로젝트는 로컬 디바이스의 하드웨어 한계를 극복하고 생성형 AI 기술을 교육 현장에 실질적으로 적용하기 위해 설계되었습니다.

초기 단계에서 **Apple MLX(mflux)** 프레임워크를 도입하여 순수 로컬 구동을 시도하였으나, 고해상도 이미지 생성 시 발생하는 GPU 타임아웃 문제를 해결하고자 **Hybrid(Cloud + Local)** 방식으로 아키텍처를 전면 개편하였습니다.

---

## 🚀 주요 기능

사용자가 교육 주제를 입력하면 기획부터 영상 렌더링까지 전 과정이 자동화됩니다.

1. **콘텐츠 기획(Brain):** 최신 Google GenAI SDK를 활용하여 교육용 어휘 선정 및 시나리오 기획을 수행합니다. (Gemini 1.5 Flash 모델 적용)
2. **시각 자료 생성(Visual):** 로컬 자원 소모를 최소화하기 위해 클라우드 기반의 Imagen 3 모델을 연동, 1024px 고화질 이미지를 신속하게 생성합니다.
3. **음성 합성(Audio):** Edge TTS 엔진을 사용하여 자연스러운 한국어 교수 학습 음성을 합성합니다.
4. **영상 합성(Editor):** MoviePy 엔진을 기반으로 이미지, 오디오, 자막을 결합하여 최종 MP4 파일을 렌더링합니다.

---

## 📅 개발 일지 (Development Log)

### ✅ v3.0.0 - Hybrid Architecture 전환

* **아키텍처 최적화:** M1 16GB 환경의 GPU 타임아웃(Exit Code -6) 이슈를 해결하기 위해 리소스 소모가 큰 이미지 생성 엔진을 Cloud(Imagen 3)로 전환하여 안정성을 확보하였습니다.
* **의존성 안정화:** MoviePy v2.0의 구조 변경에 따른 호환성 문제를 해결하기 위해 v1.0.3으로 버전을 고정하여 운영 안정성을 높였습니다.
* **SDK 고도화:** 최신 `google-genai` SDK를 도입하여 API 통신 효율을 개선하였습니다.

### 📜 v2.0.0 - MLX 로컬 최적화 실험

* **백엔드 교체:** PyTorch 대비 효율적인 메모리 관리를 위해 Apple MLX(mflux)로 엔진을 전환하였습니다.
* **메모리 최적화:** 4-bit Quantization(양자화) 기술을 적용하여 로컬 환경에서의 메모리 점유율을 약 50% 절감, OOM(Out of Memory) 현상을 방지하였습니다.

---

## 🛠 기술 스택 및 의존성

### 프로젝트 구조

```text
Korean_Edu_Factory/
├── src/
│   ├── brain.py        # Gemini 기반 콘텐츠 기획 모듈
│   ├── visual.py       # Cloud Imagen 연동 모듈
│   ├── audio.py        # Edge TTS 음성 합성 모듈
│   ├── editor.py       # MoviePy 영상 편집 모듈
│   └── config.py       # 시스템 환경 설정
├── output/             # 생성된 미디어 자산 저장 경로
├── app.py              # Streamlit 기반 메인 애플리케이션
└── .env                # API Key 및 환경 변수 관리

```

### 필수 라이브러리

본 프로젝트의 안정적인 구동을 위해 아래의 라이브러리 버전 준수를 권장합니다.

* `google-genai`: 최신 Gemini 및 Imagen API 연동
* `moviepy<2.0`: 영상 합성 엔진 (v1.0.3 권장)
* `edge-tts`: 음성 합성 처리
* `streamlit`: 웹 기반 사용자 인터페이스
* `python-dotenv`: 환경 변수 관리

---

## ⚙️ 설치 및 실행

1. **의존성 설치**
```bash
pip install "moviepy<2.0" google-genai edge-tts streamlit python-dotenv Pillow

```


2. **인증 설정**
루트 경로에 `.env` 파일을 생성하고 발급받은 API 키를 설정합니다.
```env
GEMINI_API_KEY=your_actual_api_key

```


3. **애플리케이션 실행**
```bash
streamlit run app.py --server.maxUploadSize=50 --server.headless=true

```
