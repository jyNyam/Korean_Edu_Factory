네, Nyam 님! 오늘 우리가 함께 이뤄낸 **메모리 최적화(v1.1.0)** 내용을 포함하여 `README.md`를 완벽하게 업데이트해 드리겠습니다.

아래 내용을 복사해서 `README.md` 파일에 덮어쓰기 하신 후, 하단에 적어드린 **GitHub 업데이트 명령어**를 실행하시면 됩니다.

---

### 📝 README.md (전체 복사 후 덮어쓰기)

```markdown
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

### ✅ v1.1.0 - 시스템 안정화 및 자동화 (2025. 12. 17)
- **Performance**: VS Code 메모리 누수 문제 해결 (인덱싱 차단 적용, 22GB → 500MB)
- **Optimization**: 이미지 생성 직후 즉시 가비지 컬렉션(GC) 수행으로 스왑 방지
- **Automation**: `start_factory.command` 도입으로 `sudo purge` 및 앱 실행 원클릭 자동화
- **UX**: 모델 로딩 지연 제거 (CPU Offload 유지 전략)

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

### 2. VS Code 메모리 최적화 (필수)

VS Code가 대용량 모델 파일을 읽느라 메모리를 과다 점유하는 것을 막기 위해 설정 파일을 생성합니다.

* **경로:** `.vscode/settings.json`
* **내용:**
```json
{
    "files.watcherExclude": { "**/.git/**": true, "**/models/**": true, "**/output/**": true, "**/.venv/**": true },
    "search.exclude": { "**/models": true, "**/output": true, "**/.venv": true },
    "python.analysis.indexing": false
}

```



### 3. Hugging Face & Gemini 설정

1. **Hugging Face:** `flux_key` 발급 후 `huggingface-cli login` (Write 권한).
2. **Gemini:** `.env` 파일에 API 키 입력. `check_model.py`로 사용 가능 모델 버전(예: 2.5-flash) 확인 후 `src/brain.py` 수정.



## ❓ 트러블슈팅 (Troubleshooting)

**Q1. "RuntimeError: MPS backend out of memory"**

* Flux 모델이 Mac 메모리를 초과함. `src/visual.py`에 CPU Offloading 및 GC 코드가 적용되었는지 확인.

**Q2. VS Code가 너무 느리거나 멈춥니다.**

* `.vscode/settings.json` 파일이 제대로 생성되었는지 확인.
실행은 VS Code가 아닌 `start_factory.command`로 진행.

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
├── start_factory.command # 원클릭 실행 스크립트
├── app.py              # 메인 실행 파일
└── .env                # API 키 (비공개)

```

```
