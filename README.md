
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

### ✅ v1.0.0 - 최초 가동 성공 (2025. 12. 16)
- **Status**: MVP (Minimum Viable Product) 구현 완료
- **Key Achievements**:
  - Gemini API 연동을 통한 자동 기획 로직 구현
  - Flux 모델 Mac M1 GPU(MPS) 구동 및 **메모리 최적화(Offloading)** 적용
  - MoviePy 버전 호환성 문제 해결 (`moviepy` vs `moviepy.editor`)
  - **Critical Fix**: 외장하드 파일 시스템 문제(ExFAT → APFS)로 인한 한글 인코딩 에러 해결

---

## ⚙️ 설치 가이드 (Installation)

### 1. 환경 설정 및 라이브러리 설치
터미널을 열고 프로젝트 폴더에서 아래 명령어를 순서대로 실행하세요.

```bash
# 1. 가상환경 생성 및 활성화
python3.11 -m venv .venv
source .venv/bin/activate

# 2. pip 업데이트
pip install --upgrade pip

# 3. 필수 라이브러리 설치 (sentencepiece 포함)
pip install torch torchvision torchaudio diffusers transformers accelerate google-generativeai edge-tts streamlit pandas Pillow python-dotenv moviepy protobuf==3.20.3 watchdog sentencepiece

```

### 2. Hugging Face (이미지 모델) 인증 설정

고성능 이미지 모델(**Flux.1-schnell**) 사용을 위해 라이선스 동의 및 로그인이 필요합니다.

1. [Hugging Face](https://huggingface.co/join) 회원가입.
2. [Flux.1-schnell 모델 페이지](https://huggingface.co/black-forest-labs/FLUX.1-schnell) 접속 -> **"Agree and access repository"** 클릭 (필수).
3. [Settings > Access Tokens](https://huggingface.co/settings/tokens)에서 토큰(`Write` 권한) 발급.
4. 터미널 로그인:
```bash
huggingface-cli login
# 토큰 입력 후 엔터 (화면에 안 보여도 입력됨) -> Git credential 저장 여부는 'n'

```



### 3. Google Gemini (기획 모델) 설정

1. 프로젝트 루트에 `.env` 파일 생성:
```env
GEMINI_API_KEY=AIzaSy_본인의_API_키_입력

```


2. **[중요] 모델 버전 호환성 체크:**
사용자의 API 키 권한에 따라 사용 가능한 모델이 다릅니다 (`1.5-flash` vs `2.5-flash`). 동봉된 `check_model.py`를 실행하여 확인된 모델명을 `src/brain.py`에 적용해야 합니다.
```bash
python check_model.py

```



---

## 🚀 실행 방법 (How to Run)

```bash
# 가상환경 활성화 (이미 되어있다면 생략)
source .venv/bin/activate

# 앱 실행
streamlit run app.py

```

---

## ❓ 트러블슈팅 (Troubleshooting)

**Q1. "RuntimeError: MPS backend out of memory" (메모리 부족)**

* 원인: Flux 모델이 Mac의 통합 메모리를 초과하여 사용함.
* 해결: 강제 할당보다는 `src/visual.py`에서 **CPU Offloading**을 사용해야 함.
```python
# src/visual.py 수정
self.pipe.enable_model_cpu_offload() # .to("mps") 대신 사용

```



**Q2. "ValueError: Cannot instantiate this tokenizer..."**

* 원인: `sentencepiece` 라이브러리 누락.
* 해결: `pip install sentencepiece` 실행.

**Q3. "404 models/gemini-1.5-flash is not found..."**

* 원인: API 키가 해당 모델 버전을 지원하지 않음.
* 해결: `python check_model.py`로 사용 가능한 최신 모델(예: `gemini-2.5-flash`) 확인 후 `src/brain.py` 수정.

---

## 📂 폴더 구조

```
Korean_Edu_Factory/
├── src/
│   ├── brain.py        # 기획 (Gemini)
│   ├── visual.py       # 이미지 (Flux + MPS Optimized)
│   ├── audio.py        # 음성 (EdgeTTS)
│   ├── editor.py       # 편집 (MoviePy)
│   └── config.py       # 환경 설정
├── output/             # 결과물 저장소
├── models/             # AI 모델 캐시 (HuggingFace)
├── app.py              # 메인 실행 파일 (Streamlit)
├── check_model.py      # Gemini 모델 버전 확인용 스크립트
└── .env                # API 키 (비공개)

```

```