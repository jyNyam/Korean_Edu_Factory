import streamlit as st
import sys
import os
import torch 
from pathlib import Path

# [v1.3.2 Final] M1 메모리 & 병렬처리 최적화
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'
os.environ['TORCH_MPS_NO_TRANSLATION_STACK'] = '1'
os.environ['MPS_MAX_CONCURRENT'] = '1'

# [Safety] 안전한 MPS 캐시 청소 (호환성 확보)
try:
    if torch.backends.mps.is_available():
        torch.mps.empty_cache()
except:
    pass # 구버전 torch 호환성 대비

# 1. 화면 설정
st.set_page_config(page_title="M1 영상 공장", layout="wide")

# 2. src 폴더 경로 추가 (모듈 불러오기 위함)
sys.path.append(str(Path(__file__).parent / 'src'))

# 3. 안전하게 모듈 로딩
try:
    from config import *
    if not GEMINI_API_KEY:
        st.error("❌ 오류: .env 파일에 GEMINI_API_KEY가 없습니다!")
        st.stop()
    from brain import BrainEngine
    from visual import VisualEngine
    from audio import AudioEngine
    from editor import EditorEngine
except Exception as e:
    st.error(f"⚠️ 시스템 로딩 실패: {e}")
    st.info("터미널에 'pip install'은 하셨나요?")
    st.stop()

st.title("🏭 M1 한국어 교육 영상 공장 (Github Ver.)")

# 4. Session State: AI 엔진을 한 번만 켜두기 위함
if 'visual' not in st.session_state:
    try:
        with st.spinner("🔧 AI 엔진 시동 거는 중... (약 10초 소요)"):
            st.session_state.visual = VisualEngine()
            st.session_state.audio = AudioEngine()
            st.session_state.brain = BrainEngine()
    except Exception as e:
        st.error(f"엔진 초기화 실패: {e}")
        st.stop()

# 5. 사이드바 (설정창)
with st.sidebar:
    st.header("⚙️ 설정")
    topic = st.text_input("주제 입력", "병원")
    count = st.slider("단어 개수", 1, 5, 3)

# 6. 메인 실행 버튼
if st.button("🎬 영상 생성 시작", type="primary"):
    with st.status("🚀 작업 진행 중...", expanded=True) as status:
        
        # [Step 1] 기획
        st.write("🧠 AI가 기획 중...")
        data = st.session_state.brain.generate_vocabulary_data(topic, count)
        
        if data:
            st.write(f"✅ 기획 완료: {len(data['words'])}개 단어")
            
            # [Step 2] 반복 제작 Loop
            for i, item in enumerate(data['words']):
                idx = i + 1
                word = item['korean']
                
                # 파일 저장 경로 설정
                p_img = IMAGES_DIR / f"{topic}_{idx}.png"
                p_aud = AUDIO_DIR / f"{topic}_{idx}.mp3"
                p_vid = FINAL_DIR / f"{topic}_{idx}_{word}.mp4"
                
                st.write(f"🎨 [{idx}/{count}] '{word}' 제작 중...")
                
                # AI 엔진 동작
                st.session_state.visual.generate_image(item['image_prompt'], p_img)
                st.session_state.audio.generate_audio(f"{word}. {item['example']}", p_aud)
                EditorEngine.create_video(p_img, p_aud, p_vid, word)
                
                # 화면에 결과물 표시 (2단 컬럼)
                col1, col2 = st.columns([1, 1])
                with col1: st.image(str(p_img), caption=f"이미지: {word}")
                with col2: st.video(str(p_vid))

            # 메모리 정리
            st.session_state.visual.unload_model()
            status.update(label="🎉 모든 작업 완료!", state="complete")
            st.success("영상 생성이 끝났습니다! output 폴더를 확인하세요.")